import test from "node:test";
import assert from "node:assert/strict";
import { chmodSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import manifestDevExtension, {
	buildManifestAutoPrompt,
	buildManifestBabysitPrompt,
	buildManifestDoPrompt,
	buildVerifierJsonCommand,
	createVerificationOrchestratorSession,
	buildCiPendingSummary,
	extractFinalAssistantTextFromJsonEvents,
	formatRepairFollowUpMessage,
	isWaitPendingVerification,
	makeOrchestratorSessionId,
	rehydrateRuntimeState,
	resolveManifestPath,
	routeVerificationResult,
	runVerifierSubprocess,
	shouldTriggerHarnessVerification,
	startManifestDo,
} from "../pi/extensions/manifest-dev.ts";
import {
	aggregateVerificationStatus,
	buildGateVerifierPrompt,
	chunkManifestGates,
	evaluateDoneReadiness,
	extractManifestGates,
	extractReposMap,
	makeBlockedVerificationRecord,
	parseRunState,
	parseVerifierReport,
	planVerifierBatches,
	readRunStateFile,
	resolvePositiveIntConfig,
	resolveStringConfig,
	resolveVerifierModel,
	runStateFileName,
	sha256,
	shouldStopAfterBatch,
	shouldTerminateOutcome,
	toGateVerificationResult,
	unquote,
	verificationToolResponse,
	writeRunStateFile,
} from "../pi/extensions/manifest-dev-runtime.ts";

const gate = {
	id: "AC-1.1",
	kind: "acceptance_criterion",
	title: "Thing works",
	verifyPrompt: "Run npm test and inspect output.",
};

function completedRecord(result) {
	return {
		id: "agent-1",
		type: "pi-json-subprocess",
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
			model: undefined,
			phase: 1,
		},
		{
			id: "AC-1.1",
			kind: "acceptance_criterion",
			title: "Single quoted prompt.",
			verifyPrompt: "Check it's fine",
			model: undefined,
			phase: 1,
		},
		{
			id: "AC-2.1",
			kind: "acceptance_criterion",
			title: "Block scalar prompt.",
			verifyPrompt: "first line\nsecond line",
			model: undefined,
			phase: 1,
		},
		{
			id: "AC-3.1",
			kind: "acceptance_criterion",
			title: "Model and phase.",
			verifyPrompt: "run check",
			model: "gpt-5",
			phase: 2,
		},
		{
			id: "AC-4.1",
			kind: "acceptance_criterion",
			title: "Invalid phase falls back.",
			verifyPrompt: "x",
			model: undefined,
			phase: 1,
		},
	]);
});

test("buildGateVerifierPrompt creates a single-gate JSON subprocess contract", () => {
	const prompt = buildGateVerifierPrompt({
		gate,
		manifestPath: "/tmp/manifest.md",
		manifest: "# Manifest",
		runId: "manifest-dev-abc123",
		implementationSummary: "Changed extension runtime.",
		orchestratorSessionId: "manifest-verify-123",
	});

	assert.match(prompt, /clean Pi JSON subprocess/);
	assert.match(prompt, /Do not implement fixes/);
	assert.match(prompt, /Verification orchestrator session: manifest-verify-123/);
	assert.match(prompt, /Gate: AC-1\.1 Thing works/);
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

	for (const verdict of ["PASS", "FAIL", "BLOCKED"]) {
		assert.equal(
			parseVerifierReport(`VERDICT: ${verdict}\nEVIDENCE: ok\nDETAILS: ok`)?.verdict,
			verdict,
		);
	}
});

test("parseVerifierReport accepts markdown emphasis around report labels", () => {
	assert.deepEqual(
		parseVerifierReport(`
Typecheck passes, confirming the full chain compiles.

**VERDICT: PASS**

**EVIDENCE:**
- Loaded the contracts dimension reference.
- Ran \`npx nx run cxllm:tsc\` → **exit 0**, no type errors.

**DETAILS — what passed:**
- Data type fields flow end-to-end.
- MCP and Slack surfaces preserve matching shapes.
`),
		{
			verdict: "PASS",
			evidence: "- Loaded the contracts dimension reference.\n- Ran `npx nx run cxllm:tsc` → **exit 0**, no type errors.",
			details: "- Data type fields flow end-to-end.\n- MCP and Slack surfaces preserve matching shapes.",
		},
	);

	assert.deepEqual(
		parseVerifierReport(`
Both review dimensions complete. Final assessment:

---

**VERDICT: PASS**

**EVIDENCE:**
- Inspected full change diff via \`git diff origin/master...HEAD\`.
- Loaded and applied review-code references.

**DETAILS:**

test-quality — PASS.
code-testability — PASS.
`),
		{
			verdict: "PASS",
			evidence: "- Inspected full change diff via `git diff origin/master...HEAD`.\n- Loaded and applied review-code references.",
			details: "test-quality — PASS.\ncode-testability — PASS.",
		},
	);

	assert.equal(
		parseVerifierReport("**VERDICT:** PASS\n**EVIDENCE:** ok\n**DETAILS:** ok")?.verdict,
		"PASS",
	);

	for (const verdict of ["PASS", "FAIL", "BLOCKED"]) {
		assert.equal(
			parseVerifierReport(`**VERDICT:** **${verdict}**\n**EVIDENCE:** ok\n**DETAILS:** ok`)?.verdict,
			verdict,
		);
	}
});

test("parseVerifierReport rejects missing or non-contract verdicts", () => {
	assert.equal(parseVerifierReport("EVIDENCE: no verdict"), undefined);
	assert.equal(parseVerifierReport("Looks good; passed everything."), undefined);
	assert.equal(parseVerifierReport("**VERDICT: PASSED**\nEVIDENCE: ok\nDETAILS: ok"), undefined);
	assert.equal(parseVerifierReport("VERDICT: PASS because ok\nEVIDENCE: ok\nDETAILS: ok"), undefined);
	assert.equal(parseVerifierReport("VERDICT: PASS-ish\nEVIDENCE: ok\nDETAILS: ok"), undefined);
	assert.equal(parseVerifierReport("VERDICT: PASS/FAIL\nEVIDENCE: ok\nDETAILS: ok"), undefined);
});

