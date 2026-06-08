import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { resolve } from "node:path";
import type { ExtensionAPI, ExtensionCommandContext, ExtensionContext } from "@earendil-works/pi-coding-agent";
import {
	aggregateVerificationStatus,
	buildGateVerifierPrompt,
	chunkManifestGates,
	evaluateDoneReadiness,
	extractManifestGates,
	extractReposMap,
	makeBlockedVerificationRecord,
	planVerifierBatches,
	resolvePositiveIntConfig,
	resolveVerifierModel,
	sha256,
	shouldStopAfterBatch,
	shouldTerminateOutcome,
	toGateVerificationResult,
	unquote,
	waitForVerifierRecords,
	writeRunStateFile,
	type GateVerificationResult,
	type ManifestGate,
	type SubagentsRecordService,
	type VerificationRecord,
} from "./manifest-dev-runtime.ts";

type ManifestOutcome = "done" | "escalate";
export type ManifestCommand = "do" | "auto" | "babysit-pr";
type RunStatus = "executing" | "repairing" | "verifying" | "blocked" | "done";

export interface RunRecord {
	runId: string;
	command: ManifestCommand;
	startedAt: string;
	cwd: string;
	executorSessionId: string;
	status: RunStatus;
	manifestPath?: string;
	manifestSha256?: string;
	gitHead?: string;
	gitDiffSha256?: string;
	args?: string;
	verificationAttempts?: number;
	lastVerificationStatus?: VerificationRecord["status"];
	/** /babysit-pr --ci: do every actionable lifecycle step, then exit pending on waits rather than looping repair. */
	ciOneShot?: boolean;
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
const STATUS_ENTRY = "manifest-dev:status";
// Marker a check-pr verifier emits when a gate FAILs only because it is waiting on an
// external actor/time (reviewer pending, CI in progress) rather than a fixable defect.
// In --ci one-shot mode the runtime routes such failures to a pending exit, not repair.
const WAIT_PENDING_MARKER = "WAIT-PENDING";
const SUBAGENTS_PACKAGE = "@gotgenes/pi-subagents";

// Verifiers always run as a general-purpose subagent that loads whatever skill
// the gate's verify.prompt names — there is no per-gate or configurable verifier
// agent selection.
const VERIFIER_AGENT_TYPE = "general-purpose";
const DEFAULT_VERIFIER_MAX_TURNS = 1000;
const DEFAULT_VERIFIER_TIMEOUT_MS = 30 * 60 * 1000;
const DEFAULT_VERIFIER_MAX_CONCURRENT = 24;
const FLAG_MAX_TURNS = "manifest-verifier-max-turns";
const FLAG_TIMEOUT_MS = "manifest-verifier-timeout-ms";
const FLAG_MAX_CONCURRENT = "manifest-verifier-max-concurrent";
const HARNESS_TOOL_NAMES = new Set([
	"manifest_dev_request_verification",
	"manifest_dev_report_outcome",
]);

interface VerifierConfig {
	maxTurns: number;
	timeoutMs: number;
	maxConcurrent: number;
}

export interface RuntimeState {
	latestVerificationByRunId: Map<string, VerificationRecord>;
	activeRunByExecutorSessionId: Map<string, RunRecord>;
	childSessionIds: Set<string>;
}

/** Commands owned by the core (`@doodledood/manifest-dev-pi`) package. */
export const CORE_COMMANDS: ReadonlySet<ManifestCommand> = new Set<ManifestCommand>(["do", "auto"]);

export function createRuntimeState(): RuntimeState {
	return {
		latestVerificationByRunId: new Map<string, VerificationRecord>(),
		activeRunByExecutorSessionId: new Map<string, RunRecord>(),
		childSessionIds: new Set<string>(),
	};
}

/**
 * Register the verifier launch flags. Only the CORE extension calls this. The tools
 * extension is loaded only from the repo-root `pi.extensions` (it has no standalone
 * `pi.extensions` of its own), so core is always present to own the flags and there is
 * no second load path that needs its own registration — hence no de-dup marker. The
 * tools runtime reads the parsed values via resolveVerifierConfig's process.argv
 * fallback, since Pi's getFlag is per-extension.
 */
export function registerVerifierFlags(pi: ExtensionAPI): void {
	pi.registerFlag(FLAG_MAX_TURNS, {
		description: `Max turns per manifest-dev verifier subagent (default ${DEFAULT_VERIFIER_MAX_TURNS}).`,
		type: "string",
	});
	pi.registerFlag(FLAG_TIMEOUT_MS, {
		description: `Timeout in ms to wait for manifest-dev verifier subagents (default ${DEFAULT_VERIFIER_TIMEOUT_MS}).`,
		type: "string",
	});
	pi.registerFlag(FLAG_MAX_CONCURRENT, {
		description: `Max manifest-dev verifier subagents to run in parallel per phase (default ${DEFAULT_VERIFIER_MAX_CONCURRENT}).`,
		type: "string",
	});
}

/**
 * Wire the shared Harness-level Do runtime (subagent tracking, verification on
 * executor checkpoints, repair routing) onto `state`. `ownedCommands` scopes
 * which persisted runs this instance rehydrates, so the core and tools packages
 * can each run their own runtime without double-verifying each other's runs.
 */
export function wireRuntimeHooks(
	pi: ExtensionAPI,
	state: RuntimeState,
	ownedCommands: ReadonlySet<ManifestCommand>,
): void {
	pi.events.on("subagents:child:session-created", (event: unknown) => {
		const sessionId = typeof event === "object" && event !== null && "sessionId" in event
			? String((event as { sessionId: unknown }).sessionId)
			: "";
		if (sessionId) state.childSessionIds.add(sessionId);
	});
	pi.events.on("subagents:child:disposed", (event: unknown) => {
		const sessionId = typeof event === "object" && event !== null && "sessionId" in event
			? String((event as { sessionId: unknown }).sessionId)
			: "";
		if (sessionId) state.childSessionIds.delete(sessionId);
	});

	pi.on("session_start", (_event, ctx) => {
		rehydrateRuntimeState(ctx, state, ownedCommands);
	});

	pi.on("before_agent_start", (_event, ctx) => {
		if (!state.activeRunByExecutorSessionId.has(ctx.sessionManager.getSessionId())) return;
		hideHarnessToolsFromExecutor(pi);
	});

	pi.on("agent_end", async (_event, ctx) => {
		await maybeRunHarnessVerification(pi, ctx, state);
	});
}

export default function manifestDevExtension(pi: ExtensionAPI): void {
	const state = createRuntimeState();
	registerVerifierFlags(pi);
	wireRuntimeHooks(pi, state, CORE_COMMANDS);

	pi.registerCommand("do", {
		description: "Run manifest-dev Harness-level Do for a manifest path.",
		handler: async (rawArgs, ctx) => {
			await startManifestDo(pi, rawArgs, ctx, state);
		},
	});

	pi.registerCommand("auto", {
		description: "Run manifest-dev figure-out -> define -> Harness-level Do autonomously for a task.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "auto", rawArgs, ctx, state);
		},
	});
}

