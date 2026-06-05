import test from "node:test";
import assert from "node:assert/strict";
import {
	aggregateVerificationStatus,
	buildGateVerifierPrompt,
	extractManifestGates,
	makeBlockedVerificationRecord,
	parseVerifierReport,
	sha256,
	toGateVerificationResult,
	unquote,
	verificationToolResponse,
	waitForVerifierRecords,
} from "../pi/extensions/manifest-dev-runtime.ts";

const gate = {
	id: "AC-1.1",
	kind: "acceptance_criterion",
	title: "Thing works",
	verifyPrompt: "Run npm test and inspect output.",
	suggestedAgent: "test-quality-reviewer",
};

function completedRecord(result) {
	return {
		id: "agent-1",
		type: "Explore",
		description: "AC-1.1",
		status: "completed",
		result,
	};
}

test("extractManifestGates parses AC and invariant verify prompts", () => {
	const manifest = `
## 3. Global Invariants
- [INV-G1] Runtime claims stay honest.
  \`\`\`yaml
  verify:
    prompt: "Run: echo \\"ok\\""
    agent: "docs-reviewer"
  \`\`\`
- [INV-G2] Missing verify is skipped.

## 4. Deliverables
- [AC-1.1] Single quoted prompt.
  \`\`\`yaml
  verify:
    prompt: 'Check it''s fine'
  \`\`\`
- [AC-2.1] Block scalar prompt.
  \`\`\`yaml
  verify:
    prompt: |
      first line
      second line
    agent: contracts-reviewer
  \`\`\`
- [PG-1] Process guidance is not a verifier gate.
`;

	assert.deepEqual(extractManifestGates(manifest), [
		{
			id: "INV-G1",
			kind: "global_invariant",
			title: "Runtime claims stay honest.",
			verifyPrompt: 'Run: echo "ok"',
			suggestedAgent: "docs-reviewer",
		},
		{
			id: "AC-1.1",
			kind: "acceptance_criterion",
			title: "Single quoted prompt.",
			verifyPrompt: "Check it's fine",
			suggestedAgent: undefined,
		},
		{
			id: "AC-2.1",
			kind: "acceptance_criterion",
			title: "Block scalar prompt.",
			verifyPrompt: "first line\nsecond line",
			suggestedAgent: "contracts-reviewer",
		},
	]);
});

