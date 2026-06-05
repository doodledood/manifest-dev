import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join, resolve } from "node:path";
import { defineTool, type ExtensionAPI, type ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import {
	aggregateVerificationStatus,
	buildGateVerifierPrompt,
	evaluateDoneReadiness,
	extractManifestGates,
	extractReposMap,
	makeBlockedVerificationRecord,
	parseRunState,
	planVerifierBatches,
	resolvePositiveIntConfig,
	resolveStringConfig,
	resolveVerifierModel,
	runStateFileName,
	sha256,
	shouldTerminateOutcome,
	toGateVerificationResult,
	unquote,
	verificationToolResponse,
	waitForVerifierRecords,
	type GateVerificationResult,
	type ManifestGate,
	type SubagentsRecordService,
	type VerificationRecord,
} from "./manifest-dev-runtime.ts";

type ManifestOutcome = "done" | "escalate";
type ManifestCommand = "manifest-do" | "manifest-auto" | "manifest-babysit-pr";

interface RunRecord {
	runId: string;
	command: ManifestCommand;
	startedAt: string;
	cwd: string;
	manifestPath?: string;
	manifestSha256?: string;
	gitHead?: string;
	gitDiffSha256?: string;
	args?: string;
}

interface SubagentsService extends SubagentsRecordService {
	spawn(type: string, prompt: string, options?: {
		description?: string;
		model?: string;
		maxTurns?: number;
		thinkingLevel?: string;
		inheritContext?: boolean;
		foreground?: boolean;
		bypassQueue?: boolean;
	}): string;
}

const RUN_ENTRY = "manifest-dev:run";
const VERIFICATION_ENTRY = "manifest-dev:verification";
const OUTCOME_ENTRY = "manifest-dev:outcome";
const SUBAGENTS_PACKAGE = "@gotgenes/pi-subagents";

const DEFAULT_VERIFIER_AGENT = "general-purpose";
const DEFAULT_VERIFIER_MAX_TURNS = 1000;
const DEFAULT_VERIFIER_TIMEOUT_MS = 30 * 60 * 1000;
const FLAG_MAX_TURNS = "manifest-verifier-max-turns";
const FLAG_AGENT = "manifest-verifier-agent";
const FLAG_TIMEOUT_MS = "manifest-verifier-timeout-ms";

interface VerifierConfig {
	agent: string;
	maxTurns: number;
	timeoutMs: number;
}

export default function manifestDevExtension(pi: ExtensionAPI): void {
	const latestVerificationByRunId = new Map<string, VerificationRecord>();

	pi.registerFlag(FLAG_MAX_TURNS, {
		description: `Max turns per manifest-dev verifier subagent (default ${DEFAULT_VERIFIER_MAX_TURNS}).`,
		type: "string",
	});
	pi.registerFlag(FLAG_AGENT, {
		description: `Default subagent type for manifest-dev verifiers when a gate omits verify.agent (default ${DEFAULT_VERIFIER_AGENT}).`,
		type: "string",
	});
	pi.registerFlag(FLAG_TIMEOUT_MS, {
		description: `Timeout in ms to wait for manifest-dev verifier subagents (default ${DEFAULT_VERIFIER_TIMEOUT_MS}).`,
		type: "string",
	});

	pi.registerTool(defineTool({
		name: "manifest_dev_request_verification",
		label: "Manifest-dev Verification",
		description:
			"Run the manifest-dev Harness-level verification fanout. Call this when implementation is believed ready; it parses the manifest, spawns clean verifier subagent sessions per Acceptance Criterion and Global Invariant, aggregates PASS / FAIL / BLOCKED verdicts, and reports whether the executor should finish, repair, or escalate.",
		promptSnippet:
			"Request manifest-dev verification before reporting done. Verification launches clean subagent sessions for every manifest gate.",
		promptGuidelines: [
			"Call manifest_dev_request_verification when a Harness-level Do implementation attempt is ready for independent verification.",
			"Do not call manifest_dev_report_outcome with outcome=done until this tool returns an all-PASS report for the same run id.",
			"If this tool returns FAIL, repair the failed gates and call this tool again.",
			"If this tool returns BLOCKED, call manifest_dev_report_outcome with outcome=escalate only when the blockers require human input, access, external state, or another unrecoverable decision.",
		],
		parameters: Type.Object({
			runId: Type.String({
				description: "Run id emitted by /manifest-do, /manifest-auto, or /manifest-babysit-pr.",
			}),
			manifestPath: Type.String({
				description: "Path to the manifest that contains Acceptance Criteria and Global Invariant verify.prompt blocks.",
			}),
			implementationSummary: Type.Optional(Type.String({
				description: "Concise summary of what changed before verification.",
			})),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
			const requestedAt = new Date().toISOString();
			const runId = params.runId.trim();
			if (!runId) {
				return {
					content: [{ type: "text", text: "Verification requires a non-empty runId." }],
					details: { error: "missing_run_id", requestedAt },
				};
			}

			const manifestPath = resolve(ctx.cwd, unquote(params.manifestPath));
			if (!existsSync(manifestPath)) {
				return {
					content: [{
						type: "text",
						text: `Verification blocked: manifest not found at ${manifestPath}.`,
					}],
					details: { error: "manifest_not_found", manifestPath, requestedAt },
				};
			}

			const manifest = readFileSync(manifestPath, "utf-8");
			const gates = extractManifestGates(manifest);
			if (gates.length === 0) {
				const record = makeBlockedVerificationRecord({
					runId,
					manifestPath,
					manifest,
					cwd: ctx.cwd,
					requestedAt,
					implementationSummary: params.implementationSummary,
					blocker: "No Acceptance Criteria or Global Invariants with verify.prompt blocks were found in the manifest.",
				});
				latestVerificationByRunId.set(runId, record);
				pi.appendEntry(VERIFICATION_ENTRY, record);
				return verificationToolResponse(record);
			}

			const subagents = await getSubagentsService();
			if (!subagents) {
				const record = makeBlockedVerificationRecord({
					runId,
					manifestPath,
					manifest,
					cwd: ctx.cwd,
					requestedAt,
					implementationSummary: params.implementationSummary,
					blocker:
						`Pi subagents service is unavailable. Install and enable it with: pi install npm:${SUBAGENTS_PACKAGE}`,
				});
				latestVerificationByRunId.set(runId, record);
				pi.appendEntry(VERIFICATION_ENTRY, record);
				return verificationToolResponse(record);
			}

			const config = resolveVerifierConfig(pi);
			const reposMap = extractReposMap(manifest);
			const batches = planVerifierBatches(gates);
			const results: GateVerificationResult[] = [];

			for (const batch of batches) {
				const spawnedInBatch: Array<{
					gate: ManifestGate;
					agentId: string;
					requestedType: string;
					usedType: string;
					fellBack: boolean;
				}> = [];

				for (const gate of batch) {
					const prompt = buildGateVerifierPrompt({
						gate,
						manifestPath,
						manifest,
						runId,
						implementationSummary: params.implementationSummary,
						reposMap,
					});
					const verifierModel = resolveVerifierModel(gate.model, ctx.model);
					const spawnOptions = {
						description: `${gate.id}: ${gate.title}`.slice(0, 120),
						inheritContext: false,
						foreground: false,
						maxTurns: config.maxTurns,
						...(verifierModel ? { model: verifierModel } : {}),
					};
					const requestedType = gate.suggestedAgent?.trim() || config.agent;

					try {
						const agentId = subagents.spawn(requestedType, prompt, spawnOptions);
						spawnedInBatch.push({ gate, agentId, requestedType, usedType: requestedType, fellBack: false });
					} catch (error) {
						if (requestedType !== config.agent) {
							try {
								const agentId = subagents.spawn(config.agent, prompt, spawnOptions);
								spawnedInBatch.push({ gate, agentId, requestedType, usedType: config.agent, fellBack: true });
								continue;
							} catch (fallbackError) {
								results.push(spawnBlockedResult(gate, requestedType, fallbackError));
								continue;
							}
						}
						results.push(spawnBlockedResult(gate, requestedType, error));
					}
				}

				if (spawnedInBatch.length > 0) {
					const records = await waitForVerifierRecords(
						subagents,
						spawnedInBatch.map((item) => item.agentId),
						{ timeoutMs: config.timeoutMs },
					);
					for (const item of spawnedInBatch) {
						const result = toGateVerificationResult(item.gate, item.agentId, records.get(item.agentId));
						results.push(
							item.fellBack
								? {
									...result,
									evidence: `[verifier agent "${item.requestedType}" unavailable; fell back to "${item.usedType}"] ${result.evidence}`,
								}
							: result,
						);
					}
				}

				// Phase short-circuit: a FAIL/BLOCKED in this phase stops later phases from running.
				if (results.some((result) => result.verdict !== "PASS")) break;
			}

			const verification: VerificationRecord = {
				runId,
				manifestPath,
				manifestSha256: sha256(manifest),
				requestedAt,
				completedAt: new Date().toISOString(),
				cwd: ctx.cwd,
				status: aggregateVerificationStatus(results),
				implementationSummary: params.implementationSummary,
				results,
				workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
			};

			latestVerificationByRunId.set(runId, verification);
			writeRunStateFile(verification);
			pi.appendEntry(VERIFICATION_ENTRY, verification);
			ctx.ui.notify(
				verification.status === "passed"
					? `Manifest-dev verification passed for ${runId}.`
					: `Manifest-dev verification ${verification.status} for ${runId}.`,
				verification.status === "passed" ? "info" : "warning",
			);

			return verificationToolResponse(verification);
		},
	}));

	pi.registerTool(defineTool({
		name: "manifest_dev_report_outcome",
		label: "Manifest-dev Outcome",
		description:
			"Report the final manifest-dev Harness-level Do outcome. Use outcome=done only after manifest_dev_request_verification returns all PASS for this run id. Use outcome=escalate when the run is blocked by an external precondition or unrecoverable blocker.",
		promptSnippet:
			"Report final manifest-dev Do state with outcome=done or outcome=escalate; completion and escalation are runtime outcomes, not prose.",
		promptGuidelines: [
			"Call manifest_dev_report_outcome exactly once when a manifest-dev Harness-level Do run reaches a final state.",
			"Use outcome=done only after manifest_dev_request_verification returns an all-PASS report for the same run id.",
			"Use outcome=escalate when the remaining blocker needs human input, access, external state, or a decision the agent cannot safely make.",
			"Do not call this tool for progress updates, plans, or partial implementation.",
		],
		parameters: Type.Object({
			runId: Type.String({
				description: "Run id emitted by /manifest-do, /manifest-auto, or /manifest-babysit-pr.",
			}),
			outcome: Type.Union([
				Type.Literal("done"),
				Type.Literal("escalate"),
			], {
				description: "Final Harness-level Do outcome.",
			}),
			summary: Type.String({
				description: "Concise summary of what was completed or why the run escalated.",
			}),
			verified: Type.Optional(Type.Array(Type.String({
				description: "Acceptance criteria, invariants, tests, or checks that passed.",
			}))),
			blockers: Type.Optional(Type.Array(Type.String({
				description: "Blocking facts. Required for outcome=escalate.",
			}))),
			nextSteps: Type.Optional(Type.Array(Type.String({
				description: "Human or future-agent actions needed after escalation.",
			}))),
		}),
		async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
			const reportedAt = new Date().toISOString();
			const blockers = params.blockers ?? [];
			const nextSteps = params.nextSteps ?? [];
			const outcome = params.outcome as ManifestOutcome;
			const runId = params.runId.trim();

			if (!runId) {
				return {
					content: [{ type: "text", text: "Outcome reporting requires a non-empty runId." }],
					details: { error: "missing_run_id", reportedAt },
				};
			}

			let latestVerification = latestVerificationByRunId.get(runId);
			if (!latestVerification) {
				latestVerification = readRunStateFile(runId);
				if (latestVerification) latestVerificationByRunId.set(runId, latestVerification);
			}

			if (outcome === "done") {
				const currentManifestSha256 = latestVerification && existsSync(latestVerification.manifestPath)
					? sha256(readFileSync(latestVerification.manifestPath, "utf-8"))
					: undefined;
				const readiness = evaluateDoneReadiness({
					verification: latestVerification,
					currentManifestSha256,
					currentWorkspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
				});
				if (!readiness.ready) {
					return {
						content: [{
							type: "text",
							text:
								`Done is blocked for ${runId}: ${readiness.reason}. Call manifest_dev_request_verification, repair any FAIL results, and only report done after all gates PASS for the current manifest and workspace.`,
						}],
						details: {
							error: "verification_required",
							runId,
							reason: readiness.reason,
							latestVerification,
							reportedAt,
						},
					};
				}
			}

			if (outcome === "escalate" && blockers.length === 0) {
				return {
					content: [{
						type: "text",
						text: "Escalation requires at least one blocker in blockers[].",
					}],
					details: { error: "missing_blockers", reportedAt },
				};
			}

			const verified = params.verified?.length
				? params.verified
				: latestVerification?.results.map((result) => result.gateId) ?? [];
			const record = {
				...params,
				runId,
				blockers,
				nextSteps,
				verified,
				verification: latestVerification,
				reportedAt,
				cwd: ctx.cwd,
			};
			pi.appendEntry(OUTCOME_ENTRY, record);
			ctx.ui.notify(
				outcome === "done"
					? "Manifest-dev run reported done."
					: "Manifest-dev run reported escalation.",
				outcome === "done" ? "info" : "warning",
			);

			return {
				content: [{
					type: "text",
					text: outcome === "done"
						? `Manifest-dev done: ${params.summary}`
						: `Manifest-dev escalation (run remains resumable): ${params.summary}`,
				}],
				details: record,
				...(shouldTerminateOutcome(outcome) ? { terminate: true } : {}),
			};
		},
	}));

	pi.registerCommand("manifest-do", {
		description: "Run manifest-dev Harness-level Do for a manifest path.",
		handler: async (rawArgs, ctx) => {
			await startManifestDo(pi, rawArgs, ctx);
		},
	});

	pi.registerCommand("manifest-auto", {
		description: "Run manifest-dev figure-out -> define -> Harness-level Do autonomously for a task.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "manifest-auto", rawArgs, ctx);
		},
	});

	pi.registerCommand("manifest-babysit-pr", {
		description: "Synthesize a PR lifecycle manifest and run Harness-level Do for a GitHub PR.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "manifest-babysit-pr", rawArgs, ctx);
		},
	});
}