export async function startManifestDo(
	pi: ExtensionAPI,
	rawArgs: string,
	ctx: ExtensionCommandContext,
	state: RuntimeState,
): Promise<void> {
	const manifestPath = resolveManifestPath(rawArgs, ctx.cwd);
	if (!manifestPath) {
		ctx.ui.notify("Usage: /do <manifest-path>", "warning");
		return;
	}
	if (!existsSync(manifestPath)) {
		ctx.ui.notify(`Manifest not found: ${manifestPath}`, "error");
		return;
	}

	const manifest = readFileSync(manifestPath, "utf-8");
	const run = makeRunRecord("do", ctx, {
		manifestPath,
		manifestSha256: sha256(manifest),
	});
	registerRun(pi, state, run);
	pi.setSessionName(`manifest-dev ${shortId(run.runId)}`);
	hideHarnessToolsFromExecutor(pi);

	await sendPrompt(pi, ctx, buildManifestDoPrompt(run, manifest));
	ctx.ui.notify(`Started manifest-dev Harness-level Do: ${manifestPath}`, "info");
}

export async function startWrapper(
	pi: ExtensionAPI,
	command: Extract<ManifestCommand, "auto" | "babysit-pr">,
	rawArgs: string,
	ctx: ExtensionCommandContext,
	state: RuntimeState,
): Promise<void> {
	const args = rawArgs.trim();
	if (!args) {
		const usage = command === "auto"
			? "Usage: /auto <task>"
			: "Usage: /babysit-pr <github-pr-url> [--ci] [--manifest <path>]";
		ctx.ui.notify(usage, "warning");
		return;
	}
	let babysitPrUrl: string | undefined;
	let babysitManifest: string | undefined;
	let ciOneShot = false;
	if (command === "babysit-pr") {
		// Accept the URL anywhere in the args so documented flags (--ci, --manifest <path>)
		// don't fail validation; the URL is the only required positional.
		const tokens = args.split(/\s+/);
		babysitPrUrl = tokens.find(isGithubPr);
		if (!babysitPrUrl) {
			ctx.ui.notify(
				"Cannot babysit: include a GitHub PR URL such as https://github.com/owner/repo/pull/123 (flags like --ci or --manifest <path> may accompany it).",
				"warning",
			);
			return;
		}
		const manifestFlagIndex = tokens.indexOf("--manifest");
		babysitManifest = manifestFlagIndex >= 0 ? tokens[manifestFlagIndex + 1] : undefined;
		ciOneShot = tokens.includes("--ci");
	}

	const plannedManifestPath = makePlannedManifestPath(command);
	// When --manifest <path> is supplied for babysit, the run is grounded in that
	// existing manifest — point run.manifestPath at it so runtime verification
	// reads the real file instead of the never-written planned path.
	const manifestPath = babysitManifest
		? resolveInputPath(babysitManifest, ctx.cwd)
		: plannedManifestPath;
	const run = makeRunRecord(command, ctx, { args, manifestPath, ...(ciOneShot ? { ciOneShot: true } : {}) });
	registerRun(pi, state, run);
	pi.setSessionName(`${command} ${shortId(run.runId)}`);
	hideHarnessToolsFromExecutor(pi);

	const prompt = command === "auto"
		? buildManifestAutoPrompt(run, args)
		: buildManifestBabysitPrompt(run, babysitPrUrl as string, args);
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

function registerRun(pi: ExtensionAPI, state: RuntimeState, run: RunRecord): void {
	state.activeRunByExecutorSessionId.set(run.executorSessionId, run);
	pi.appendEntry(RUN_ENTRY, run);
}

function updateRun(pi: ExtensionAPI, state: RuntimeState, run: RunRecord, updates: Partial<RunRecord>): RunRecord {
	const next = { ...run, ...updates };
	state.activeRunByExecutorSessionId.set(next.executorSessionId, next);
	pi.appendEntry(RUN_ENTRY, next);
	return next;
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
		executorSessionId: ctx.sessionManager.getSessionId(),
		status: "executing",
		verificationAttempts: 0,
		gitHead: gitOutput(ctx.cwd, ["rev-parse", "HEAD"]),
		gitDiffSha256: sha256(gitOutput(ctx.cwd, ["diff", "--binary"]) ?? ""),
		...extra,
	};
}

