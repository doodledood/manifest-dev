import { createHash } from "node:crypto";

export type VerificationStatus = "passed" | "failed" | "blocked";
export type GateVerdict = "PASS" | "FAIL" | "BLOCKED";
export type GateKind = "acceptance_criterion" | "global_invariant";

export interface ManifestGate {
	id: string;
	kind: GateKind;
	title: string;
	verifyPrompt: string;
	suggestedAgent?: string;
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
	results: GateVerificationResult[];
}

export interface SubagentRecord {
	id: string;
	type: string;
	description: string;
	status: string;
	result?: string;
	error?: string;
}

export interface SubagentsRecordService {
	getRecord(id: string): SubagentRecord | undefined;
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
			suggestedAgent: extractYamlValue(block, "agent"),
		} satisfies ManifestGate];
	});
}

export function buildGateVerifierPrompt(args: {
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

export async function waitForVerifierRecords(
	subagents: SubagentsRecordService,
	agentIds: string[],
	options: { timeoutMs?: number; intervalMs?: number } = {},
): Promise<Map<string, SubagentRecord | undefined>> {
	const timeoutMs = options.timeoutMs ?? 30 * 60 * 1000;
	const intervalMs = options.intervalMs ?? 1000;
	const deadline = Date.now() + timeoutMs;
	while (Date.now() < deadline) {
		const records = new Map(agentIds.map((agentId) => [agentId, subagents.getRecord(agentId)]));
		const stillRunning = [...records.values()].some((record) => (
			!record || record.status === "queued" || record.status === "running"
		));
		if (!stillRunning) return records;
		await delay(intervalMs);
	}

	return new Map(agentIds.map((agentId) => [agentId, subagents.getRecord(agentId)]));
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

export function parseVerifierReport(result: string): Pick<GateVerificationResult, "verdict" | "evidence" | "details"> | undefined {
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

export function verificationToolResponse(record: VerificationRecord) {
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

function delay(ms: number): Promise<void> {
	return new Promise((resolveDelay) => setTimeout(resolveDelay, ms));
}