async function startManifestDo(
	pi: ExtensionAPI,
	rawArgs: string,
	ctx: ExtensionCommandContext,
): Promise<void> {
	const manifestPath = resolveManifestPath(rawArgs, ctx.cwd);
	if (!manifestPath) {
		ctx.ui.notify("Usage: /manifest-do <manifest-path>", "warning");
		return;
	}
	if (!existsSync(manifestPath)) {
		ctx.ui.notify(`Manifest not found: ${manifestPath}`, "error");
		return;
	}

	const manifest = readFileSync(manifestPath, "utf-8");
	const run = makeRunRecord("manifest-do", ctx, {
		manifestPath,
		manifestSha256: sha256(manifest),
	});
	pi.appendEntry(RUN_ENTRY, run);
	pi.setSessionName(`manifest-dev ${shortId(run.runId)}`);

	await sendPrompt(pi, ctx, buildManifestDoPrompt(run, manifest));
	ctx.ui.notify(`Started manifest-dev Harness-level Do: ${manifestPath}`, "info");
}

async function startWrapper(
	pi: ExtensionAPI,
	command: Extract<ManifestCommand, "manifest-auto" | "manifest-babysit-pr">,
	rawArgs: string,
	ctx: ExtensionCommandContext,
): Promise<void> {
	const args = rawArgs.trim();
	if (!args) {
		const usage = command === "manifest-auto"
			? "Usage: /manifest-auto <task>"
			: "Usage: /manifest-babysit-pr <github-pr-url>";
		ctx.ui.notify(usage, "warning");
		return;
	}
	if (command === "manifest-babysit-pr" && !isGithubPr(args)) {
		ctx.ui.notify(
			"Cannot babysit: provide a GitHub PR URL such as https://github.com/owner/repo/pull/123.",
			"warning",
		);
		return;
	}

	const run = makeRunRecord(command, ctx, { args });
	pi.appendEntry(RUN_ENTRY, run);
	pi.setSessionName(`${command} ${shortId(run.runId)}`);

	const prompt = command === "manifest-auto"
		? buildManifestAutoPrompt(run, args)
		: buildManifestBabysitPrompt(run, args);
	await sendPrompt(pi, ctx, prompt);
	ctx.ui.notify(`Started ${command} run ${run.runId}.`, "info");
}