export function resolveManifestPath(rawArgs: string, cwd: string): string | undefined {
	const trimmed = rawArgs.trim();
	if (!trimmed) return undefined;
	return resolveInputPath(trimmed, cwd);
}

function resolveInputPath(rawValue: string, cwd: string): string {
	const value = unquote(rawValue.trim());
	if (value === "~") return homedir();
	if (value.startsWith("~/")) return resolve(homedir(), value.slice(2));
	return resolve(cwd, value);
}

export function buildManifestDoPrompt(run: RunRecord, manifest: string): string {
	return `Run manifest-dev Harness-level Do implementation.

Run id: ${run.runId}
Manifest path: ${run.manifestPath}
Manifest SHA-256: ${run.manifestSha256}

Read the manifest from disk before editing. Treat it as the acceptance contract.

Execution contract:
1. Implement the Manifest Deliverables until they appear satisfied.
2. Run useful local checks/tests while implementing. These checks are implementation aids, not final harness verification.
3. If the runtime injects a Harness verification report with failed Acceptance Criteria or Global Invariants, repair those concrete failures.
4. Stop when no known implementation or repair work remains. The Pi runtime owns authoritative verification, done, and escalation.

Judgment rules:
- The Manifest's Acceptance Criteria and Global Invariants are the authority.
- A mid-run user message that adds or changes scope is an amendment request: invoke the define skill with the manifest path instead of silently drifting scope.
- Never amend the manifest just to suppress a failing or blocked gate.
- If you are blocked by missing access, a required human decision, or unavailable external state, state the blocker plainly and stop.

Manifest content:
\`\`\`markdown
${manifest}
\`\`\``;
}

export function buildManifestAutoPrompt(run: RunRecord, task: string): string {
	return `Run manifest-dev auto in Pi.

Run id: ${run.runId}
Manifest path to create: ${run.manifestPath}
Task:
${task}

Follow the manifest-dev chain autonomously:
1. Invoke the figure-out skill (/skill:figure-out) autonomously to reach shared understanding — self-answer reasonable clarifying questions and investigate what is discoverable.
2. Invoke the define skill (/skill:define) autonomously to write the manifest exactly at: ${run.manifestPath}
3. Execute that manifest under the simplified Harness-level Do implementation contract: implement Deliverables, run useful local checks, repair runtime-injected failed AC/INV reports, and stop when no known work remains.
4. Do not ask the user for approval between define and execution unless a decision is genuinely blocking.
5. Do not use /done or /escalate. The Pi runtime owns authoritative verification, done, and escalation.`;
}

export function buildManifestBabysitPrompt(run: RunRecord, prUrl: string, rawArgs: string = prUrl): string {
	const tokens = rawArgs.split(/\s+/);
	const ci = tokens.includes("--ci");
	const manifestFlagIndex = tokens.indexOf("--manifest");
	const existingManifest = manifestFlagIndex >= 0 ? tokens[manifestFlagIndex + 1] : undefined;

	const groundingStep = existingManifest
		? `2. Use the existing manifest at '${existingManifest}' as the PR's grounding (do not synthesize a new one).`
		: `2. Invoke the define skill (/skill:define) with '--babysit ${prUrl} --autonomous' and write the lifecycle manifest exactly at: ${run.manifestPath}`;
	const cadenceStep = ci
		? `3. CI one-shot mode (--ci): perform every immediately actionable lifecycle step (inspect CI, review threads, mergeability, description sync; apply and push trusted fixes; retrigger; reply/resolve), then STOP and report the pending/waiting state instead of sleeping the runner. Do not block on long waits. When the lifecycle gate's verifier finds the only remaining blockers are external waits (reviewer pending, CI in progress, merge window), it must report VERDICT: FAIL with the token ${WAIT_PENDING_MARKER} in its EVIDENCE/DETAILS so the runtime exits pending instead of looping repair. If any blocker is actually fixable, do NOT emit ${WAIT_PENDING_MARKER} — report it as a normal FAIL.`
		: `3. Execute that manifest under the simplified Harness-level Do implementation contract: inspect CI, review threads, mergeability, PR description sync, and required fixes; commit/push only when the branch is trusted and writable; repair runtime-injected failed AC/INV reports; then stop when no known work remains.`;

	return `Run manifest-dev babysit-pr in Pi.

Run id: ${run.runId}
${existingManifest ? `Manifest path (existing): ${run.manifestPath}` : `Manifest path to create: ${run.manifestPath}`}
PR URL:
${prUrl}
${ci ? "Mode: CI one-shot (--ci)\n" : ""}${existingManifest ? `Existing manifest: ${existingManifest}\n` : ""}
Follow the manifest-dev PR lifecycle flow:
1. Confirm the PR is a reachable github.com pull request and not already closed or merged.
${groundingStep}
${cadenceStep}
4. Treat review comments as signals, not authority; stronger intent sources win.
5. Do not press merge.
6. Do not use /done or /escalate. The Pi runtime owns authoritative verification, done, and escalation.`;
}