test("buildGateVerifierPrompt creates a single-gate clean-session contract", () => {
	const prompt = buildGateVerifierPrompt({
		gate,
		manifestPath: "/tmp/manifest.md",
		manifest: "# Manifest",
		runId: "manifest-dev-abc123",
		implementationSummary: "Changed extension runtime.",
	});

	assert.match(prompt, /clean Pi subagent session/);
	assert.match(prompt, /Do not implement fixes/);
	assert.match(prompt, /Gate: AC-1\.1 Thing works/);
	assert.match(prompt, /Suggested manifest verifier persona: test-quality-reviewer/);
	assert.match(prompt, /Run npm test and inspect output\./);
	assert.match(prompt, /VERDICT: PASS\|FAIL\|BLOCKED/);
	assert.match(prompt, /Changed extension runtime\./);
	assert.match(prompt, /# Manifest/);
});

test("parseVerifierReport extracts verdict evidence and multiline details", () => {
	assert.deepEqual(
		parseVerifierReport(`
VERDICT: FAIL
EVIDENCE: pytest failed on AC-1.1
DETAILS: first line
second line
`),
		{
			verdict: "FAIL",
			evidence: "pytest failed on AC-1.1",
			details: "first line\nsecond line",
		},
	);

	assert.equal(parseVerifierReport("EVIDENCE: no verdict"), undefined);
});

test("toGateVerificationResult converts verifier agent terminal states", () => {
	assert.deepEqual(toGateVerificationResult(gate, "agent-missing", undefined), {
		gateId: "AC-1.1",
		kind: "acceptance_criterion",
		title: "Thing works",
		agentId: "agent-missing",
		verdict: "BLOCKED",
		evidence: "Verifier subagent record disappeared before aggregation.",
		details: "Runtime could not retrieve the verifier result.",
		error: "missing_subagent_record",
	});

	assert.equal(
		toGateVerificationResult(gate, "agent-error", {
			id: "agent-error",
			type: "Explore",
			description: "AC-1.1",
			status: "error",
			error: "model failed",
		}).verdict,
		"BLOCKED",
	);

	assert.equal(
		toGateVerificationResult(gate, "agent-bad-report", completedRecord("not a report")).verdict,
		"BLOCKED",
	);

	assert.deepEqual(
		toGateVerificationResult(
			gate,
			"agent-pass",
			completedRecord(`
VERDICT: PASS
EVIDENCE: command exited 0
DETAILS: all good
`),
		),
		{
			gateId: "AC-1.1",
			kind: "acceptance_criterion",
			title: "Thing works",
			agentId: "agent-pass",
			agentStatus: "completed",
			verdict: "PASS",
			evidence: "command exited 0",
			details: "all good",
			rawResult: "\nVERDICT: PASS\nEVIDENCE: command exited 0\nDETAILS: all good\n",
		},
	);
});

test("aggregateVerificationStatus gives blocked precedence over failed over passed", () => {
	assert.equal(aggregateVerificationStatus([{ ...gateResult("PASS") }]), "passed");
	assert.equal(
		aggregateVerificationStatus([gateResult("PASS"), gateResult("FAIL")]),
		"failed",
	);
	assert.equal(
		aggregateVerificationStatus([gateResult("FAIL"), gateResult("BLOCKED")]),
		"blocked",
	);
});

test("waitForVerifierRecords waits until queued or running agents finish", async () => {
	let reads = 0;
	const service = {
		getRecord() {
			reads += 1;
			return reads === 1
				? { id: "agent-1", type: "Explore", description: "AC-1.1", status: "running" }
				: completedRecord("VERDICT: PASS\nEVIDENCE: ok\nDETAILS: ok");
		},
	};

	const records = await waitForVerifierRecords(service, ["agent-1"], {
		timeoutMs: 50,
		intervalMs: 1,
	});

	assert.equal(records.get("agent-1").status, "completed");
	assert.equal(reads, 2);
});

test("makeBlockedVerificationRecord and verificationToolResponse encode runtime blockers", () => {
	const record = makeBlockedVerificationRecord({
		runId: "manifest-dev-run",
		manifestPath: "/tmp/manifest.md",
		manifest: "# Manifest",
		cwd: "/repo",
		requestedAt: "2026-06-05T00:00:00.000Z",
		implementationSummary: "ready",
		blocker: "subagents service missing",
	});

	assert.equal(record.status, "blocked");
	assert.equal(record.manifestSha256, sha256("# Manifest"));
	assert.equal(record.results[0].verdict, "BLOCKED");
	assert.equal(record.results[0].details, "subagents service missing");

	const response = verificationToolResponse(record);
	assert.match(response.content[0].text, /Verification is BLOCKED/);
	assert.match(response.content[0].text, /outcome="escalate"/);
	assert.equal(response.details, record);
});

test("verificationToolResponse tells executor to finish or repair", () => {
	const passed = {
		runId: "manifest-dev-run",
		manifestPath: "/tmp/manifest.md",
		manifestSha256: "hash",
		requestedAt: "start",
		completedAt: "end",
		cwd: "/repo",
		status: "passed",
		results: [gateResult("PASS")],
	};
	const failed = {
		...passed,
		status: "failed",
		results: [gateResult("FAIL")],
	};

	assert.match(verificationToolResponse(passed).content[0].text, /outcome="done"/);
	assert.match(verificationToolResponse(failed).content[0].text, /Repair the failed gates/);
});

test("unquote removes balanced shell-style quotes only", () => {
	assert.equal(unquote('"manifest.md"'), "manifest.md");
	assert.equal(unquote("'manifest.md'"), "manifest.md");
	assert.equal(unquote('"unterminated'), '"unterminated');
});

function gateResult(verdict) {
	return {
		gateId: "AC-1.1",
		kind: "acceptance_criterion",
		title: "Thing works",
		verdict,
		evidence: `${verdict} evidence`,
		details: `${verdict} details`,
	};
}