async function sendPrompt(
	pi: ExtensionAPI,
	ctx: ExtensionCommandContext,
	prompt: string,
): Promise<void> {
	try {
		const queued = ctx.isIdle()
			? pi.sendUserMessage(prompt)
			: pi.sendUserMessage(prompt, { deliverAs: "followUp" });
		await Promise.resolve(queued);
	} catch (error) {
		ctx.ui.notify(`Could not start manifest-dev run: ${formatError(error)}`, "error");
	}
}

function makeRunRecord(
	command: ManifestCommand,
	ctx: ExtensionCommandContext,
	extra: Partial<RunRecord>,
): RunRecord {
	const startedAt = new Date().toISOString();
	const basis = `${command}:${ctx.cwd}:${startedAt}:${extra.manifestPath ?? extra.args ?? ""}`;
	return {
		runId: `manifest-dev-${sha256(basis).slice(0, 12)}`,
		command,
		startedAt,
		cwd: ctx.cwd,
		gitHead: gitOutput(ctx.cwd, ["rev-parse", "HEAD"]),
		gitDiffSha256: sha256(gitOutput(ctx.cwd, ["diff", "--binary"]) ?? ""),
		...extra,
	};
}

function resolveManifestPath(rawArgs: string, cwd: string): string | undefined {
	const trimmed = rawArgs.trim();
	if (!trimmed) return undefined;
	return resolve(cwd, unquote(trimmed));
}