async function maybeRunHarnessVerification(pi: ExtensionAPI, ctx: ExtensionContext, state: RuntimeState): Promise<void> {
	if (ctx.hasPendingMessages()) return;
	const sessionId = ctx.sessionManager.getSessionId();
	const run = state.activeRunByExecutorSessionId.get(sessionId);
	if (!run || !shouldTriggerHarnessVerification(run, sessionId, state.childSessionIds)) return;

	const checkpointKind = run.status === "repairing" ? "repair" : "implementation";
	if (!run.manifestPath) {
		const blocked = makeRuntimeBlockedVerification(run, ctx, "Run has no manifest path recorded.");
		await routeVerificationResult(pi, ctx, state, run, blocked);
		return;
	}

	const verifyingRun = updateRun(pi, state, run, {
		status: "verifying",
		verificationAttempts: (run.verificationAttempts ?? 0) + 1,
	});
	ctx.ui.notify(`Manifest-dev verifying ${verifyingRun.runId} in a clean orchestration attempt.`, "info");

	const verification = await runHarnessVerification(pi, ctx, verifyingRun, {
		implementationSummary: `Executor session ${verifyingRun.executorSessionId} stopped after ${checkpointKind}.`,
	});
	await routeVerificationResult(pi, ctx, state, verifyingRun, verification);
}

export function shouldTriggerHarnessVerification(
	run: RunRecord | undefined,
	sessionId: string,
	childSessionIds: ReadonlySet<string> = new Set(),
): boolean {
	if (!run) return false;
	if (childSessionIds.has(sessionId)) return false;
	if (run.executorSessionId !== sessionId) return false;
	return run.status === "executing" || run.status === "repairing";
}

