import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export type VerificationStatus = "passed" | "failed" | "blocked";
export type GateVerdict = "PASS" | "FAIL" | "BLOCKED";
export type GateKind = "acceptance_criterion" | "global_invariant";

// Verifier→runtime contract token (NOT a check-pr token — check-pr stays workflow-neutral).
// In a `/babysit-pr --ci` (ciOneShot) run the runtime injects CI_WAIT_PENDING_VERIFIER_RULE
// into every gate's verifier prompt; a verifier that finds the gate is blocked only on an
// external wait appends this marker, and the runtime routes the failure to a pending exit
// instead of repair. Defined here (not in the executor prompt) so it reaches the verifier
// execution context for synthesized AND --manifest runs alike.
export const WAIT_PENDING_MARKER = "WAIT-PENDING";
export const CI_WAIT_PENDING_VERIFIER_RULE = `
CI one-shot wait-pending rule: if this gate's only remaining blocker is an external wait — the check-pr finding's sole directive is a wait ("bash sleep <N>; reinvoke") and nothing is actionable (no reply / reply-and-resolve / retrigger / sync-description / re-request-review / prose fix) — append the token ${WAIT_PENDING_MARKER} on its own line in DETAILS. Pick the VERDICT by the normal rules above (a reviewer / CI / merge-window wait is typically BLOCKED — a human/external condition, not a workspace-repairable defect); the runtime treats either FAIL or BLOCKED carrying ${WAIT_PENDING_MARKER} as a pending exit instead of looping repair or escalating. Omit ${WAIT_PENDING_MARKER} entirely if anything here is actionable.`;


export interface ManifestGate {
	id: string;
	kind: GateKind;
	title: string;
	verifyPrompt: string;
	model?: string;
	phase: number;
}

export interface GateVerificationResult {
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

export interface VerificationRecord {
	runId: string;
	manifestPath: string;
	manifestSha256: string;
	requestedAt: string;
	completedAt: string;
	cwd: string;
	status: VerificationStatus;
	implementationSummary?: string;
	orchestratorSessionId?: string;
	orchestratorSessionFile?: string;
	attempt?: number;
	results: GateVerificationResult[];
	workspaceDiffSha256?: string;
}

export interface SubagentRecord {
	id: string;
	type: string;
	description: string;
	status: string;
	result?: string;
	error?: string;
}

export function extractManifestGates(manifest: string): ManifestGate[] {
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
			model: extractYamlValue(block, "model"),
			phase: parsePhase(extractYamlValue(block, "phase")),
		} satisfies ManifestGate];
	});
}