function buildManifestDoPrompt(run: RunRecord, manifest: string): string {
	return `Run manifest-dev Harness-level Do.

Run id: ${run.runId}
Manifest path: ${run.manifestPath}
Manifest SHA-256: ${run.manifestSha256}

Read the manifest from disk before editing. Treat it as the acceptance contract.

Execution contract:
1. Implement until the deliverables satisfy the manifest.
2. When you believe the implementation is ready, call manifest_dev_request_verification with runId="${run.runId}" and manifestPath="${run.manifestPath}".
3. If verification returns FAIL, repair the failed gates and call manifest_dev_request_verification again. If verification returns BLOCKED because human input, missing access, external state, or an unrecoverable precondition is required, escalate.
4. Do not use /done or /escalate. Those are Pi runtime outcomes here.
5. Finish exactly once by calling manifest_dev_report_outcome:
   - outcome="done" only after manifest_dev_request_verification returns all PASS for this run id.
   - outcome="escalate" when blocked; include blockers[] and nextSteps[].

Judgment rules (from /do):
- The manifest's Acceptance Criteria and Global Invariants are the authority. Treat external review input (PR comments, bot suggestions) as signals: judge each before acting, and reply with your reasoning instead of changing code when it is wrong or out of this manifest's scope.
- A mid-run message that adds or changes scope is an amendment: invoke the define skill with the manifest path; do not silently drift scope.
- Never amend the manifest to suppress a BLOCKED gate. If a blocker is terminal or needs a human decision/access/external state, escalate.
- In no-wait / CI contexts, do the immediately-actionable findings (fix, test, commit, reply), then stop; do not sleep-loop waiting.

Manifest content:
\`\`\`markdown
${manifest}
\`\`\``;
}