async function runHarnessVerification(
	pi: ExtensionAPI,
	ctx: ExtensionContext,
	run: RunRecord,
	params: { implementationSummary?: string } = {},
): Promise<VerificationRecord> {
	const requestedAt = new Date().toISOString();
	const manifestPath = resolveRunManifestPath(run, ctx.cwd);
	const orchestrator = createVerificationOrchestratorSession(ctx, run, requestedAt);

	if (!manifestPath || !existsSync(manifestPath)) {
		return makeBlockedVerificationRecord({
			runId: run.runId,
			manifestPath: manifestPath ?? "",
			manifest: "",
			cwd: ctx.cwd,
			requestedAt,
			implementationSummary: params.implementationSummary,
			blocker: `Manifest not found at ${manifestPath ?? "<missing>"}.`,
			orchestratorSessionId: orchestrator.id,
			orchestratorSessionFile: orchestrator.file,
			workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
		});
	}

	const manifest = readFileSync(manifestPath, "utf-8");
	const gates = extractManifestGates(manifest);
	if (gates.length === 0) {
		return makeBlockedVerificationRecord({
			runId: run.runId,
			manifestPath,
			manifest,
			cwd: ctx.cwd,
			requestedAt,
			implementationSummary: params.implementationSummary,
			blocker: "No Acceptance Criteria or Global Invariants with verify.prompt blocks were found in the manifest.",
			orchestratorSessionId: orchestrator.id,
			orchestratorSessionFile: orchestrator.file,
			workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
		});
	}

	const subagents = await getSubagentsService();
	if (!subagents) {
		return makeBlockedVerificationRecord({
			runId: run.runId,
			manifestPath,
			manifest,
			cwd: ctx.cwd,
			requestedAt,
			implementationSummary: params.implementationSummary,
			blocker: `Pi subagents service is unavailable. Install and enable it with: pi install npm:${SUBAGENTS_PACKAGE}`,
			orchestratorSessionId: orchestrator.id,
			orchestratorSessionFile: orchestrator.file,
			workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
		});
	}

	const config = resolveVerifierConfig(pi);
	const reposMap = extractReposMap(manifest);
	const batches = planVerifierBatches(gates);
	const results: GateVerificationResult[] = [];
	let totalSpawned = 0;

	for (const batch of batches) {
		const phaseResultStart = results.length;

		for (const chunk of chunkManifestGates(batch, config.maxConcurrent)) {
			const spawnedInChunk: Array<{
				gate: ManifestGate;
				agentId: string;
			}> = [];

			for (const gate of chunk) {
				const prompt = buildGateVerifierPrompt({
					gate,
					manifestPath,
					manifest,
					runId: run.runId,
					implementationSummary: params.implementationSummary,
					reposMap,
					orchestratorSessionId: orchestrator.id,
					orchestratorSessionFile: orchestrator.file,
				});
				const verifierModel = resolveVerifierModel(gate.model, ctx.model);
				const spawnOptions = {
					description: `${gate.id}: ${gate.title}`.slice(0, 120),
					inheritContext: false,
					foreground: false,
					bypassQueue: true,
					maxTurns: config.maxTurns,
					...(verifierModel ? { model: verifierModel } : {}),
				};

				const spawn = spawnVerifier(subagents, VERIFIER_AGENT_TYPE, prompt, spawnOptions);
				if (spawn.ok) {
					totalSpawned += 1;
					spawnedInChunk.push({ gate, agentId: spawn.agentId });
				} else if (totalSpawned === 0) {
					// No verifier has spawned at all — treat this as a systemic harness
					// orchestration failure (e.g. a stale Pi session context at the
					// checkpoint) and report ONE clear blocker, instead of an identical
					// BLOCKED on every gate that never actually ran.
					return makeBlockedVerificationRecord({
						runId: run.runId,
						manifestPath,
						manifest,
						cwd: ctx.cwd,
						requestedAt,
						implementationSummary: params.implementationSummary,
						blocker: buildOrchestrationSpawnBlocker(run, ctx.sessionManager.getSessionId(), spawn.error),
						orchestratorSessionId: orchestrator.id,
						orchestratorSessionFile: orchestrator.file,
						workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
					});
				} else {
					// Some verifiers already spawned, so spawning works in general; keep a
					// per-gate blocker for this one rather than failing the whole attempt.
					results.push(spawnBlockedResult(gate, VERIFIER_AGENT_TYPE, spawn.error));
				}
			}

			if (spawnedInChunk.length > 0) {
				const records = await waitForVerifierRecords(
					subagents,
					spawnedInChunk.map((item) => item.agentId),
					{ timeoutMs: config.timeoutMs },
				);
				for (const item of spawnedInChunk) {
					results.push(toGateVerificationResult(item.gate, item.agentId, records.get(item.agentId)));
				}
			}
		}

		if (shouldStopAfterBatch(results.slice(phaseResultStart))) break;
	}

	return {
		runId: run.runId,
		manifestPath,
		manifestSha256: sha256(manifest),
		requestedAt,
		completedAt: new Date().toISOString(),
		cwd: ctx.cwd,
		status: aggregateVerificationStatus(results),
		implementationSummary: params.implementationSummary,
		orchestratorSessionId: orchestrator.id,
		orchestratorSessionFile: orchestrator.file,
		attempt: run.verificationAttempts ?? 1,
		results,
		workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
	};
}