test("toGateVerificationResult converts verifier runner terminal states", () => {
	assert.deepEqual(toGateVerificationResult(gate, "agent-missing", undefined), {
		gateId: "AC-1.1",
		kind: "acceptance_criterion",
		title: "Thing works",
		agentId: "agent-missing",
		verdict: "BLOCKED",
		evidence: "Verifier record disappeared before aggregation.",
		details: "Runtime could not retrieve the verifier result.",
		error: "missing_verifier_record",
	});

	assert.equal(
		toGateVerificationResult(gate, "agent-error", {
			id: "agent-error",
			type: "pi-json-subprocess",
			description: "AC-1.1",
			status: "error",
			error: "model failed",
		}).verdict,
		"BLOCKED",
	);

	assert.deepEqual(
		toGateVerificationResult(gate, "agent-bad-report", completedRecord("not a report")),
		{
			gateId: "AC-1.1",
			kind: "acceptance_criterion",
			title: "Thing works",
			agentId: "agent-bad-report",
			agentStatus: "completed",
			verdict: "BLOCKED",
			evidence: "Verifier completed but did not emit a parseable VERDICT line.",
			details: "Expected report lines: VERDICT, EVIDENCE, DETAILS.",
			rawResult: "not a report",
		},
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

	assert.equal(
		toGateVerificationResult(
			gate,
			"agent-bold-pass",
			completedRecord("**VERDICT: PASS**\n\n**EVIDENCE:**\n- command exited 0\n\n**DETAILS:**\nall good"),
		).verdict,
		"PASS",
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

test("buildVerifierJsonCommand sends the prompt to pi json mode without suppressing resources", () => {
	const command = buildVerifierJsonCommand({
		gate,
		prompt: "VERIFIER PROMPT",
		cwd: "/repo",
		description: "AC-1.1: Thing works",
		model: "openai/gpt-5",
		thinkingLevel: "high",
		piBin: "/usr/local/bin/pi",
	});

	assert.equal(command.command, "/usr/local/bin/pi");
	assert.equal(command.cwd, "/repo");
	assert.equal(command.stdin, "VERIFIER PROMPT");
	assert.deepEqual(command.args, [
		"--mode",
		"json",
		"--print",
		"--no-session",
		"--name",
		"AC-1.1: Thing works",
		"--model",
		"openai/gpt-5",
		"--thinking",
		"high",
	]);
	assert.equal(command.args.includes("--no-extensions"), false);
	assert.equal(command.args.includes("--no-skills"), false);
});

test("extractFinalAssistantTextFromJsonEvents reads the final assistant message from Pi JSONL", () => {
	const stdout = [
		JSON.stringify({ type: "session", id: "s" }),
		JSON.stringify({
			type: "message_end",
			message: { role: "assistant", content: [{ type: "text", text: "draft" }] },
		}),
		JSON.stringify({
			type: "turn_end",
			message: { role: "assistant", content: [{ type: "text", text: "VERDICT: PASS\nEVIDENCE: ok\nDETAILS: ok" }] },
		}),
		"not-json",
		"",
	].join("\n");

	assert.equal(
		extractFinalAssistantTextFromJsonEvents(stdout),
		"VERDICT: PASS\nEVIDENCE: ok\nDETAILS: ok",
	);
});

test("runVerifierSubprocess captures successful final assistant text", async () => {
	const dir = mkdtempSync(`${tmpdir()}/manifest-dev-pi-json-`);
	const piBin = `${dir}/fake-pi-success.mjs`;
	writeFileSync(
		piBin,
		`#!/usr/bin/env node
process.stdin.resume();
let input = "";
process.stdin.on("data", (chunk) => { input += chunk; });
process.stdin.on("end", () => {
  console.log(JSON.stringify({ type: "message_end", message: { role: "assistant", content: [{ type: "text", text: "VERDICT: PASS\\nEVIDENCE: saw " + input.length + " bytes\\nDETAILS: ok" }] } }));
});
`,
		"utf-8",
	);
	chmodSync(piBin, 0o755);
	try {
		const record = await runVerifierSubprocess({
			gate,
			prompt: "exact verifier prompt",
			cwd: dir,
			description: "AC-1.1: Thing works",
			piBin,
		});
		assert.equal(record.type, "pi-json-subprocess");
		assert.equal(record.status, "completed");
		assert.match(record.result, /VERDICT: PASS/);
		assert.match(record.result, /saw 21 bytes/);
	} finally {
		rmSync(dir, { recursive: true, force: true });
	}
});

test("runVerifierSubprocess reports process failures with stdout and stderr evidence", async () => {
	const dir = mkdtempSync(`${tmpdir()}/manifest-dev-pi-json-fail-`);
	const piBin = `${dir}/fake-pi-fail.mjs`;
	writeFileSync(
		piBin,
		`#!/usr/bin/env node
console.log(JSON.stringify({ type: "message_end", message: { role: "assistant", content: [{ type: "text", text: "partial" }] } }));
console.error("model unavailable");
process.exit(7);
`,
		"utf-8",
	);
	chmodSync(piBin, 0o755);
	try {
		const record = await runVerifierSubprocess({
			gate,
			prompt: "prompt",
			cwd: dir,
			description: "AC-1.1: Thing works",
			piBin,
		});
		assert.equal(record.status, "error");
		assert.match(record.error, /exited with code 7/);
		assert.match(record.error, /stderr:\nmodel unavailable/);
		assert.match(record.error, /stdout:/);
		assert.equal(toGateVerificationResult(gate, record.id, record).verdict, "BLOCKED");
	} finally {
		rmSync(dir, { recursive: true, force: true });
	}
});

test("makeBlockedVerificationRecord and verificationToolResponse encode runtime blockers", () => {
	const record = makeBlockedVerificationRecord({
		runId: "manifest-dev-run",
		manifestPath: "/tmp/manifest.md",
		manifest: "# Manifest",
		cwd: "/repo",
		requestedAt: "2026-06-05T00:00:00.000Z",
		implementationSummary: "ready",
		blocker: "verifier subprocess unavailable",
		orchestratorSessionId: "manifest-verify-1",
		attempt: 2,
		workspaceDiffSha256: "diff-sha",
	});

	assert.equal(record.status, "blocked");
	assert.equal(record.manifestSha256, sha256("# Manifest"));
	assert.equal(record.orchestratorSessionId, "manifest-verify-1");
	assert.equal(record.attempt, 2);
	assert.equal(record.workspaceDiffSha256, "diff-sha");
	assert.equal(record.results[0].verdict, "BLOCKED");
	assert.equal(record.results[0].details, "verifier subprocess unavailable");

	const response = verificationToolResponse(record);
	assert.match(response.content[0].text, /Verification is BLOCKED/);
	assert.match(response.content[0].text, /resumable blocker/);
	assert.doesNotMatch(response.content[0].text, /manifest_dev_request_verification/);
	assert.doesNotMatch(response.content[0].text, /manifest_dev_report_outcome/);
	assert.equal(response.details, record);
});

test("verificationToolResponse summarizes legacy internal verification records", () => {
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

	const passedText = verificationToolResponse(passed).content[0].text;
	const failedText = verificationToolResponse(failed).content[0].text;
	assert.match(passedText, /runtime may record done/);
	assert.match(failedText, /Inject the failed gates back/);
	assert.doesNotMatch(passedText + failedText, /manifest_dev_request_verification/);
	assert.doesNotMatch(passedText + failedText, /manifest_dev_report_outcome/);
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

test("phase execution short-circuits later batches on FAIL or BLOCKED", () => {
	const g = (id, phase) => ({ id, kind: "acceptance_criterion", title: id, verifyPrompt: "x", phase });
	const batches = planVerifierBatches([g("AC-1.1", 1), g("AC-1.2", 2)]);
	const spawnedOnFail = [];
	for (const batch of batches) {
		spawnedOnFail.push(...batch.map((gate) => gate.id));
		if (shouldStopAfterBatch([gateResult(batch[0].phase === 1 ? "FAIL" : "PASS")])) break;
	}
	assert.deepEqual(spawnedOnFail, ["AC-1.1"]);

	const spawnedOnBlocked = [];
	for (const batch of batches) {
		spawnedOnBlocked.push(...batch.map((gate) => gate.id));
		if (shouldStopAfterBatch([gateResult(batch[0].phase === 1 ? "BLOCKED" : "PASS")])) break;
	}
	assert.deepEqual(spawnedOnBlocked, ["AC-1.1"]);

	assert.equal(shouldStopAfterBatch([gateResult("PASS")]), false);
});

test("chunkManifestGates bounds verifier fanout while preserving order", () => {
	const gates = Array.from({ length: 25 }, (_, index) => ({
		id: `AC-1.${index + 1}`,
		kind: "acceptance_criterion",
		title: `gate ${index + 1}`,
		verifyPrompt: "x",
		phase: 1,
	}));

	const chunks = chunkManifestGates(gates, 10);
	assert.deepEqual(chunks.map((chunk) => chunk.length), [10, 10, 5]);
	assert.deepEqual(chunks.flat().map((chunkGate) => chunkGate.id), gates.map((chunkGate) => chunkGate.id));
	assert.deepEqual(chunkManifestGates(gates.slice(0, 3), 0).map((chunk) => chunk.length), [1, 1, 1]);
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

test("run-state helpers round-trip to disk and handle missing or corrupt files", () => {
	const record = makeBlockedVerificationRecord({
		runId: "manifest-dev-run",
		manifestPath: "/m",
		manifest: "# M",
		cwd: "/repo",
		requestedAt: "t",
		blocker: "b",
	});
	const expected = JSON.parse(JSON.stringify(record));
	const dir = mkdtempSync(`${tmpdir()}/manifest-dev-runstate-`);
	try {
		assert.equal(runStateFileName("manifest-dev-d0/be c"), "manifest-dev-d0_be_c.json");
		assert.deepEqual(parseRunState(JSON.stringify(record)), expected);
		assert.equal(writeRunStateFile(record, dir), true);
		assert.deepEqual(readRunStateFile(record.runId, dir), expected);
		assert.equal(readRunStateFile("missing", dir), undefined);
		writeFileSync(`${dir}/${runStateFileName("corrupt")}`, "{not json", "utf-8");
		assert.equal(readRunStateFile("corrupt", dir), undefined);
		assert.equal(parseRunState("{not json"), undefined);
		assert.equal(parseRunState('{"runId":"x"}'), undefined);
	} finally {
		rmSync(dir, { recursive: true, force: true });
	}
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
	assert.equal(evaluateDoneReadiness({ verification: base, currentWorkspaceDiffSha256: "dsha" }).ready, false);
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

test("resolveManifestPath expands leading tilde while preserving relative paths", () => {
	const cwd = "/repo";
	assert.equal(resolveManifestPath("", cwd), undefined);
	assert.equal(resolveManifestPath("manifest.md", cwd), "/repo/manifest.md");
	assert.equal(resolveManifestPath("'manifest.md'", cwd), "/repo/manifest.md");
	assert.equal(resolveManifestPath('"~/manifest.md"', cwd), `${process.env.HOME}/manifest.md`);
	assert.equal(resolveManifestPath("~/.manifest-dev/manifests/m.md", cwd), `${process.env.HOME}/.manifest-dev/manifests/m.md`);
	assert.equal(resolveManifestPath("~", cwd), process.env.HOME);
});

test("simplified Pi executor prompts omit harness verification tools", () => {
	const run = {
		runId: "manifest-dev-run",
		manifestPath: "/tmp/manifest.md",
		manifestSha256: "hash",
	};
	const doPrompt = buildManifestDoPrompt(run, "# Manifest");
	assert.match(doPrompt, /implement the Manifest Deliverables/i);
	assert.match(doPrompt, /run useful local checks/i);
	assert.match(doPrompt, /runtime owns authoritative verification/i);
	assert.doesNotMatch(doPrompt, /manifest_dev_request_verification/);
	assert.doesNotMatch(doPrompt, /manifest_dev_report_outcome/);
	assert.doesNotMatch(doPrompt, /Finish exactly once/);

	const autoPrompt = buildManifestAutoPrompt(run, "build it");
	assert.match(autoPrompt, /write the manifest exactly at: \/tmp\/manifest\.md/);
	assert.doesNotMatch(autoPrompt, /manifest_dev_request_verification/);
	assert.doesNotMatch(autoPrompt, /manifest_dev_report_outcome/);

	const babysitPrompt = buildManifestBabysitPrompt(run, "https://github.com/o/r/pull/1");
	assert.match(babysitPrompt, /write the lifecycle manifest exactly at: \/tmp\/manifest\.md/);
	assert.doesNotMatch(babysitPrompt, /manifest_dev_request_verification/);
	assert.doesNotMatch(babysitPrompt, /manifest_dev_report_outcome/);
});

test("shouldTriggerHarnessVerification only allows active executor checkpoints", () => {
	const run = {
		runId: "manifest-dev-run",
		command: "do",
		startedAt: "t",
		cwd: "/repo",
		executorSessionId: "executor-session",
		status: "executing",
	};
	assert.equal(shouldTriggerHarnessVerification(run, "executor-session"), true);
	assert.equal(shouldTriggerHarnessVerification({ ...run, status: "repairing" }, "executor-session"), true);
	assert.equal(shouldTriggerHarnessVerification({ ...run, status: "verifying" }, "executor-session"), false);
	assert.equal(shouldTriggerHarnessVerification({ ...run, status: "done" }, "executor-session"), false);
	assert.equal(shouldTriggerHarnessVerification({ ...run, status: "blocked" }, "executor-session"), false);
	assert.equal(shouldTriggerHarnessVerification(run, "other-session"), false);
	assert.equal(shouldTriggerHarnessVerification(run, "executor-session", new Set(["executor-session"])), false);
	assert.equal(shouldTriggerHarnessVerification(undefined, "executor-session"), false);
});

test("extension registers agent_end lifecycle hook for Harness-level verification", () => {
	const events = new Map();
	const commands = new Map();
	const flags = [];
	const pi = {
		events: { on() {} },
		registerFlag(name, options) { flags.push({ name, options }); },
		on(name, handler) { events.set(name, handler); },
		registerCommand(name, command) { commands.set(name, command); },
	};

	manifestDevExtension(pi);

	assert.equal(typeof events.get("agent_end"), "function");
	assert.equal(typeof events.get("before_agent_start"), "function");
	assert.equal(commands.has("do"), true);
	assert.equal(commands.has("auto"), true);
	// babysit-pr moved to the @doodledood/manifest-dev-pi-tools package.
	assert.equal(commands.has("babysit-pr"), false);
	assert.equal(flags.some((flag) => flag.name === "manifest-verifier-max-concurrent"), true);
});

test("rehydrateRuntimeState removes terminal runs after replay", () => {
	const executing = {
		runId: "manifest-dev-run",
		command: "do",
		startedAt: "t",
		cwd: "/repo",
		executorSessionId: "executor-session",
		status: "executing",
	};
	const verification = {
		runId: executing.runId,
		manifestPath: "/m",
		manifestSha256: "h",
		requestedAt: "start",
		completedAt: "end",
		cwd: "/repo",
		status: "passed",
		results: [gateResult("PASS")],
	};
	const state = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map(),
		childSessionIds: new Set(),
	};
	const ctx = {
		sessionManager: {
			getBranch() {
				return [
					{ type: "custom", customType: "manifest-dev:run", data: executing },
					{ type: "custom", customType: "manifest-dev:verification", data: verification },
					{ type: "custom", customType: "manifest-dev:run", data: { ...executing, status: "done" } },
				];
			},
		},
	};

	rehydrateRuntimeState(ctx, state);

	assert.equal(state.activeRunByExecutorSessionId.has("executor-session"), false);
	assert.equal(state.latestVerificationByRunId.get(executing.runId), verification);
});

test("rehydrateRuntimeState scopes runs to the owning package's command set", () => {
	const doRun = {
		runId: "run-do",
		command: "do",
		startedAt: "t",
		cwd: "/repo",
		executorSessionId: "core-session",
		status: "executing",
	};
	const babysitRun = {
		runId: "run-babysit",
		command: "babysit-pr",
		startedAt: "t",
		cwd: "/repo",
		executorSessionId: "tools-session",
		status: "executing",
	};
	const ctx = {
		sessionManager: {
			getBranch() {
				return [
					{ type: "custom", customType: "manifest-dev:run", data: doRun },
					{ type: "custom", customType: "manifest-dev:run", data: babysitRun },
				];
			},
		},
	};

	// Tools runtime (owns babysit-pr) must ignore the core /do run, so it never
	// double-verifies it.
	const toolsState = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map(),
		childSessionIds: new Set(),
	};
	rehydrateRuntimeState(ctx, toolsState, new Set(["babysit-pr"]));
	assert.equal(toolsState.activeRunByExecutorSessionId.has("tools-session"), true);
	assert.equal(toolsState.activeRunByExecutorSessionId.has("core-session"), false);

	// Core runtime (owns do/auto) must ignore the tools babysit-pr run.
	const coreState = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map(),
		childSessionIds: new Set(),
	};
	rehydrateRuntimeState(ctx, coreState, new Set(["do", "auto"]));
	assert.equal(coreState.activeRunByExecutorSessionId.has("core-session"), true);
	assert.equal(coreState.activeRunByExecutorSessionId.has("tools-session"), false);
});

test("registered agent_end handler runs runtime verification path", async () => {
	const events = new Map();
	const commands = new Map();
	const calls = { entries: [], prompts: [], messages: [], activeTools: [] };
	const pi = {
		events: { on() {} },
		registerFlag() {},
		on(name, handler) { events.set(name, handler); },
		registerCommand(name, command) { commands.set(name, command); },
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		setSessionName() {},
		getActiveTools() { return calls.activeTools; },
		setActiveTools(names) { calls.activeTools = names; },
		sendUserMessage(prompt) { calls.prompts.push(prompt); },
		sendMessage(message, options) { calls.messages.push({ message, options }); },
	};
	manifestDevExtension(pi);

	const dir = mkdtempSync(`${tmpdir()}/manifest-dev-agent-end-`);
	const manifestPath = `${dir}/manifest.md`;
	const fakePiBin = `${dir}/fake-pi-fail.mjs`;
	writeFileSync(manifestPath, `# Manifest\n\n## 6. Deliverables\n### Deliverable 1: X\n**Acceptance Criteria:**\n- [AC-1.1] X works\n  \`\`\`yaml\n  verify:\n    prompt: "Check X"\n  \`\`\`\n`, "utf-8");
	writeFileSync(
		fakePiBin,
		`#!/usr/bin/env node
console.error("fake verifier failure");
process.exit(2);
`,
		"utf-8",
	);
	chmodSync(fakePiBin, 0o755);
	const ctx = {
		cwd: dir,
		sessionManager: { getSessionId() { return "executor-session"; } },
		isIdle() { return true; },
		hasPendingMessages() { return false; },
		ui: { notify() {} },
	};
	const previousPiBin = process.env.MANIFEST_DEV_PI_BIN;
	process.env.MANIFEST_DEV_PI_BIN = fakePiBin;
	try {
		await commands.get("do").handler(manifestPath, ctx);
		await events.get("agent_end")({}, ctx);

		const verificationEntry = calls.entries.find((entry) => entry.customType === "manifest-dev:verification");
		assert.ok(verificationEntry);
		assert.equal(verificationEntry.data.status, "blocked");
		assert.equal(verificationEntry.data.orchestratorSessionId.startsWith("manifest-verify-"), true);
		assert.ok(verificationEntry.data.orchestratorSessionFile);
		assert.equal(calls.entries.some((entry) => entry.customType === "manifest-dev:outcome" && entry.data.outcome === "escalate"), true);
		assert.equal(calls.entries.some((entry) => entry.customType === "manifest-dev:run" && entry.data.status === "blocked"), true);
		assert.equal(calls.messages.length, 1);
		assert.match(calls.messages[0].message.content, /verification is blocked/);
		assert.equal(calls.prompts.length, 1);
		assert.doesNotMatch(calls.prompts[0], /manifest_dev_request_verification/);

		rmSync(`${process.env.HOME}/.manifest-dev/runs/${verificationEntry.data.runId}.json`, { force: true });
		rmSync(verificationEntry.data.orchestratorSessionFile, { force: true });
	} finally {
		if (previousPiBin === undefined) {
			delete process.env.MANIFEST_DEV_PI_BIN;
		} else {
			process.env.MANIFEST_DEV_PI_BIN = previousPiBin;
		}
		rmSync(dir, { recursive: true, force: true });
	}
});

test("registered agent_end handler waits for pending messages before verification", async () => {
	const events = new Map();
	const commands = new Map();
	const calls = { entries: [], prompts: [], activeTools: [] };
	const pi = {
		events: { on() {} },
		registerFlag() {},
		on(name, handler) { events.set(name, handler); },
		registerCommand(name, command) { commands.set(name, command); },
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		setSessionName() {},
		getActiveTools() { return calls.activeTools; },
		setActiveTools(names) { calls.activeTools = names; },
		sendUserMessage(prompt) { calls.prompts.push(prompt); },
	};
	manifestDevExtension(pi);

	const dir = mkdtempSync(`${tmpdir()}/manifest-dev-pending-`);
	const manifestPath = `${dir}/manifest.md`;
	writeFileSync(manifestPath, "# Manifest\n\n## 6. Deliverables\n", "utf-8");
	const ctx = {
		cwd: dir,
		sessionManager: { getSessionId() { return "executor-session"; } },
		isIdle() { return true; },
		hasPendingMessages() { return true; },
		ui: { notify() {} },
	};
	try {
		await commands.get("do").handler(manifestPath, ctx);
		await events.get("agent_end")({}, ctx);
		assert.equal(calls.entries.some((entry) => entry.customType === "manifest-dev:verification"), false);
		assert.equal(calls.entries.some((entry) => entry.customType === "manifest-dev:outcome"), false);
	} finally {
		rmSync(dir, { recursive: true, force: true });
	}
});

test("startManifestDo records executor session and simplified prompt", async () => {
	const dir = mkdtempSync(`${tmpdir()}/manifest-dev-start-`);
	const manifestPath = `${dir}/manifest.md`;
	writeFileSync(manifestPath, "# Manifest\n\n## 6. Deliverables\n", "utf-8");
	const calls = { entries: [], prompts: [], sessionNames: [], notifications: [], activeTools: ["read", "manifest_dev_request_verification"] };
	const pi = {
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		setSessionName(name) { calls.sessionNames.push(name); },
		getActiveTools() { return calls.activeTools; },
		setActiveTools(names) { calls.activeTools = names; },
		sendUserMessage(prompt) { calls.prompts.push(prompt); },
	};
	const ctx = {
		cwd: dir,
		sessionManager: { getSessionId() { return "executor-session"; } },
		isIdle() { return true; },
		ui: { notify(message, level) { calls.notifications.push({ message, level }); } },
	};
	const state = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map(),
		childSessionIds: new Set(),
	};
	await startManifestDo(pi, manifestPath, ctx, state);
	try {
		const runEntry = calls.entries.find((entry) => entry.customType === "manifest-dev:run");
		assert.ok(runEntry);
		assert.equal(runEntry.data.executorSessionId, "executor-session");
		assert.equal(runEntry.data.status, "executing");
		assert.equal(state.activeRunByExecutorSessionId.get("executor-session").runId, runEntry.data.runId);
		assert.equal(shouldTriggerHarnessVerification(runEntry.data, "executor-session", state.childSessionIds), true);
		assert.equal(calls.activeTools.includes("manifest_dev_request_verification"), false);
		assert.equal(calls.prompts.length, 1);
		assert.match(calls.prompts[0], /Run manifest-dev Harness-level Do implementation/);
		assert.match(calls.prompts[0], /run useful local checks/i);
		assert.doesNotMatch(calls.prompts[0], /manifest_dev_request_verification/);
	} finally {
		rmSync(dir, { recursive: true, force: true });
	}
});

test("second executor stop after repair starts another clean Verification Orchestrator Session", () => {
	const requestedAt = "2026-06-05T20:00:00.000Z";
	const repairingRun = {
		runId: "manifest-dev-repair-loop-test",
		command: "do",
		startedAt: "2026-06-05T18:00:00.000Z",
		cwd: process.cwd(),
		executorSessionId: "executor-session",
		status: "repairing",
		verificationAttempts: 2,
	};
	const ctx = { cwd: process.cwd() };

	assert.equal(shouldTriggerHarnessVerification(repairingRun, "executor-session"), true);
	const firstAttemptId = makeOrchestratorSessionId({ ...repairingRun, verificationAttempts: 1 }, requestedAt);
	const secondAttempt = createVerificationOrchestratorSession(ctx, repairingRun, requestedAt);
	try {
		assert.notEqual(secondAttempt.id, firstAttemptId);
		assert.equal(secondAttempt.id, makeOrchestratorSessionId(repairingRun, requestedAt));
		const lines = readFileSync(secondAttempt.file, "utf-8").trim().split("\n").map((line) => JSON.parse(line));
		assert.equal(lines[0].parentSession, undefined);
		assert.equal(lines[1].parentId, null);
		assert.equal(lines[1].details.executorSessionId, "executor-session");
	} finally {
		if (secondAttempt.file) rmSync(secondAttempt.file, { force: true });
	}
});

test("verification orchestrator sessions are clean persisted attempts", () => {
	const requestedAt = "2026-06-05T19:00:00.000Z";
	const run = {
		runId: "manifest-dev-orchestrator-test",
		command: "do",
		startedAt: "2026-06-05T18:00:00.000Z",
		cwd: process.cwd(),
		executorSessionId: "executor-session",
		status: "verifying",
		verificationAttempts: 1,
	};
	const ctx = { cwd: process.cwd() };
	const firstId = makeOrchestratorSessionId(run, requestedAt);
	const secondId = makeOrchestratorSessionId({ ...run, verificationAttempts: 2 }, requestedAt);
	assert.notEqual(firstId, secondId);

	const session = createVerificationOrchestratorSession(ctx, run, requestedAt);
	try {
		assert.equal(session.id, firstId);
		assert.ok(session.file?.includes(".manifest-dev/verification-sessions"));
		const lines = readFileSync(session.file, "utf-8").trim().split("\n").map((line) => JSON.parse(line));
		assert.equal(lines[0].type, "session");
		assert.equal(lines[0].id, firstId);
		assert.equal(lines[0].parentSession, undefined);
		assert.equal(lines[1].type, "custom_message");
		assert.equal(lines[1].parentId, null);
		assert.equal(lines[1].details.executorSessionId, "executor-session");
		assert.match(lines[1].content, /intentionally not inherited/);
	} finally {
		if (session.file) rmSync(session.file, { force: true });
	}
});

test("formatRepairFollowUpMessage injects failed gate evidence without exposing protocol", () => {
	const message = formatRepairFollowUpMessage({
		runId: "manifest-dev-run",
		manifestPath: "/m",
		manifestSha256: "h",
		requestedAt: "start",
		completedAt: "end",
		cwd: "/repo",
		status: "failed",
		orchestratorSessionId: "manifest-verify-1",
		orchestratorSessionFile: "/tmp/manifest-verify-1.jsonl",
		results: [
			gateResult("PASS"),
			{ ...gateResult("FAIL"), gateId: "INV-G1", title: "Runtime boundary", evidence: "tool is visible", details: "remove it" },
		],
	});
	assert.match(message, /Harness verification found failed/);
	assert.match(message, /Verification orchestrator session: manifest-verify-1 \(\/tmp\/manifest-verify-1\.jsonl\)/);
	assert.match(message, /INV-G1 Runtime boundary: tool is visible/);
	assert.match(message, /Details: remove it/);
	assert.doesNotMatch(message, /manifest_dev_request_verification/);
	assert.doesNotMatch(message, /manifest_dev_report_outcome/);
	assert.doesNotMatch(message, /AC-1\.1 Thing works/);
});

test("routeVerificationResult injects repair, blocked, and done runtime outcomes", async () => {
	const routeRunStateFile = `${process.env.HOME}/.manifest-dev/runs/manifest-dev-route-test.json`;
	rmSync(routeRunStateFile, { force: true });
	const makePi = () => {
		const calls = { entries: [], userMessages: [], messages: [], notifications: [] };
		return {
			calls,
			pi: {
				appendEntry(customType, data) { calls.entries.push({ customType, data }); },
				sendUserMessage(message, options) { calls.userMessages.push({ message, options }); },
				sendMessage(message, options) { calls.messages.push({ message, options }); },
			},
		};
	};
	const routeTmpDir = mkdtempSync(`${tmpdir()}/manifest-dev-route-`);
	const routeManifest = `${routeTmpDir}/manifest.md`;
	writeFileSync(routeManifest, "# Manifest", "utf-8");
	const ctx = {
		cwd: process.cwd(),
		ui: { notify(message, level) { void message; void level; } },
	};
	const baseRun = {
		runId: "manifest-dev-route-test",
		command: "do",
		startedAt: "2026-06-05T00:00:00.000Z",
		cwd: process.cwd(),
		executorSessionId: "executor-session",
		status: "verifying",
		verificationAttempts: 1,
	};
	const makeState = () => ({
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map([[baseRun.executorSessionId, baseRun]]),
		childSessionIds: new Set(),
	});
	const verification = (status, results) => ({
		runId: baseRun.runId,
		manifestPath: routeManifest,
		manifestSha256: sha256("# Manifest"),
		requestedAt: "start",
		completedAt: "end",
		cwd: process.cwd(),
		status,
		orchestratorSessionId: "manifest-verify-1",
		results,
	});

	const failedPi = makePi();
	await routeVerificationResult(failedPi.pi, ctx, makeState(), baseRun, verification("failed", [
		{ ...gateResult("FAIL"), gateId: "AC-2.1", title: "Runtime internals", evidence: "still exposed", details: "hide it" },
	]));
	assert.equal(failedPi.calls.userMessages.length, 1);
	assert.match(failedPi.calls.userMessages[0].message, /AC-2\.1 Runtime internals: still exposed/);
	assert.deepEqual(failedPi.calls.userMessages[0].options, { deliverAs: "followUp" });
	assert.equal(failedPi.calls.entries.some((entry) => entry.customType === "manifest-dev:verification"), true);
	assert.equal(failedPi.calls.entries.some((entry) => entry.customType === "manifest-dev:run" && entry.data.status === "repairing"), true);

	const blockedPi = makePi();
	await routeVerificationResult(blockedPi.pi, ctx, makeState(), baseRun, verification("blocked", [
		gateResult("PASS"),
		{ ...gateResult("BLOCKED"), gateId: "INV-G2", evidence: "verifier subprocess unavailable" },
	]));
	assert.equal(blockedPi.calls.messages.length, 1);
	assert.match(blockedPi.calls.messages[0].message.content, /verification is blocked/);
	assert.match(blockedPi.calls.messages[0].message.content, /INV-G2: verifier subprocess unavailable/);
	assert.doesNotMatch(blockedPi.calls.messages[0].message.content, /AC-1\.1: PASS evidence/);
	const blockedOutcome = blockedPi.calls.entries.find((entry) => entry.customType === "manifest-dev:outcome" && entry.data.outcome === "escalate");
	assert.ok(blockedOutcome);
	assert.deepEqual(blockedOutcome.data.blockers, ["INV-G2: verifier subprocess unavailable"]);
	assert.equal(blockedPi.calls.entries.some((entry) => entry.customType === "manifest-dev:run" && entry.data.status === "blocked"), true);

	const passedPi = makePi();
	await routeVerificationResult(passedPi.pi, ctx, makeState(), baseRun, verification("passed", [gateResult("PASS")]));
	assert.equal(passedPi.calls.messages.length, 1);
	assert.match(passedPi.calls.messages[0].message.content, /Manifest-dev done/);
	assert.equal(passedPi.calls.entries.some((entry) => entry.customType === "manifest-dev:outcome" && entry.data.outcome === "done"), true);
	assert.equal(passedPi.calls.entries.some((entry) => entry.customType === "manifest-dev:run" && entry.data.status === "done"), true);

	writeFileSync(routeManifest, "# Changed Manifest", "utf-8");
	const stalePi = makePi();
	await routeVerificationResult(stalePi.pi, ctx, makeState(), baseRun, verification("passed", [gateResult("PASS")]));
	assert.equal(stalePi.calls.messages.length, 0);
	assert.equal(stalePi.calls.userMessages.length, 1);
	assert.match(stalePi.calls.userMessages[0].message, /became stale before done/);
	assert.equal(stalePi.calls.entries.some((entry) => entry.customType === "manifest-dev:outcome" && entry.data.outcome === "done"), false);
	assert.deepEqual(
		stalePi.calls.entries
			.filter((entry) => entry.customType === "manifest-dev:run")
			.map((entry) => entry.data.status),
		["repairing"],
	);
	rmSync(routeRunStateFile, { force: true });
	rmSync(routeTmpDir, { recursive: true, force: true });
});

test("buildManifestBabysitPrompt --ci sets pending cadence but does NOT carry the verifier token", () => {
	const run = { runId: "manifest-dev-run", manifestPath: "/tmp/m.md", manifestSha256: "h" };
	const url = "https://github.com/o/r/pull/1";
	const ciPrompt = buildManifestBabysitPrompt(run, url, `${url} --ci`);
	assert.match(ciPrompt, /CI one-shot mode/);
	assert.match(ciPrompt, /pending/);
	// The WAIT-PENDING token is a verifier->runtime contract injected into the VERIFIER
	// prompt by the runtime, not the executor prompt — the verifier never reads this prompt.
	assert.doesNotMatch(ciPrompt, /WAIT-PENDING/);
	assert.doesNotMatch(buildManifestBabysitPrompt(run, url, url), /WAIT-PENDING/);
});

test("buildGateVerifierPrompt injects the WAIT-PENDING rule only when ciOneShot", () => {
	const gate = { id: "AC-1.1", kind: "acceptance_criterion", title: "PR lifecycle", verifyPrompt: "Activate the check-pr skill." };
	const base = { gate, manifestPath: "/m", manifest: "# M", runId: "r" };
	const ciPrompt = buildGateVerifierPrompt({ ...base, ciOneShot: true });
	assert.match(ciPrompt, /WAIT-PENDING/);
	assert.match(ciPrompt, /bash sleep <N>; reinvoke/);
	// Off by default — non-ci runs and other gates get the plain verifier contract.
	assert.doesNotMatch(buildGateVerifierPrompt(base), /WAIT-PENDING/);
	assert.doesNotMatch(buildGateVerifierPrompt({ ...base, ciOneShot: false }), /WAIT-PENDING/);
});

test("isWaitPendingVerification accepts the marker on FAIL or BLOCKED non-PASS gates", () => {
	const verification = (results) => ({ runId: "r", status: "failed", results });
	const waitFail = { ...gateResult("FAIL"), gateId: "AC-1.1", evidence: "Reviewer pending. WAIT-PENDING" };
	const waitBlocked = { ...gateResult("BLOCKED"), gateId: "AC-1.1", evidence: "Reviewer pending (human). WAIT-PENDING" };
	const realFail = { ...gateResult("FAIL"), gateId: "AC-1.2", evidence: "broken test" };
	assert.equal(isWaitPendingVerification(verification([waitFail])), true);
	// A reviewer/CI wait classified as BLOCKED must still count as wait-only.
	assert.equal(isWaitPendingVerification(verification([waitBlocked])), true);
	assert.equal(isWaitPendingVerification(verification([gateResult("PASS"), waitBlocked])), true);
	// Mixed wait + real (unmarked) failure is not wait-only — the normal path still runs.
	assert.equal(isWaitPendingVerification(verification([waitFail, realFail])), false);
	// No non-PASS gates at all is not wait-pending.
	assert.equal(isWaitPendingVerification(verification([gateResult("PASS")])), false);
});

test("buildCiPendingSummary frames the exit as pending, not blocked, and lists the waits", () => {
	const summary = buildCiPendingSummary({
		runId: "r", status: "failed",
		results: [{ ...gateResult("FAIL"), gateId: "AC-1.1", evidence: "Reviewer @bob pending. WAIT-PENDING" }],
	});
	assert.match(summary, /CI one-shot/);
	assert.match(summary, /Exiting pending instead of looping repair/);
	assert.match(summary, /Re-run \/babysit-pr --ci/);
	assert.match(summary, /AC-1\.1: Reviewer @bob pending/);
});

test("routeVerificationResult exits pending (no repair) for a --ci wait-only failure", async () => {
	const routeRunStateFile = `${process.env.HOME}/.manifest-dev/runs/manifest-dev-ci-pending.json`;
	rmSync(routeRunStateFile, { force: true });
	const calls = { entries: [], userMessages: [], messages: [] };
	const pi = {
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		sendUserMessage(message, options) { calls.userMessages.push({ message, options }); },
		sendMessage(message, options) { calls.messages.push({ message, options }); },
	};
	const tmp = mkdtempSync(`${tmpdir()}/manifest-dev-ci-`);
	const manifestPath = `${tmp}/manifest.md`;
	writeFileSync(manifestPath, "# Manifest", "utf-8");
	const ctx = { cwd: process.cwd(), ui: { notify() {} } };
	const run = {
		runId: "manifest-dev-ci-pending", command: "babysit-pr", startedAt: "t",
		cwd: process.cwd(), executorSessionId: "executor-session", status: "verifying",
		verificationAttempts: 1, ciOneShot: true,
	};
	const state = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map([[run.executorSessionId, run]]),
		childSessionIds: new Set(),
	};
	const verification = {
		runId: run.runId, manifestPath, manifestSha256: sha256("# Manifest"),
		requestedAt: "s", completedAt: "e", cwd: process.cwd(), status: "failed",
		orchestratorSessionId: "manifest-verify-1",
		results: [{ ...gateResult("FAIL"), gateId: "AC-1.1", title: "PR lifecycle", evidence: "Reviewer @bob pending; CI green. WAIT-PENDING" }],
	};
	try {
		await routeVerificationResult(pi, ctx, state, run, verification);
		// No repair injection.
		assert.equal(calls.userMessages.length, 0);
		// A pending status message instead.
		assert.equal(calls.messages.length, 1);
		assert.match(calls.messages[0].message.content, /Exiting pending instead of looping repair/);
		// Outcome recorded as a (resumable) escalate flavored pending; run left blocked.
		assert.equal(calls.entries.some((e) => e.customType === "manifest-dev:outcome" && e.data.summary === "CI one-shot pending on external wait."), true);
		assert.equal(calls.entries.some((e) => e.customType === "manifest-dev:run" && e.data.status === "blocked"), true);
	} finally {
		rmSync(routeRunStateFile, { force: true });
		rmSync(tmp, { recursive: true, force: true });
	}
});

test("routeVerificationResult exits pending for a --ci wait-only BLOCKED verification (not generic escalation)", async () => {
	const routeRunStateFile = `${process.env.HOME}/.manifest-dev/runs/manifest-dev-ci-blocked.json`;
	rmSync(routeRunStateFile, { force: true });
	const calls = { entries: [], userMessages: [], messages: [] };
	const pi = {
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		sendUserMessage(message, options) { calls.userMessages.push({ message, options }); },
		sendMessage(message, options) { calls.messages.push({ message, options }); },
	};
	const tmp = mkdtempSync(`${tmpdir()}/manifest-dev-ci-`);
	const manifestPath = `${tmp}/manifest.md`;
	writeFileSync(manifestPath, "# Manifest", "utf-8");
	const ctx = { cwd: process.cwd(), ui: { notify() {} } };
	const run = {
		runId: "manifest-dev-ci-blocked", command: "babysit-pr", startedAt: "t",
		cwd: process.cwd(), executorSessionId: "executor-session", status: "verifying",
		verificationAttempts: 1, ciOneShot: true,
	};
	const state = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map([[run.executorSessionId, run]]),
		childSessionIds: new Set(),
	};
	// Verifier classified the reviewer/CI wait as BLOCKED (human/external) — aggregate
	// status is "blocked", but the WAIT-PENDING marker must still route to pending.
	const verification = {
		runId: run.runId, manifestPath, manifestSha256: sha256("# Manifest"),
		requestedAt: "s", completedAt: "e", cwd: process.cwd(), status: "blocked",
		orchestratorSessionId: "manifest-verify-1",
		results: [{ ...gateResult("BLOCKED"), gateId: "AC-1.1", title: "PR lifecycle", evidence: "Reviewer @bob pending (human decision); CI green. WAIT-PENDING" }],
	};
	try {
		await routeVerificationResult(pi, ctx, state, run, verification);
		assert.equal(calls.userMessages.length, 0); // no repair
		assert.equal(calls.messages.length, 1);
		assert.match(calls.messages[0].message.content, /Exiting pending instead of looping repair/);
		assert.equal(calls.entries.some((e) => e.customType === "manifest-dev:outcome" && e.data.summary === "CI one-shot pending on external wait."), true);
	} finally {
		rmSync(routeRunStateFile, { force: true });
		rmSync(tmp, { recursive: true, force: true });
	}
});

test("routeVerificationResult still repairs a --ci failure that is not wait-only", async () => {
	const routeRunStateFile = `${process.env.HOME}/.manifest-dev/runs/manifest-dev-ci-repair.json`;
	rmSync(routeRunStateFile, { force: true });
	const calls = { userMessages: [], messages: [], entries: [] };
	const pi = {
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		sendUserMessage(message, options) { calls.userMessages.push({ message, options }); },
		sendMessage(message, options) { calls.messages.push({ message, options }); },
	};
	const ctx = { cwd: process.cwd(), ui: { notify() {} } };
	const run = {
		runId: "manifest-dev-ci-repair", command: "babysit-pr", startedAt: "t",
		cwd: process.cwd(), executorSessionId: "executor-session", status: "verifying",
		verificationAttempts: 1, ciOneShot: true,
	};
	const state = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map([[run.executorSessionId, run]]),
		childSessionIds: new Set(),
	};
	const verification = {
		runId: run.runId, manifestPath: "/m", manifestSha256: "h", requestedAt: "s", completedAt: "e",
		cwd: process.cwd(), status: "failed", orchestratorSessionId: "manifest-verify-1",
		results: [{ ...gateResult("FAIL"), gateId: "AC-1.1", title: "PR lifecycle", evidence: "merge conflict — fix it" }],
	};
	try {
		await routeVerificationResult(pi, ctx, state, run, verification);
		// Not wait-only → normal repair injection, no pending status message.
		assert.equal(calls.userMessages.length, 1);
		assert.match(calls.userMessages[0].message, /AC-1\.1 PR lifecycle: merge conflict/);
		assert.equal(calls.messages.length, 0);
	} finally {
		rmSync(routeRunStateFile, { force: true });
	}
});

test("routeVerificationResult escalates (not pending) for a --ci BLOCKED verification WITHOUT the marker", async () => {
	// Pairs the BLOCKED+WAIT-PENDING positive test: a ciOneShot blocked verification with no
	// marker must take the generic blocked/escalation path, proving the marker — not merely
	// the blocked status — is what routes to pending.
	const routeRunStateFile = `${process.env.HOME}/.manifest-dev/runs/manifest-dev-ci-escalate.json`;
	rmSync(routeRunStateFile, { force: true });
	const calls = { userMessages: [], messages: [], entries: [] };
	const pi = {
		appendEntry(customType, data) { calls.entries.push({ customType, data }); },
		sendUserMessage(message, options) { calls.userMessages.push({ message, options }); },
		sendMessage(message, options) { calls.messages.push({ message, options }); },
	};
	const ctx = { cwd: process.cwd(), ui: { notify() {} } };
	const run = {
		runId: "manifest-dev-ci-escalate", command: "babysit-pr", startedAt: "t",
		cwd: process.cwd(), executorSessionId: "executor-session", status: "verifying",
		verificationAttempts: 1, ciOneShot: true,
	};
	const state = {
		latestVerificationByRunId: new Map(),
		activeRunByExecutorSessionId: new Map([[run.executorSessionId, run]]),
		childSessionIds: new Set(),
	};
	const verification = {
		runId: run.runId, manifestPath: "/m", manifestSha256: "h", requestedAt: "s", completedAt: "e",
		cwd: process.cwd(), status: "blocked", orchestratorSessionId: "manifest-verify-1",
		results: [{ ...gateResult("BLOCKED"), gateId: "AC-1.1", title: "PR lifecycle", evidence: "Needs maintainer secret to retrigger; no WAIT marker here" }],
	};
	try {
		await routeVerificationResult(pi, ctx, state, run, verification);
		assert.equal(calls.userMessages.length, 0); // no repair
		// Generic blocked status message, NOT the pending summary.
		assert.equal(calls.messages.length, 1);
		assert.match(calls.messages[0].message.content, /is blocked for/);
		assert.doesNotMatch(calls.messages[0].message.content, /Exiting pending instead of looping repair/);
		// Generic blocked outcome, not the CI pending outcome.
		assert.equal(calls.entries.some((e) => e.customType === "manifest-dev:outcome" && e.data.summary === "Harness verification is blocked."), true);
		assert.equal(calls.entries.some((e) => e.customType === "manifest-dev:outcome" && e.data.summary === "CI one-shot pending on external wait."), false);
	} finally {
		rmSync(routeRunStateFile, { force: true });
	}
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