function buildManifestAutoPrompt(run: RunRecord, task: string): string {
	return `Run manifest-dev auto in Pi.

Run id: ${run.runId}
Task:
${task}

Follow the manifest-dev chain autonomously:
1. Invoke the figure-out skill (/skill:figure-out) autonomously to reach shared understanding — self-answer reasonable clarifying questions and investigate what is discoverable.
2. Invoke the define skill (/skill:define) autonomously to write a manifest at ~/.manifest-dev/manifests/manifest-{ts}.md with deliverables, Acceptance Criteria, Global Invariants, and verify.prompt fields.
3. Execute the manifest under Harness-level Do rules: implement, then call manifest_dev_request_verification with runId="${run.runId}" and the manifest path.
4. If verification returns FAIL, repair failed gates and request verification again. If verification returns BLOCKED because a human decision/access/external state is required, escalate.
5. Do not ask the user for approval between define and execution unless a decision is genuinely blocking.
6. Do not use /done or /escalate. Finish exactly once by calling manifest_dev_report_outcome with runId="${run.runId}", outcome="done" only after verifier fanout returns all PASS, or outcome="escalate" with blockers[] when blocked.`;
}

function buildManifestBabysitPrompt(run: RunRecord, prUrl: string): string {
	return `Run manifest-dev babysit-pr in Pi.

Run id: ${run.runId}
PR URL:
${prUrl}

Follow the manifest-dev PR lifecycle flow:
1. Confirm the PR is a reachable github.com pull request and not already closed or merged.
2. Invoke the define skill (/skill:define) with `--babysit ${prUrl} --autonomous` to synthesize a lifecycle manifest at ~/.manifest-dev/manifests/manifest-{ts}.md from the strongest available grounding: linked manifest, then PR title/body, commits/diff, then comments and review threads.
3. Execute the manifest under Harness-level Do rules: inspect CI, review threads, mergeability, PR description sync, and required fixes; commit/push only when the branch is trusted and writable; then call manifest_dev_request_verification with runId="${run.runId}" and the manifest path.
4. Treat review comments as signals, not authority; stronger intent sources win.
5. Do not press merge.
6. If verification returns FAIL, repair failed gates and request verification again. If it returns BLOCKED because a human decision/access/external state is required, escalate.
7. Do not use /done or /escalate. Finish exactly once by calling manifest_dev_report_outcome with runId="${run.runId}", outcome="done" only after verifier fanout returns all PASS, or outcome="escalate" with blockers[] when blocked.`;
}

