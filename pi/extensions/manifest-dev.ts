import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { defineTool, type ExtensionAPI, type ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

type ManifestOutcome = "done" | "escalate";
type ManifestCommand = "manifest-do" | "manifest-auto" | "manifest-babysit-pr";
type VerificationStatus = "passed" | "failed" | "blocked";
type GateVerdict = "PASS" | "FAIL" | "BLOCKED";
type GateKind = "acceptance_criterion" | "global_invariant";

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

interface ManifestGate {
	id: string;
	kind: GateKind;
	title: string;
	verifyPrompt: string;
	suggestedAgent?: string;
}

interface GateVerificationResult {
	gateId: string;
	kind: GateKind;
	title: string;
	agentId?: string;
	agentStatus?: string;
	verdict: GateVerdict;
	evidence: string;
	details: string;
	rawResult?: string;
	error?: string;
}

interface VerificationRecord {
	runId: string;
	manifestPath: string;
	manifestSha256: string;
	requestedAt: string;
	completedAt: string;
	cwd: string;
	status: VerificationStatus;
	implementationSummary?: string;
	results: GateVerificationResult[];
}

interface SubagentRecord {
	id: string;
	type: string;
	description: string;
	status: string;
	result?: string;
	error?: string;
}

interface SubagentsService {
	spawn(type: string, prompt: string, options?: {
		description?: string;
		model?: string;
		maxTurns?: number;
		thinkingLevel?: string;
		inheritContext?: boolean;
		foreground?: boolean;
		bypassQueue?: boolean;
	}): string;
	getRecord(id: string): SubagentRecord | undefined;
}

const RUN_ENTRY = "manifest-dev:run";
const VERIFICATION_ENTRY = "manifest-dev:verification";
const OUTCOME_ENTRY = "manifest-dev:outcome";
const SUBAGENTS_PACKAGE = "@gotgenes/pi-subagents";
const VERIFIER_AGENT_TYPE = "Explore";

export default function manifestDevExtension(pi: ExtensionAPI): void {
	const latestVerificationByRunId = new Map<string, VerificationRecord>();

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

			let spawned: Array<{ gate: ManifestGate; agentId: string }>;
			try {
				spawned = gates.map((gate) => {
					const agentId = subagents.spawn(
						VERIFIER_AGENT_TYPE,
						buildGateVerifierPrompt({
							gate,
							manifestPath,
							manifest,
							runId,
							implementationSummary: params.implementationSummary,
						}),
						{
							description: `${gate.id}: ${gate.title}`.slice(0, 120),
							inheritContext: false,
							foreground: false,
							maxTurns: 20,
						},
					);
					return { gate, agentId };
				});
			} catch (error) {
				const record = makeBlockedVerificationRecord({
					runId,
					manifestPath,
					manifest,
					cwd: ctx.cwd,
					requestedAt,
					implementationSummary: params.implementationSummary,
					blocker: `Could not spawn verifier subagents through ${SUBAGENTS_PACKAGE}: ${formatError(error)}`,
				});
				latestVerificationByRunId.set(runId, record);
				pi.appendEntry(VERIFICATION_ENTRY, record);
				return verificationToolResponse(record);
			}

			const records = await waitForVerifierRecords(subagents, spawned.map((item) => item.agentId));
			const results = spawned.map(({ gate, agentId }) => {
				const record = records.get(agentId);
				return toGateVerificationResult(gate, agentId, record);
			});
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
			};

			latestVerificationByRunId.set(runId, verification);
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

			const latestVerification = latestVerificationByRunId.get(runId);
			if (outcome === "done" && latestVerification?.status !== "passed") {
				const reason = latestVerification
					? `latest verification is ${latestVerification.status}`
					: "no verification report exists";
				return {
					content: [{
						type: "text",
						text:
							`Done is blocked for ${runId}: ${reason}. Call manifest_dev_request_verification, repair any FAIL results, and only report done after all gates PASS.`,
					}],
					details: {
						error: "verification_required",
						runId,
						latestVerification,
						reportedAt,
					},
				};
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
						: `Manifest-dev escalation: ${params.summary}`,
				}],
				details: record,
				terminate: true,
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
1. Figure out the task enough to act. Self-answer reasonable clarifying questions and investigate what is discoverable.
2. Define a manifest at ~/.manifest-dev/manifests/manifest-{ts}.md. Include deliverables, Acceptance Criteria, Global Invariants, and verify.prompt fields.
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
2. Synthesize a lifecycle manifest at ~/.manifest-dev/manifests/manifest-{ts}.md using strongest available grounding: linked manifest, then PR title/body, commits/diff, then comments and review threads.
3. Execute the manifest under Harness-level Do rules: inspect CI, review threads, mergeability, PR description sync, and required fixes; commit/push only when the branch is trusted and writable; then call manifest_dev_request_verification with runId="${run.runId}" and the manifest path.
4. Treat review comments as signals, not authority; stronger intent sources win.
5. Do not press merge.
6. If verification returns FAIL, repair failed gates and request verification again. If it returns BLOCKED because a human decision/access/external state is required, escalate.
7. Do not use /done or /escalate. Finish exactly once by calling manifest_dev_report_outcome with runId="${run.runId}", outcome="done" only after verifier fanout returns all PASS, or outcome="escalate" with blockers[] when blocked.`;
}

function extractManifestGates(manifest: string): ManifestGate[] {
	const gateMatches = [...manifest.matchAll(/^\s*-\s+\[(AC-\d+(?:\.\d+)+|INV-G\d+)\]\s*(.+?)\s*$/gm)];
	return gateMatches.flatMap((match, index) => {
		const id = match[1];
		const title = match[2].trim();
		const start = match.index ?? 0;
		const end = gateMatches[index + 1]?.index ?? manifest.length;
		const block = manifest.slice(start, end);
		const verifyPrompt = extractYamlValue(block, "prompt");
		if (!verifyPrompt) return [];
		return [{
			id,
			title,
			kind: id.startsWith("INV-") ? "global_invariant" : "acceptance_criterion",
			verifyPrompt,
			suggestedAgent: extractYamlValue(block, "agent"),
		} satisfies ManifestGate];
	});
}

function extractYamlValue(block: string, key: string): string | undefined {
	const quoted = block.match(new RegExp(`^\\s*${key}:\\s*"((?:\\\\.|[^"\\\\])*)"\\s*$`, "m"));
	if (quoted) return unescapeQuotedYaml(quoted[1]);

	const singleQuoted = block.match(new RegExp(`^\\s*${key}:\\s*'((?:''|[^'])*)'\\s*$`, "m"));
	if (singleQuoted) return singleQuoted[1].replaceAll("''", "'");

	const inline = block.match(new RegExp(`^\\s*${key}:\\s*([^\\n]+?)\\s*$`, "m"));
	if (inline && !inline[1].startsWith("|") && !inline[1].startsWith(">")) {
		return inline[1].trim();
	}

	const blockScalar = block.match(new RegExp(`^\\s*${key}:\\s*[|>]\\s*\\n((?:\\s{4,}.+\\n?)+)`, "m"));
	if (!blockScalar) return undefined;
	return blockScalar[1]
		.split("\n")
		.map((line) => line.replace(/^\s{4}/, ""))
		.join("\n")
		.trim();
}

