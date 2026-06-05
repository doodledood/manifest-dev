import test from "node:test";
import assert from "node:assert/strict";
import {
	aggregateVerificationStatus,
	buildGateVerifierPrompt,
	evaluateDoneReadiness,
	extractManifestGates,
	extractReposMap,
	makeBlockedVerificationRecord,
	parseRunState,
	parseVerifierReport,
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
- [AC-3.1] Model and phase.
  \`\`\`yaml
  verify:
    prompt: "run check"
    model: gpt-5
    phase: 2
  \`\`\`
- [AC-4.1] Invalid phase falls back.
  \`\`\`yaml
  verify:
    prompt: "x"
    phase: not-a-number
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
			model: undefined,
			phase: 1,
		},
		{
			id: "AC-1.1",
			kind: "acceptance_criterion",
			title: "Single quoted prompt.",
			verifyPrompt: "Check it's fine",
			suggestedAgent: undefined,
			model: undefined,
			phase: 1,
		},
		{
			id: "AC-2.1",
			kind: "acceptance_criterion",
			title: "Block scalar prompt.",
			verifyPrompt: "first line\nsecond line",
			suggestedAgent: "contracts-reviewer",
			model: undefined,
			phase: 1,
		},
		{
			id: "AC-3.1",
			kind: "acceptance_criterion",
			title: "Model and phase.",
			verifyPrompt: "run check",
			suggestedAgent: undefined,
			model: "gpt-5",
			phase: 2,
		},
		{
			id: "AC-4.1",
			kind: "acceptance_criterion",
			title: "Invalid phase falls back.",
			verifyPrompt: "x",
			suggestedAgent: undefined,
			model: undefined,
			phase: 1,
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

test("planVerifierBatches groups by ascending phase, parallel within", () => {
	const g = (id, phase) => ({ id, kind: "acceptance_criterion", title: id, verifyPrompt: "x", phase });
	const batches = planVerifierBatches([g("AC-1.1", 2), g("AC-1.2", 1), g("AC-1.3", 2), g("AC-1.4", 1)]);
	assert.deepEqual(
		batches.map((batch) => batch.map((gate) => gate.id)),
		[["AC-1.2", "AC-1.4"], ["AC-1.1", "AC-1.3"]],
	);
});

test("extractReposMap parses a Repos declaration and ignores single-repo", () => {
	assert.deepEqual(
		extractReposMap("- **Repos:** [loco: /a/loco, billing: /b/billing]"),
		{ loco: "/a/loco", billing: "/b/billing" },
	);
	assert.deepEqual(extractReposMap("no repos declared here"), {});
});

test("buildGateVerifierPrompt prepends repo map only for multi-repo", () => {
	const gate = { id: "AC-1.1", kind: "acceptance_criterion", title: "t", verifyPrompt: "do it", phase: 1 };
	const base = buildGateVerifierPrompt({ gate, manifestPath: "/m", manifest: "# M", runId: "r" });
	const withRepos = buildGateVerifierPrompt({ gate, manifestPath: "/m", manifest: "# M", runId: "r", reposMap: { loco: "/a" } });
	assert.ok(!base.includes("Repository path map"));
	assert.match(withRepos, /Repository path map/);
	assert.match(withRepos, /- loco: \/a/);
	// Empty map (single-repo) is byte-identical to omitting reposMap.
	assert.equal(buildGateVerifierPrompt({ gate, manifestPath: "/m", manifest: "# M", runId: "r", reposMap: {} }), base);
});

test("run-state round-trips and rejects corrupt or foreign content", () => {
	const record = makeBlockedVerificationRecord({
		runId: "manifest-dev-run",
		manifestPath: "/m",
		manifest: "# M",
		cwd: "/repo",
		requestedAt: "t",
		blocker: "b",
	});
	assert.equal(runStateFileName("manifest-dev-d0/be c"), "manifest-dev-d0_be_c.json");
	assert.deepEqual(parseRunState(JSON.stringify(record)), JSON.parse(JSON.stringify(record)));
	assert.equal(parseRunState("{not json"), undefined);
	assert.equal(parseRunState('{"runId":"x"}'), undefined);
});

test("resolveVerifierModel prefers the gate model then inherits the session model", () => {
	assert.equal(resolveVerifierModel("openai/gpt-5", { provider: "anthropic", id: "claude" }), "openai/gpt-5");
	assert.equal(resolveVerifierModel(undefined, { provider: "anthropic", id: "claude-sonnet-4" }), "anthropic/claude-sonnet-4");
	assert.equal(resolveVerifierModel(undefined, { id: "bare-id" }), "bare-id");
	assert.equal(resolveVerifierModel(undefined, undefined), undefined);
});

test("evaluateDoneReadiness clears only an all-PASS verification that still matches", () => {
	const base = {
		runId: "r", manifestPath: "/m", manifestSha256: "msha", requestedAt: "a", completedAt: "b",
		cwd: "/repo", status: "passed", results: [], workspaceDiffSha256: "dsha",
	};
	assert.equal(evaluateDoneReadiness({ verification: undefined }).ready, false);
	assert.equal(evaluateDoneReadiness({ verification: { ...base, status: "failed" } }).ready, false);
	assert.equal(
		evaluateDoneReadiness({ verification: base, currentManifestSha256: "msha", currentWorkspaceDiffSha256: "dsha" }).ready,
		true,
	);
	assert.equal(
		evaluateDoneReadiness({ verification: base, currentManifestSha256: "changed", currentWorkspaceDiffSha256: "dsha" }).ready,
		false,
	);
	assert.equal(
		evaluateDoneReadiness({ verification: base, currentManifestSha256: "msha", currentWorkspaceDiffSha256: "changed" }).ready,
		false,
	);
});

test("shouldTerminateOutcome terminates done only", () => {
	assert.equal(shouldTerminateOutcome("done"), true);
	assert.equal(shouldTerminateOutcome("escalate"), false);
});

test("config resolution follows flag > env > default with validation", () => {
	assert.equal(resolvePositiveIntConfig({ flag: "50", env: "9", fallback: 1000 }), 50);
	assert.equal(resolvePositiveIntConfig({ flag: "bad", env: "9", fallback: 1000 }), 9);
	assert.equal(resolvePositiveIntConfig({ flag: undefined, env: "0", fallback: 1000 }), 1000);
	assert.equal(resolvePositiveIntConfig({ flag: undefined, env: undefined, fallback: 1000 }), 1000);
	assert.equal(resolveStringConfig({ flag: "general-purpose", env: "x", fallback: "d" }), "general-purpose");
	assert.equal(resolveStringConfig({ flag: "  ", env: "fromenv", fallback: "d" }), "fromenv");
	assert.equal(resolveStringConfig({ flag: undefined, env: undefined, fallback: "d" }), "d");
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