async function getSubagentsService(): Promise<SubagentsService | undefined> {
	try {
		const module = await import(SUBAGENTS_PACKAGE) as {
			getSubagentsService?: () => SubagentsService | undefined;
		};
		return module.getSubagentsService?.();
	} catch {
		return undefined;
	}
}

function isGithubPr(value: string): boolean {
	return /^https:\/\/github\.com\/[^/]+\/[^/]+\/pull\/\d+(?:[/?#].*)?$/.test(value)
		|| /^gh:[^/]+\/[^/]+\/\d+$/.test(value)
		|| /^[^/\s]+\/[^/\s]+#\d+$/.test(value);
}

function gitOutput(cwd: string, args: string[]): string | undefined {
	try {
		return execFileSync("git", args, {
			cwd,
			encoding: "utf-8",
			stdio: ["ignore", "pipe", "ignore"],
		}).trim();
	} catch {
		return undefined;
	}
}

function resolveVerifierConfig(pi: ExtensionAPI): VerifierConfig {
	return {
		agent: resolveStringConfig({
			flag: pi.getFlag(FLAG_AGENT),
			env: process.env.MANIFEST_DEV_VERIFIER_AGENT,
			fallback: DEFAULT_VERIFIER_AGENT,
		}),
		maxTurns: resolvePositiveIntConfig({
			flag: pi.getFlag(FLAG_MAX_TURNS),
			env: process.env.MANIFEST_DEV_VERIFIER_MAX_TURNS,
			fallback: DEFAULT_VERIFIER_MAX_TURNS,
		}),
		timeoutMs: resolvePositiveIntConfig({
			flag: pi.getFlag(FLAG_TIMEOUT_MS),
			env: process.env.MANIFEST_DEV_VERIFIER_TIMEOUT_MS,
			fallback: DEFAULT_VERIFIER_TIMEOUT_MS,
		}),
	};
}

function spawnBlockedResult(gate: ManifestGate, requestedType: string, error: unknown): GateVerificationResult {
	return {
		gateId: gate.id,
		kind: gate.kind,
		title: gate.title,
		verdict: "BLOCKED",
		evidence: `Could not spawn verifier subagent (type "${requestedType}").`,
		details: formatError(error),
		error: "spawn_failed",
	};
}

function runStateDir(): string {
	return resolve(homedir(), ".manifest-dev", "runs");
}

function writeRunStateFile(verification: VerificationRecord): void {
	try {
		mkdirSync(runStateDir(), { recursive: true });
		writeFileSync(
			join(runStateDir(), runStateFileName(verification.runId)),
			JSON.stringify(verification, null, 2),
			"utf-8",
		);
	} catch {
		// Best-effort: in-memory state still gates done within this session.
	}
}

function readRunStateFile(runId: string): VerificationRecord | undefined {
	try {
		const file = join(runStateDir(), runStateFileName(runId));
		if (!existsSync(file)) return undefined;
		return parseRunState(readFileSync(file, "utf-8"));
	} catch {
		return undefined;
	}
}

function workspaceDiffSha256(cwd: string): string {
	return sha256(gitOutput(cwd, ["diff", "--binary"]) ?? "");
}

function shortId(runId: string): string {
	return runId.replace(/^manifest-dev-/, "").slice(0, 8);
}

function formatError(error: unknown): string {
	return error instanceof Error ? error.message : String(error);
}
