import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { defineTool, type ExtensionAPI, type ExtensionCommandContext } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";

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

const RUN_ENTRY = "manifest-dev:run";
const OUTCOME_ENTRY = "manifest-dev:outcome";

export default function manifestDevExtension(pi: ExtensionAPI): void {
	pi.registerTool(defineTool({
		name: "manifest_dev_report_outcome",
		label: "Manifest-dev Outcome",
		description:
			"Report the final manifest-dev Harness-level Do outcome. Use outcome=done only after every manifest acceptance criterion and invariant verifies PASS. Use outcome=escalate when the run is blocked by an external precondition or unrecoverable blocker.",
		promptSnippet:
			"Report final manifest-dev Do state with outcome=done or outcome=escalate; completion and escalation are runtime outcomes, not prose.",
		promptGuidelines: [
			"Call manifest_dev_report_outcome exactly once when a manifest-dev Harness-level Do run reaches a final state.",
			"Use outcome=done only after every Acceptance Criterion and Global Invariant has concrete PASS evidence.",
			"Use outcome=escalate when the remaining blocker needs human input, access, external state, or a decision the agent cannot safely make.",
			"Do not call this tool for progress updates, plans, or partial implementation.",
		],
		parameters: Type.Object({
			runId: Type.Optional(Type.String({
				description: "Run id emitted by /manifest-do, /manifest-auto, or /manifest-babysit-pr when available.",
			})),
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
			const verified = params.verified ?? [];
			const outcome = params.outcome as ManifestOutcome;

			if (outcome === "escalate" && blockers.length === 0) {
				return {
					content: [{
						type: "text",
						text: "Escalation requires at least one blocker in blockers[].",
					}],
					details: { error: "missing_blockers", reportedAt },
				};
			}

			const record = {
				...params,
				blockers,
				nextSteps,
				verified,
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
2. Verify every Acceptance Criterion and Global Invariant using its verify.prompt. Prefer automated checks and concrete file/tool evidence.
3. If any gate fails, repair and re-verify. If a gate is blocked by human input, missing access, external state, or an unrecoverable precondition, escalate.
4. Do not use /done or /escalate. Those are Pi runtime outcomes here.
5. Finish exactly once by calling manifest_dev_report_outcome:
   - outcome="done" only after every AC and invariant verifies PASS.
   - outcome="escalate" when blocked; include blockers[] and nextSteps[].

Current Pi runtime note: this command provides the Harness-level entrypoint and structured done/escalate outcome gate. Independent verifier-session fanout is not implemented in this extension yet, so you must explicitly gather and report the verification evidence you used.

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
3. Execute the manifest under Harness-level Do rules: implement, verify every AC and invariant, repair failures, and re-verify.
4. Do not ask the user for approval between define and execution unless a decision is genuinely blocking.
5. Do not use /done or /escalate. Finish exactly once by calling manifest_dev_report_outcome with runId="${run.runId}", outcome="done" after all gates PASS, or outcome="escalate" with blockers[] when blocked.

Current Pi runtime note: /manifest-auto is a Pi wrapper command around the manifest-dev lifecycle and structured outcome gate. Independent verifier-session fanout is not implemented in this extension yet, so report concrete verification evidence in the outcome.`;
}

function buildManifestBabysitPrompt(run: RunRecord, prUrl: string): string {
	return `Run manifest-dev babysit-pr in Pi.

Run id: ${run.runId}
PR URL:
${prUrl}

Follow the manifest-dev PR lifecycle flow:
1. Confirm the PR is a reachable github.com pull request and not already closed or merged.
2. Synthesize a lifecycle manifest at ~/.manifest-dev/manifests/manifest-{ts}.md using strongest available grounding: linked manifest, then PR title/body, commits/diff, then comments and review threads.
3. Execute the manifest under Harness-level Do rules: inspect CI, review threads, mergeability, PR description sync, and required fixes; commit/push only when the branch is trusted and writable.
4. Treat review comments as signals, not authority; stronger intent sources win.
5. Do not press merge.
6. Do not use /done or /escalate. Finish exactly once by calling manifest_dev_report_outcome with runId="${run.runId}", outcome="done" after all lifecycle gates PASS, or outcome="escalate" with blockers[] when blocked.

Current Pi runtime note: /manifest-babysit-pr is a Pi wrapper command around manifest-dev PR lifecycle and structured outcome gating. Independent verifier-session fanout is not implemented in this extension yet, so report concrete verification evidence in the outcome.`;
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