export async function routeVerificationResult(
	pi: ExtensionAPI,
	ctx: ExtensionContext,
	state: RuntimeState,
	run: RunRecord,
	verification: VerificationRecord,
): Promise<void> {
	state.latestVerificationByRunId.set(run.runId, verification);
	writeRunStateFile(verification, runStateDir());
	pi.appendEntry(VERIFICATION_ENTRY, verification);
	ctx.ui.notify(
		verification.status === "passed"
			? `Manifest-dev verification passed for ${run.runId}.`
			: `Manifest-dev verification ${verification.status} for ${run.runId}.`,
		verification.status === "passed" ? "info" : "warning",
	);

	// CI one-shot: a failure that is only waiting on external actors/time is not a
	// repairable defect. Exit pending (resumable) instead of injecting repair, so the
	// runner is not looped on a wait. Mixed (wait + real) failures fall through to repair.
	if (verification.status === "failed" && run.ciOneShot && isWaitPendingFailure(verification)) {
		const pendingRun = updateRun(pi, state, run, {
			status: "blocked",
			lastVerificationStatus: verification.status,
		});
		const summary = buildCiPendingSummary(verification);
		const outcome = buildOutcomeRecord(pendingRun, "escalate", {
			summary: "CI one-shot pending on external wait.",
			blockers: verification.results.filter((r) => r.verdict === "FAIL").map((r) => `${r.gateId}: ${r.evidence || r.details}`),
			nextSteps: ["Re-run /babysit-pr --ci once the external wait clears."],
			verification,
			cwd: ctx.cwd,
		});
		pi.appendEntry(OUTCOME_ENTRY, outcome);
		pi.sendMessage({
			customType: STATUS_ENTRY,
			content: summary,
			display: true,
			details: outcome,
		}, { triggerTurn: false });
		return;
	}

	if (verification.status === "failed") {
		const nextRun = updateRun(pi, state, run, {
			status: "repairing",
			lastVerificationStatus: verification.status,
		});
		void nextRun;
		pi.sendUserMessage(formatRepairFollowUpMessage(verification), { deliverAs: "followUp" });
		return;
	}

	if (verification.status === "blocked") {
		const blockedRun = updateRun(pi, state, run, {
			status: "blocked",
			lastVerificationStatus: verification.status,
		});
		const blockers = verification.results
			.filter((result) => result.verdict === "BLOCKED")
			.map((result) => `${result.gateId}: ${result.evidence || result.details}`);
		const outcome = buildOutcomeRecord(blockedRun, "escalate", {
			summary: "Harness verification is blocked.",
			blockers,
			nextSteps: blockers,
			verification,
			cwd: ctx.cwd,
		});
		pi.appendEntry(OUTCOME_ENTRY, outcome);
		pi.sendMessage({
			customType: STATUS_ENTRY,
			content: `Manifest-dev verification is blocked for ${run.runId}.\n\n${blockers.join("\n")}`,
			display: true,
			details: outcome,
		}, { triggerTurn: false });
		return;
	}

	const currentManifestSha256 = verification.manifestPath && existsSync(verification.manifestPath)
		? sha256(readFileSync(verification.manifestPath, "utf-8"))
		: undefined;
	const readiness = evaluateDoneReadiness({
		verification,
		currentManifestSha256,
		currentWorkspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
	});
	if (!readiness.ready) {
		const staleRun = updateRun(pi, state, run, {
			status: "repairing",
			lastVerificationStatus: "failed",
		});
		void staleRun;
		pi.sendUserMessage(
			`Harness verification became stale before done could be recorded: ${readiness.reason}. Re-read the manifest/workspace, repair any resulting drift, and stop when ready for runtime verification again.`,
			{ deliverAs: "followUp" },
		);
		return;
	}

	const doneRun = updateRun(pi, state, run, {
		status: "done",
		lastVerificationStatus: verification.status,
	});
	const outcome = buildOutcomeRecord(doneRun, "done", {
		summary: "All manifest gates passed harness verification.",
		verified: verification.results.map((result) => result.gateId),
		verification,
		cwd: ctx.cwd,
	});
	pi.appendEntry(OUTCOME_ENTRY, outcome);
	pi.sendMessage({
		customType: STATUS_ENTRY,
		content: `Manifest-dev done for ${run.runId}: all manifest gates passed harness verification.`,
		display: true,
		details: outcome,
	}, { triggerTurn: false });
}

function makeRuntimeBlockedVerification(run: RunRecord | undefined, ctx: ExtensionContext, blocker: string): VerificationRecord {
	const manifest = run?.manifestPath && existsSync(run.manifestPath) ? readFileSync(run.manifestPath, "utf-8") : "";
	return makeBlockedVerificationRecord({
		runId: run?.runId ?? "manifest-dev-unknown",
		manifestPath: run?.manifestPath ?? "",
		manifest,
		cwd: ctx.cwd,
		requestedAt: new Date().toISOString(),
		blocker,
		orchestratorSessionId: run ? makeOrchestratorSessionId(run, new Date().toISOString()) : "manifest-verify-missing-run",
		workspaceDiffSha256: workspaceDiffSha256(ctx.cwd),
	});
}

function buildOutcomeRecord(
	run: RunRecord,
	outcome: ManifestOutcome,
	args: {
		summary: string;
		verification?: VerificationRecord;
		verified?: string[];
		blockers?: string[];
		nextSteps?: string[];
		cwd: string;
	},
) {
	const blockers = args.blockers ?? [];
	const nextSteps = args.nextSteps ?? [];
	return {
		runId: run.runId,
		outcome,
		summary: args.summary,
		verified: args.verified ?? args.verification?.results.map((result) => result.gateId) ?? [],
		blockers,
		nextSteps,
		verification: args.verification,
		reportedAt: new Date().toISOString(),
		cwd: args.cwd,
		terminate: shouldTerminateOutcome(outcome),
	};
}

export function formatRepairFollowUpMessage(verification: VerificationRecord): string {
	const failed = verification.results.filter((result) => result.verdict === "FAIL");
	const lines = [
		"Harness verification found failed Acceptance Criteria / Global Invariants.",
		"",
		"Repair the failed gates below. Do not run or invoke the harness verification protocol yourself; stop when the repair work is complete and the runtime will verify again from a clean session.",
		"",
		`Run id: ${verification.runId}`,
		`Verification orchestrator session: ${verification.orchestratorSessionId ?? "unknown"}${verification.orchestratorSessionFile ? ` (${verification.orchestratorSessionFile})` : ""}`,
		"",
	];
	for (const result of failed) {
		lines.push(`- ${result.gateId} ${result.title}: ${result.evidence || "No evidence reported."}`);
		if (result.details) lines.push(`  Details: ${singleLine(result.details)}`);
	}
	return lines.join("\n");
}

