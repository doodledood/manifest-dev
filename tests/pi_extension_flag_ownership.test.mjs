import test from "node:test";
import assert from "node:assert/strict";
import manifestDevExtension, { launchFlagFromArgv } from "../pi/extensions/manifest-dev.ts";
import manifestDevToolsExtension from "../packages/manifest-dev-pi-tools/pi/extensions/manifest-dev-tools.ts";

const VERIFIER_FLAGS = [
	"manifest-verifier-max-concurrent",
];

function makePi() {
	const flags = [];
	return {
		flags,
		events: { on() {} },
		registerFlag(name) { flags.push(name); },
		getFlag() { return undefined; },
		on() {},
		registerCommand() {},
	};
}

// Grounded in the real Pi loader (loader.js): getFlag is gated on the CALLING
// extension having registered the flag (`extension.flags.has(name)`), values live in a
// shared per-load-cycle `runtime.flagValues` map, and that runtime is rebuilt on every
// loadExtensions() call. So a single static owner is correct and needs no marker:
// only the core extension registers the --manifest-verifier-* flags, on every load.
test("only the core extension registers the verifier flags", () => {
	const core = makePi();
	const tools = makePi();

	manifestDevExtension(core);
	manifestDevToolsExtension(tools);

	for (const flag of VERIFIER_FLAGS) {
		assert.equal(core.flags.filter((name) => name === flag).length, 1, `core registers ${flag} once`);
		assert.equal(tools.flags.includes(flag), false, `tools never registers ${flag}`);
	}
});

// Registration is unconditional (no globalThis marker), so a second load cycle in the
// same process still registers the flags — Pi gives each loadExtensions() a fresh
// runtime, so a persisted marker would have left the second cycle with no flags.
test("a second core load still registers the flags (no persisted marker)", () => {
	const first = makePi();
	const second = makePi();
	manifestDevExtension(first);
	manifestDevExtension(second);
	for (const flag of VERIFIER_FLAGS) {
		assert.equal(second.flags.includes(flag), true, `${flag} registered on the second load`);
	}
});

// The tools extension is gated out of getFlag for these flags (it never registers
// them), so /babysit-pr recovers the launch value from process.argv (process-global,
// independent of per-extension flag gating).
test("launchFlagFromArgv reads --name value and --name=value forms", () => {
	assert.equal(
		launchFlagFromArgv("manifest-verifier-max-concurrent", [
			"node", "pi", "-e", "/repo", "--manifest-verifier-max-concurrent", "3",
		]),
		"3",
	);
	assert.equal(
		launchFlagFromArgv("manifest-verifier-max-concurrent", [
			"node", "pi", "--manifest-verifier-max-concurrent=42",
		]),
		"42",
	);
	assert.equal(launchFlagFromArgv("manifest-verifier-max-concurrent", ["node", "pi", "-e", "/repo"]), undefined);
});
