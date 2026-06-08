import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import manifestDevExtension, {
	buildManifestAutoPrompt,
	buildManifestBabysitPrompt,
	buildManifestDoPrompt,
	buildOrchestrationSpawnBlocker,
	createVerificationOrchestratorSession,
	buildCiPendingSummary,
	formatRepairFollowUpMessage,
	isStaleSessionContextError,
	isWaitPendingFailure,
	makeOrchestratorSessionId,
	rehydrateRuntimeState,
	resolveManifestPath,
	routeVerificationResult,
	shouldTriggerHarnessVerification,
	spawnVerifier,
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
	waitForVerifierRecords,
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

test("buildGateVerifierPrompt creates a single-gate clean-session contract", () => {
	const prompt = buildGateVerifierPrompt({
		gate,
		manifestPath: "/tmp/manifest.md",
		manifest: "# Manifest",
		runId: "manifest-dev-abc123",
		implementationSummary: "Changed extension runtime.",
		orchestratorSessionId: "manifest-verify-123",
	});

	assert.match(prompt, /clean Pi subagent session/);
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
	assert.equal(record.results[0].details, "subagents service missing");

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
	writeFileSync(manifestPath, `# Manifest\n\n## 6. Deliverables\n### Deliverable 1: X\n**Acceptance Criteria:**\n- [AC-1.1] X works\n  \`\`\`yaml\n  verify:\n    prompt: "Check X"\n  \`\`\`\n`, "utf-8");
	const ctx = {
		cwd: dir,
		sessionManager: { getSessionId() { return "executor-session"; } },
		isIdle() { return true; },
		hasPendingMessages() { return false; },
		ui: { notify() {} },
	};
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
		{ ...gateResult("BLOCKED"), gateId: "INV-G2", evidence: "subagents unavailable" },
	]));
	assert.equal(blockedPi.calls.messages.length, 1);
	assert.match(blockedPi.calls.messages[0].message.content, /verification is blocked/);
	assert.match(blockedPi.calls.messages[0].message.content, /INV-G2: subagents unavailable/);
	assert.doesNotMatch(blockedPi.calls.messages[0].message.content, /AC-1\.1: PASS evidence/);
	const blockedOutcome = blockedPi.calls.entries.find((entry) => entry.customType === "manifest-dev:outcome" && entry.data.outcome === "escalate");
	assert.ok(blockedOutcome);
	assert.deepEqual(blockedOutcome.data.blockers, ["INV-G2: subagents unavailable"]);
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

test("spawnVerifier returns the agentId on success and the error on failure (no retry)", () => {
	let calls = 0;
	const ok = spawnVerifier({ spawn() { calls += 1; return "agent-1"; } }, "general-purpose", "verify", { maxTurns: 5 });
	assert.deepEqual(ok, { ok: true, agentId: "agent-1" });
	assert.equal(calls, 1);

	// A stale-context throw is surfaced immediately — no retry, because the subagents
	// service only refreshes its stored ctx on a session lifecycle event, not in a tick.
	let failCalls = 0;
	const fail = spawnVerifier({ spawn() { failCalls += 1; throw new Error("ctx is stale after session replacement or reload"); } }, "general-purpose", "verify", undefined);
	assert.equal(fail.ok, false);
	assert.equal(failCalls, 1);
	assert.equal(isStaleSessionContextError(fail.error), true);
});

test("buildOrchestrationSpawnBlocker names a harness spawn failure and the stale-context cause", () => {
	const run = {
		runId: "manifest-dev-run",
		command: "do",
		startedAt: "t",
		cwd: "/repo",
		executorSessionId: "executor-session",
		status: "verifying",
	};
	const stale = buildOrchestrationSpawnBlocker(run, "current-session", new Error("This extension ctx is stale after session replacement or reload."));
	assert.match(stale, /harness\/runtime orchestration failure/);
	assert.match(stale, /no Acceptance Criterion or Global Invariant was verified/);
	assert.match(stale, /current session current-session, executor session executor-session/);
	assert.match(stale, /stored session context was invalidated/);

	// Non-stale spawn errors omit the session-replacement cause line.
	const other = buildOrchestrationSpawnBlocker(run, "s", new Error("No model registry available."));
	assert.doesNotMatch(other, /stored session context was invalidated/);
});

test("buildManifestBabysitPrompt --ci instructs the verifier to emit WAIT-PENDING", () => {
	const run = { runId: "manifest-dev-run", manifestPath: "/tmp/m.md", manifestSha256: "h" };
	const url = "https://github.com/o/r/pull/1";
	const ciPrompt = buildManifestBabysitPrompt(run, url, `${url} --ci`);
	assert.match(ciPrompt, /CI one-shot mode/);
	assert.match(ciPrompt, /WAIT-PENDING/);
	// Default (no --ci) does not mention the marker.
	assert.doesNotMatch(buildManifestBabysitPrompt(run, url, url), /WAIT-PENDING/);
});

test("isWaitPendingFailure requires every FAIL gate to carry the WAIT-PENDING marker", () => {
	const verification = (results) => ({ runId: "r", status: "failed", results });
	const waitFail = { ...gateResult("FAIL"), gateId: "AC-1.1", evidence: "Reviewer pending. WAIT-PENDING" };
	const realFail = { ...gateResult("FAIL"), gateId: "AC-1.2", evidence: "broken test" };
	assert.equal(isWaitPendingFailure(verification([waitFail])), true);
	assert.equal(isWaitPendingFailure(verification([gateResult("PASS"), waitFail])), true);
	// Mixed wait + real failure is not wait-only — repair must still run.
	assert.equal(isWaitPendingFailure(verification([waitFail, realFail])), false);
	// No FAIL gates at all is not a wait-pending failure.
	assert.equal(isWaitPendingFailure(verification([gateResult("PASS")])), false);
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

test("routeVerificationResult still repairs a --ci failure that is not wait-only", async () => {
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
	await routeVerificationResult(pi, ctx, state, run, verification);
	// Not wait-only → normal repair injection, no pending status message.
	assert.equal(calls.userMessages.length, 1);
	assert.match(calls.userMessages[0].message, /AC-1\.1 PR lifecycle: merge conflict/);
	assert.equal(calls.messages.length, 0);
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