export function rehydrateRuntimeState(
	ctx: ExtensionContext,
	state: RuntimeState,
	ownedCommands?: ReadonlySet<ManifestCommand>,
): void {
	for (const entry of ctx.sessionManager.getBranch()) {
		if (entry.type !== "custom") continue;
		if (entry.customType === RUN_ENTRY && isRunRecord(entry.data)) {
			if (ownedCommands && !ownedCommands.has(entry.data.command)) continue;
			if (entry.data.status === "done" || entry.data.status === "blocked") {
				state.activeRunByExecutorSessionId.delete(entry.data.executorSessionId);
			} else {
				state.activeRunByExecutorSessionId.set(entry.data.executorSessionId, entry.data);
			}
		}
		if (entry.customType === VERIFICATION_ENTRY && isVerificationRecord(entry.data)) {
			state.latestVerificationByRunId.set(entry.data.runId, entry.data);
		}
	}
}

function isRunRecord(value: unknown): value is RunRecord {
	return typeof value === "object"
		&& value !== null
		&& typeof (value as { runId?: unknown }).runId === "string"
		&& typeof (value as { executorSessionId?: unknown }).executorSessionId === "string"
		&& typeof (value as { status?: unknown }).status === "string";
}

function isVerificationRecord(value: unknown): value is VerificationRecord {
	return typeof value === "object"
		&& value !== null
		&& typeof (value as { runId?: unknown }).runId === "string"
		&& typeof (value as { status?: unknown }).status === "string"
		&& Array.isArray((value as { results?: unknown }).results);
}