export function buildGateVerifierPrompt(args: {
	gate: ManifestGate;
	manifestPath: string;
	manifest: string;
	runId: string;
	implementationSummary?: string;
	reposMap?: Record<string, string>;
	orchestratorSessionId?: string;
	orchestratorSessionFile?: string;
	ciOneShot?: boolean;
}): string {
	const waitPendingRule = args.ciOneShot ? `\n${CI_WAIT_PENDING_VERIFIER_RULE}\n` : "";
	const implementationSummary = args.implementationSummary
		? `\nImplementation summary from executor:\n${args.implementationSummary}\n`
		: "";
	const orchestratorSession = args.orchestratorSessionId
		? `\nVerification orchestrator session: ${args.orchestratorSessionId}${args.orchestratorSessionFile ? ` (${args.orchestratorSessionFile})` : ""}`
		: "";
	const reposEntries = Object.entries(args.reposMap ?? {});
	const reposBlock = reposEntries.length > 0
		? `\nRepository path map (use the absolute path for each repo when inspecting a non-cwd repo):\n${reposEntries.map(([name, path]) => `- ${name}: ${path}`).join("\n")}\n`
		: "";

	return `You are a manifest-dev verifier running in a clean Pi JSON subprocess.

Verify exactly one manifest gate. Do not implement fixes. Inspect the workspace, run focused commands when useful, and judge only the assigned gate.
${reposBlock}
Run id: ${args.runId}${orchestratorSession}
Manifest path: ${args.manifestPath}
Gate: ${args.gate.id} ${args.gate.title}
Gate kind: ${args.gate.kind}
${implementationSummary}
Verification prompt:
${args.gate.verifyPrompt}
${waitPendingRule}
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

export function toGateVerificationResult(
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
			evidence: "Verifier record disappeared before aggregation.",
			details: "Runtime could not retrieve the verifier result.",
			error: "missing_verifier_record",
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
			evidence: `Verifier runner ended with status=${record.status}.`,
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

export function parseVerifierReport(result: string): Pick<GateVerificationResult, "verdict" | "evidence" | "details"> | undefined {
	const verdict = extractVerifierVerdict(result);
	if (!verdict) return undefined;
	const evidence = extractVerifierSection(result, "EVIDENCE") ?? "";
	const details = extractVerifierSection(result, "DETAILS", { allowSuffix: true }) ?? "";
	return {
		verdict,
		evidence,
		details,
	};
}

const MARKDOWN_EMPHASIS_MARKER_PATTERN = String.raw`(\*\*|__|\*|_)`;
const MARKDOWN_EMPHASIS_PATTERN = String.raw`(?:\*\*|__|\*|_)?`;
const HORIZONTAL_SPACE_PATTERN = String.raw`[^\S\r\n]*`;

function extractVerifierVerdict(result: string): GateVerdict | undefined {
	const match = findVerifierLabel(result, "VERDICT");
	if (!match) return undefined;

	const verdictLine = result.slice(match.index + match[0].length).match(/^[^\r\n]*/)?.[0] ?? "";
	const value = verdictLine.match(
		/^(?:\*\*|__|\*|_)?[^\S\r\n]*(PASS|FAIL|BLOCKED)[^\S\r\n]*(?:\*\*|__|\*|_)?[^\S\r\n]*$/,
	)?.[1];
	return value?.toUpperCase() as GateVerdict | undefined;
}

function extractVerifierSection(result: string, label: "EVIDENCE" | "DETAILS", options?: { allowSuffix?: boolean }): string | undefined {
	const match = findVerifierLabel(result, label, options);
	if (!match) return undefined;

	const start = match.index + match[0].length;
	const nextLabel = label === "EVIDENCE" ? findVerifierLabel(result, "DETAILS", { allowSuffix: true, start }) : undefined;
	return result.slice(start, nextLabel?.index).trim();
}

function findVerifierLabel(
	result: string,
	label: "VERDICT" | "EVIDENCE" | "DETAILS",
	options?: { allowSuffix?: boolean; start?: number },
): RegExpExecArray | undefined {
	const suffixPattern = options?.allowSuffix ? String.raw`(?:[^\S\r\n]+[—-][^:\r\n]*)?` : "";
	const wrappedLabelPattern = String.raw`${MARKDOWN_EMPHASIS_MARKER_PATTERN}${HORIZONTAL_SPACE_PATTERN}${label}\b${suffixPattern}${HORIZONTAL_SPACE_PATTERN}(?:\1${HORIZONTAL_SPACE_PATTERN}:|:${HORIZONTAL_SPACE_PATTERN}\1?)${HORIZONTAL_SPACE_PATTERN}`;
	const plainLabelPattern = String.raw`${label}\b${suffixPattern}${HORIZONTAL_SPACE_PATTERN}:${HORIZONTAL_SPACE_PATTERN}`;
	const pattern = new RegExp(
		String.raw`^${HORIZONTAL_SPACE_PATTERN}(?:${wrappedLabelPattern}|${plainLabelPattern})`,
		"gim",
	);
	pattern.lastIndex = options?.start ?? 0;
	return pattern.exec(result) ?? undefined;
}

export function aggregateVerificationStatus(results: GateVerificationResult[]): VerificationStatus {
	if (results.some((result) => result.verdict === "BLOCKED")) return "blocked";
	if (results.some((result) => result.verdict === "FAIL")) return "failed";
	return "passed";
}

export function makeBlockedVerificationRecord(args: {
	runId: string;
	manifestPath: string;
	manifest: string;
	cwd: string;
	requestedAt: string;
	implementationSummary?: string;
	blocker: string;
	orchestratorSessionId?: string;
	orchestratorSessionFile?: string;
	attempt?: number;
	workspaceDiffSha256?: string;
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
		orchestratorSessionId: args.orchestratorSessionId,
		orchestratorSessionFile: args.orchestratorSessionFile,
		attempt: args.attempt,
		workspaceDiffSha256: args.workspaceDiffSha256,
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

export function verificationToolResponse(record: VerificationRecord) {
	const summary = record.results
		.map((result) => `${result.gateId}: ${result.verdict} - ${firstLine(result.evidence || result.details)}`)
		.join("\n");
	const instruction = record.status === "passed"
		? "All manifest gates PASS. The runtime may record done for this run id."
		: record.status === "failed"
			? "Some manifest gates FAIL. Inject the failed gates back to the executor as repair work, then rerun clean verification after the executor stops again."
			: "Verification is BLOCKED. Record or surface a resumable blocker when human input, access, external state, or an unrecoverable decision is required.";

	return {
		content: [{
			type: "text",
			text: `Manifest-dev verification ${record.status.toUpperCase()} for ${record.runId}.\n\n${summary}\n\n${instruction}`,
		}],
		details: record,
	};
}

export function unquote(value: string): string {
	if (
		(value.startsWith('"') && value.endsWith('"'))
		|| (value.startsWith("'") && value.endsWith("'"))
	) {
		return value.slice(1, -1);
	}
	return value;
}

export function sha256(value: string): string {
	return createHash("sha256").update(value).digest("hex");
}

function extractYamlValue(block: string, key: string): string | undefined {
	const keyPattern = new RegExp(`^(\\s*)${key}:\\s*(.*?)\\s*$`);
	const lines = block.split(/\r?\n/);
	for (let index = 0; index < lines.length; index += 1) {
		const match = lines[index].match(keyPattern);
		if (!match) continue;

		const keyIndent = match[1].length;
		const value = match[2].trim();
		if (!value.startsWith("|") && !value.startsWith(">")) return parseInlineYamlValue(value);

		const scalarLines: string[] = [];
		for (let childIndex = index + 1; childIndex < lines.length; childIndex += 1) {
			const line = lines[childIndex];
			if (line.trim() === "") {
				scalarLines.push(line);
				continue;
			}

			const indent = leadingSpaces(line);
			if (indent <= keyIndent) break;
			scalarLines.push(line);
		}

		const contentIndent = Math.min(
			...scalarLines.filter((line) => line.trim()).map(leadingSpaces),
		);
		return scalarLines
			.map((line) => line.trim() ? line.slice(contentIndent) : "")
			.join("\n")
			.trim();
	}

	return undefined;
}

function parseInlineYamlValue(value: string): string | undefined {
	if (value === "") return undefined;
	if (value.startsWith('"') && value.endsWith('"')) {
		return unescapeQuotedYaml(value.slice(1, -1));
	}
	if (value.startsWith("'") && value.endsWith("'")) {
		return value.slice(1, -1).replaceAll("''", "'");
	}
	return value;
}

function leadingSpaces(value: string): number {
	return value.match(/^\s*/)?.[0].length ?? 0;
}

function unescapeQuotedYaml(value: string): string {
	try {
		return JSON.parse(`"${value}"`) as string;
	} catch {
		return value.replace(/\\"/g, '"');
	}
}

function firstLine(value: string): string {
	return value.split("\n")[0]?.trim() || "No evidence reported.";
}

function parsePhase(value: string | undefined): number {
	if (value === undefined) return 1;
	const parsed = Number.parseInt(value.trim(), 10);
	return Number.isInteger(parsed) && parsed > 0 ? parsed : 1;
}

/** Group gates into ascending-phase batches: serial across phases, parallel within. */
export function planVerifierBatches(gates: ManifestGate[]): ManifestGate[][] {
	const byPhase = new Map<number, ManifestGate[]>();
	for (const gate of gates) {
		const batch = byPhase.get(gate.phase) ?? [];
		batch.push(gate);
		byPhase.set(gate.phase, batch);
	}
	return [...byPhase.keys()].sort((a, b) => a - b).map((phase) => byPhase.get(phase) ?? []);
}

/** Split a phase batch into bounded parallel chunks, preserving manifest order. */
export function chunkManifestGates(gates: ManifestGate[], maxConcurrent: number): ManifestGate[][] {
	const limit = Number.isInteger(maxConcurrent) && maxConcurrent > 0 ? maxConcurrent : 1;
	const chunks: ManifestGate[][] = [];
	for (let index = 0; index < gates.length; index += limit) {
		chunks.push(gates.slice(index, index + limit));
	}
	return chunks;
}

/** Parse a manifest `Repos: [name: path, ...]` declaration into a name->path map. Empty when single-repo. */
export function extractReposMap(manifest: string): Record<string, string> {
	const line = manifest
		.split(/\r?\n/)
		.find((candidate) => /^\s*(?:[-*]\s*)?(?:\*\*)?Repos:/.test(candidate) && candidate.includes("[") && candidate.includes("]"));
	if (!line) return {};
	const inner = line.slice(line.indexOf("[") + 1, line.lastIndexOf("]"));
	const map: Record<string, string> = {};
	for (const part of inner.split(",")) {
		const separator = part.indexOf(":");
		if (separator === -1) continue;
		const name = part.slice(0, separator).trim();
		const path = part.slice(separator + 1).trim();
		if (name && path) map[name] = path;
	}
	return map;
}

export function runStateFileName(runId: string): string {
	return `${runId.replace(/[^A-Za-z0-9._-]/g, "_")}.json`;
}

/** Parse a persisted run-state file; returns undefined on missing/corrupt/foreign content. */
export function parseRunState(text: string): VerificationRecord | undefined {
	try {
		const parsed = JSON.parse(text) as Partial<VerificationRecord>;
		if (parsed && typeof parsed.runId === "string" && typeof parsed.status === "string" && Array.isArray(parsed.results)) {
			return parsed as VerificationRecord;
		}
		return undefined;
	} catch {
		return undefined;
	}
}

export function writeRunStateFile(verification: VerificationRecord, directory: string): boolean {
	try {
		mkdirSync(directory, { recursive: true });
		writeFileSync(
			join(directory, runStateFileName(verification.runId)),
			JSON.stringify(verification, null, 2),
			"utf-8",
		);
		return true;
	} catch {
		return false;
	}
}

export function readRunStateFile(runId: string, directory: string): VerificationRecord | undefined {
	try {
		const file = join(directory, runStateFileName(runId));
		if (!existsSync(file)) return undefined;
		return parseRunState(readFileSync(file, "utf-8"));
	} catch {
		return undefined;
	}
}

export interface DoneReadiness {
	ready: boolean;
	reason?: string;
}

export function shouldStopAfterBatch(results: GateVerificationResult[]): boolean {
	return results.some((result) => result.verdict !== "PASS");
}

/** Decide whether `done` may be reported: only on an all-PASS verification that still matches the current manifest + workspace. */
export function evaluateDoneReadiness(args: {
	verification: VerificationRecord | undefined;
	currentManifestSha256?: string;
	currentWorkspaceDiffSha256?: string;
}): DoneReadiness {
	const verification = args.verification;
	if (!verification) return { ready: false, reason: "no verification report exists for this run id" };
	if (verification.status !== "passed") return { ready: false, reason: `latest verification is ${verification.status}` };
	if (args.currentManifestSha256 === undefined) {
		return { ready: false, reason: "the manifest is unavailable — re-verify before reporting done" };
	}
	if (
		verification.manifestSha256 !== undefined
		&& args.currentManifestSha256 !== verification.manifestSha256
	) {
		return { ready: false, reason: "the manifest changed since verification \u2014 re-verify before reporting done" };
	}
	if (
		verification.workspaceDiffSha256 !== undefined
		&& args.currentWorkspaceDiffSha256 !== undefined
		&& verification.workspaceDiffSha256 !== args.currentWorkspaceDiffSha256
	) {
		return { ready: false, reason: "the workspace changed since verification \u2014 re-verify before reporting done" };
	}
	return { ready: true };
}

/** Only `done` ends (terminates) the run; `escalate` is a resumable pause. */
export function shouldTerminateOutcome(outcome: "done" | "escalate"): boolean {
	return outcome === "done";
}

/** Resolve a positive-integer config value: flag > env > fallback, ignoring blank/invalid candidates. */
export function resolvePositiveIntConfig(args: { flag?: unknown; env?: string; fallback: number }): number {
	for (const candidate of [args.flag, args.env]) {
		if (typeof candidate !== "string" && typeof candidate !== "number") continue;
		const parsed = typeof candidate === "number" ? candidate : Number.parseInt(candidate.trim(), 10);
		if (Number.isInteger(parsed) && parsed > 0) return parsed;
	}
	return args.fallback;
}

/** Resolve the verifier model: an explicit gate `verify.model` wins; otherwise inherit the main session's current model. */
export function resolveVerifierModel(
	gateModel: string | undefined,
	sessionModel: { provider?: string; id?: string } | undefined,
): string | undefined {
	const gate = gateModel?.trim();
	if (gate) return gate;
	if (sessionModel?.id) {
		return sessionModel.provider ? `${sessionModel.provider}/${sessionModel.id}` : sessionModel.id;
	}
	return undefined;
}

/** Resolve a string config value: flag > env > fallback, ignoring blank candidates. */
export function resolveStringConfig(args: { flag?: unknown; env?: string; fallback: string }): string {
	const flag = typeof args.flag === "string" ? args.flag.trim() : "";
	if (flag.length > 0) return flag;
	const env = args.env?.trim();
	if (env && env.length > 0) return env;
	return args.fallback;
}