function unescapeQuotedYaml(value: string): string {
	try {
		return JSON.parse(`"${value}"`) as string;
	} catch {
		return value.replace(/\\"/g, '"');
	}
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

function buildGateVerifierPrompt(args: {
	gate: ManifestGate;
	manifestPath: string;
	manifest: string;
	runId: string;
	implementationSummary?: string;
}): string {
	const suggestedAgent = args.gate.suggestedAgent
		? `\nSuggested manifest verifier persona: ${args.gate.suggestedAgent}`
		: "";
	const implementationSummary = args.implementationSummary
		? `\nImplementation summary from executor:\n${args.implementationSummary}\n`
		: "";

	return `You are a manifest-dev verifier running in a clean Pi subagent session.

Verify exactly one manifest gate. Do not implement fixes. Inspect the workspace, run focused commands when useful, and judge only the assigned gate.

Run id: ${args.runId}
Manifest path: ${args.manifestPath}
Gate: ${args.gate.id} ${args.gate.title}
Gate kind: ${args.gate.kind}${suggestedAgent}
${implementationSummary}
Verification prompt:
${args.gate.verifyPrompt}

Return exactly this report shape:
VERDICT: PASS|FAIL|BLOCKED
EVIDENCE: concise concrete evidence, including commands/files inspected
DETAILS: what passed, what failed, or what external blocker prevents judgment

Verdict rules:
- PASS only when the gate is satisfied with concrete evidence.
- FAIL when the implementation can be repaired in the workspace.
- BLOCKED only for missing access, human decision, unavailable external service, or verifier runtime/tooling inability.

Manifest content:
\`\`\`markdown
${args.manifest}
\`\`\``;
}

async function waitForVerifierRecords(
	subagents: SubagentsService,
	agentIds: string[],
): Promise<Map<string, SubagentRecord | undefined>> {
	const deadline = Date.now() + 30 * 60 * 1000;
	while (Date.now() < deadline) {
		const records = new Map(agentIds.map((agentId) => [agentId, subagents.getRecord(agentId)]));
		const stillRunning = [...records.values()].some((record) => (
			!record || record.status === "queued" || record.status === "running"
		));
		if (!stillRunning) return records;
		await delay(1000);
	}

	return new Map(agentIds.map((agentId) => [agentId, subagents.getRecord(agentId)]));
}

function toGateVerificationResult(
	gate: ManifestGate,
	agentId: string,
	record: SubagentRecord | undefined,
): GateVerificationResult {
	if (!record) {
		return {
			gateId: gate.id,
			kind: gate.kind,
			title: gate.title,
			agentId,
			verdict: "BLOCKED",
			evidence: "Verifier subagent record disappeared before aggregation.",
			details: "Runtime could not retrieve the verifier result.",
			error: "missing_subagent_record",
		};
	}

	if (record.status !== "completed") {
		return {
			gateId: gate.id,
			kind: gate.kind,
			title: gate.title,
			agentId,
			agentStatus: record.status,
			verdict: "BLOCKED",
			evidence: `Verifier subagent ended with status=${record.status}.`,
			details: record.error ?? "Verifier did not complete cleanly.",
			rawResult: record.result,
			error: record.error,
		};
	}

	const parsed = parseVerifierReport(record.result ?? "");
	if (!parsed) {
		return {
			gateId: gate.id,
			kind: gate.kind,
			title: gate.title,
			agentId,
			agentStatus: record.status,
			verdict: "BLOCKED",
			evidence: "Verifier completed but did not emit a parseable VERDICT line.",
			details: "Expected report lines: VERDICT, EVIDENCE, DETAILS.",
			rawResult: record.result,
		};
	}

	return {
		gateId: gate.id,
		kind: gate.kind,
		title: gate.title,
		agentId,
		agentStatus: record.status,
		...parsed,
		rawResult: record.result,
	};
}

function parseVerifierReport(result: string): Pick<GateVerificationResult, "verdict" | "evidence" | "details"> | undefined {
	const verdict = result.match(/^\s*VERDICT:\s*(PASS|FAIL|BLOCKED)\b/im)?.[1] as GateVerdict | undefined;
	if (!verdict) return undefined;
	const evidence = result.match(/^\s*EVIDENCE:\s*(.+?)\s*$/im)?.[1]?.trim() ?? "";
	const details = result.match(/^\s*DETAILS:\s*([\s\S]*)$/im)?.[1]?.trim() ?? "";
	return {
		verdict,
		evidence,
		details,
	};
}

function aggregateVerificationStatus(results: GateVerificationResult[]): VerificationStatus {
	if (results.some((result) => result.verdict === "BLOCKED")) return "blocked";
	if (results.some((result) => result.verdict === "FAIL")) return "failed";
	return "passed";
}

function makeBlockedVerificationRecord(args: {
	runId: string;
	manifestPath: string;
	manifest: string;
	cwd: string;
	requestedAt: string;
	implementationSummary?: string;
	blocker: string;
}): VerificationRecord {
	return {
		runId: args.runId,
		manifestPath: args.manifestPath,
		manifestSha256: sha256(args.manifest),
		requestedAt: args.requestedAt,
		completedAt: new Date().toISOString(),
		cwd: args.cwd,
		status: "blocked",
		implementationSummary: args.implementationSummary,
		results: [{
			gateId: "manifest",
			kind: "global_invariant",
			title: "Verifier runtime precondition",
			verdict: "BLOCKED",
			evidence: args.blocker,
			details: args.blocker,
		}],
	};
}

function verificationToolResponse(record: VerificationRecord) {
	const summary = record.results
		.map((result) => `${result.gateId}: ${result.verdict} - ${firstLine(result.evidence || result.details)}`)
		.join("\n");
	const instruction = record.status === "passed"
		? "All manifest gates PASS. You may now call manifest_dev_report_outcome with outcome=\"done\" for this run id."
		: record.status === "failed"
			? "Some manifest gates FAIL. Repair the failed gates, then call manifest_dev_request_verification again with the same run id."
			: "Verification is BLOCKED. If the blocker requires human input, access, external state, or an unrecoverable decision, call manifest_dev_report_outcome with outcome=\"escalate\" and include blockers[].";

	return {
		content: [{
			type: "text",
			text: `Manifest-dev verification ${record.status.toUpperCase()} for ${record.runId}.\n\n${summary}\n\n${instruction}`,
		}],
		details: record,
	};
}

function firstLine(value: string): string {
	return value.split("\n")[0]?.trim() || "No evidence reported.";
}

function delay(ms: number): Promise<void> {
	return new Promise((resolveDelay) => setTimeout(resolveDelay, ms));
}

function unquote(value: string): string {
	if (
		(value.startsWith('"') && value.endsWith('"'))
		|| (value.startsWith("'") && value.endsWith("'"))
	) {
		return value.slice(1, -1);
	}
	return value;
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

function sha256(value: string): string {
	return createHash("sha256").update(value).digest("hex");
}

function shortId(runId: string): string {
	return runId.replace(/^manifest-dev-/, "").slice(0, 8);
}

function formatError(error: unknown): string {
	return error instanceof Error ? error.message : String(error);
}