function hideHarnessToolsFromExecutor(pi: ExtensionAPI): void {
	const active = pi.getActiveTools();
	const filtered = active.filter((toolName) => !HARNESS_TOOL_NAMES.has(toolName));
	if (filtered.length !== active.length) pi.setActiveTools(filtered);
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

/**
 * Read a Pi launch flag straight from process.argv. The verifier flags are
 * process-global launch flags, so this is shared across module instances (unlike
 * per-extension getFlag). Supports `--name value` and `--name=value`.
 */
export function launchFlagFromArgv(name: string, argv: readonly string[] = process.argv): string | undefined {
	const long = `--${name}`;
	for (let i = 0; i < argv.length; i++) {
		const arg = argv[i];
		if (arg === long) return argv[i + 1];
		if (arg.startsWith(`${long}=`)) return arg.slice(long.length + 1);
	}
	return undefined;
}

/**
 * Read a verifier flag value, preferring the calling extension's own getFlag and
 * falling back to process.argv. Pi's getFlag only returns values for flags the
 * calling extension registered; in the repo-root install the tools extension does
 * not own the flags (core does), so it recovers the parsed launch value from argv.
 */
function readVerifierFlag(pi: ExtensionAPI, name: string): string | undefined {
	const own = pi.getFlag?.(name);
	if (own !== undefined && own !== null) return own as string;
	return launchFlagFromArgv(name);
}

function resolveVerifierConfig(pi: ExtensionAPI): VerifierConfig {
	return {
		maxTurns: resolvePositiveIntConfig({
			flag: readVerifierFlag(pi, FLAG_MAX_TURNS),
			env: process.env.MANIFEST_DEV_VERIFIER_MAX_TURNS,
			fallback: DEFAULT_VERIFIER_MAX_TURNS,
		}),
		timeoutMs: resolvePositiveIntConfig({
			flag: readVerifierFlag(pi, FLAG_TIMEOUT_MS),
			env: process.env.MANIFEST_DEV_VERIFIER_TIMEOUT_MS,
			fallback: DEFAULT_VERIFIER_TIMEOUT_MS,
		}),
		maxConcurrent: resolvePositiveIntConfig({
			flag: readVerifierFlag(pi, FLAG_MAX_CONCURRENT),
			env: process.env.MANIFEST_DEV_VERIFIER_MAX_CONCURRENT,
			fallback: DEFAULT_VERIFIER_MAX_CONCURRENT,
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

/**
 * Spawn one verifier subagent. Returns the agentId or the thrown error. spawn() is
 * synchronous and returns the agentId immediately (@gotgenes/pi-subagents
 * service-adapter.ts), so a thrown attempt creates no child to leak. We do NOT retry:
 * the subagents service reads its stored `currentCtx` (captured at session_start) when
 * building the parent snapshot, and that reference is only refreshed by another
 * session lifecycle event — never within a microtask — so an immediate re-spawn would
 * read the same stale ctx and throw identically. A spawn failure is surfaced instead.
 */
export function spawnVerifier(
	subagents: Pick<SubagentsService, "spawn">,
	type: string,
	prompt: string,
	options: Parameters<SubagentsService["spawn"]>[2],
): { ok: true; agentId: string } | { ok: false; error: unknown } {
	try {
		return { ok: true, agentId: subagents.spawn(type, prompt, options) };
	} catch (error) {
		return { ok: false, error };
	}
}

/**
 * True if `error` is Pi's stale-extension-context guard (loader.js/runner.js
 * `invalidate`), which the subagents service surfaces through `spawn` when its stored
 * session context was invalidated by a session replacement/reload before the
 * verifier checkpoint.
 */
export function isStaleSessionContextError(error: unknown): boolean {
	return /stale after session replacement or reload/i.test(formatError(error));
}

/**
 * Blocker text for a systemic verifier-spawn failure: no verifier ran, so this is a
 * harness/runtime orchestration failure rather than a gate or implementation failure.
 * Names the underlying error and the session ids so a stale-context spawn failure is
 * diagnosable instead of being reported as an identical BLOCKED on every gate.
 */
export function buildOrchestrationSpawnBlocker(run: RunRecord, currentSessionId: string, error: unknown): string {
	const lines = [
		"Verifier subagents could not be spawned, so no Acceptance Criterion or Global Invariant was verified.",
		"This is a harness/runtime orchestration failure (verifier spawn), not an implementation or gate failure.",
		`Underlying spawn error: ${formatError(error)}`,
		`Diagnostics: current session ${currentSessionId}, executor session ${run.executorSessionId}.`,
	];
	if (isStaleSessionContextError(error)) {
		lines.push(
			"Cause: the Pi subagents service's stored session context was invalidated (session replacement/reload) before this checkpoint. Re-run verification from a fresh session so the service re-captures a live context.",
		);
	}
	return lines.join("\n");
}

/**
 * True if a failed verification is wait-only: every FAIL gate carries the check-pr
 * WAIT-PENDING marker (waiting on a reviewer/CI/time, not a fixable defect). Used only
 * in --ci one-shot mode to exit pending instead of looping repair. A mix of wait and
 * real failures is not wait-only — repair still runs.
 */
export function isWaitPendingFailure(verification: VerificationRecord): boolean {
	const failures = verification.results.filter((result) => result.verdict === "FAIL");
	if (failures.length === 0) return false;
	return failures.every((result) =>
		`${result.evidence ?? ""}\n${result.details ?? ""}`.includes(WAIT_PENDING_MARKER),
	);
}

/** Pending-exit summary for a --ci one-shot run blocked only on external waits. */
export function buildCiPendingSummary(verification: VerificationRecord): string {
	const waits = verification.results
		.filter((result) => result.verdict === "FAIL")
		.map((result) => `${result.gateId}: ${result.evidence || result.details}`);
	return [
		"CI one-shot (--ci): every immediately actionable lifecycle step is done; the PR is now waiting on external actors/time (reviewer, CI, merge window).",
		"Exiting pending instead of looping repair. Re-run /babysit-pr --ci to resume once the wait clears.",
		"",
		...waits,
	].join("\n");
}

function runStateDir(): string {
	return resolve(homedir(), ".manifest-dev", "runs");
}

function verificationSessionDir(): string {
	return resolve(homedir(), ".manifest-dev", "verification-sessions");
}

function workspaceDiffSha256(cwd: string): string {
	return sha256(gitOutput(cwd, ["diff", "--binary"]) ?? "");
}

function shortId(runId: string): string {
	return runId.replace(/^manifest-dev-/, "").slice(0, 8);
}

function makePlannedManifestPath(command: ManifestCommand): string {
	const suffix = command === "auto" ? "auto" : "babysit-pr";
	return resolve(homedir(), ".manifest-dev", "manifests", `manifest-${new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z")}-${suffix}.md`);
}

function resolveRunManifestPath(run: RunRecord, cwd: string): string | undefined {
	return run.manifestPath ? resolveInputPath(run.manifestPath, cwd) : undefined;
}

export function createVerificationOrchestratorSession(ctx: ExtensionContext, run: RunRecord, requestedAt: string): { id: string; file?: string } {
	const id = makeOrchestratorSessionId(run, requestedAt);
	const sessionDir = verificationSessionDir();
	const timestamp = requestedAt.replace(/[:.]/g, "-");
	const file = resolve(sessionDir, `${timestamp}_${id}.jsonl`);
	const customMessageId = `msg-${sha256(`${id}:custom-message`).slice(0, 12)}`;
	const details = { runId: run.runId, executorSessionId: run.executorSessionId, requestedAt };
	const entries = [
		{ type: "session", version: 1, id, timestamp: requestedAt, cwd: ctx.cwd },
		{
			type: "custom_message",
			id: customMessageId,
			parentId: null,
			timestamp: requestedAt,
			customType: "manifest-dev:verification-orchestrator",
			content: `Clean Harness-level verification attempt for ${run.runId}. Executor session ${run.executorSessionId} is intentionally not inherited.`,
			display: true,
			details,
		},
	];
	try {
		mkdirSync(sessionDir, { recursive: true });
		writeFileSync(file, entries.map((entry) => JSON.stringify(entry)).join("\n") + "\n", "utf-8");
		return { id, file };
	} catch {
		return { id };
	}
}

export function makeOrchestratorSessionId(run: RunRecord, requestedAt: string): string {
	const attempt = run.verificationAttempts ?? 1;
	return `manifest-verify-${sha256(`${run.runId}:${attempt}:${requestedAt}`).slice(0, 12)}`;
}

function singleLine(value: string): string {
	return value.replace(/\s+/g, " ").trim();
}

function formatError(error: unknown): string {
	return error instanceof Error ? error.message : String(error);
}
