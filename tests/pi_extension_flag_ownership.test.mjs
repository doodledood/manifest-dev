import test from "node:test";
import assert from "node:assert/strict";
import manifestDevExtension, { launchFlagFromArgv } from "../pi/extensions/manifest-dev.ts";
import manifestDevToolsExtension from "../packages/manifest-dev-pi-tools/pi/extensions/manifest-dev-tools.ts";

const VERIFIER_FLAGS = [
	"manifest-verifier-max-turns",
	"manifest-verifier-timeout-ms",
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

// The de-dup is STATIC: only the core extension registers the verifier flags, and
// the tools extension never does. This holds regardless of how Pi loads the modules
// (Pi gives each extension a fresh module instance, so an in-module owner guard
// would NOT be shared between them — the single owner must be a compile-time decision,
// not runtime state). So `pi --help` lists each --manifest-verifier-* flag exactly once.
test("only the core extension registers the verifier flags (single static owner)", () => {
	const core = makePi();
	const tools = makePi();

	manifestDevExtension(core);
	manifestDevToolsExtension(tools);

	for (const flag of VERIFIER_FLAGS) {
		assert.equal(core.flags.filter((name) => name === flag).length, 1, `core registers ${flag} once`);
		assert.equal(tools.flags.includes(flag), false, `tools does not register ${flag}`);
	}
	// Combined, the repo-root install publishes each flag exactly once (3, not 6).
	const combined = [...core.flags, ...tools.flags].filter((name) => VERIFIER_FLAGS.includes(name));
	assert.equal(combined.length, VERIFIER_FLAGS.length);
});

// The tools extension recovers the launch value from process.argv (process-global,
// shared across module instances) instead of registering its own flag — so
// /babysit-pr --manifest-verifier-max-concurrent N is honored without a second
// --help entry.
test("launchFlagFromArgv reads --name value and --name=value forms", () => {
	assert.equal(
		launchFlagFromArgv("manifest-verifier-max-concurrent", [
			"node", "pi", "-e", "/repo", "--manifest-verifier-max-concurrent", "3",
		]),
		"3",
	);
	assert.equal(
		launchFlagFromArgv("manifest-verifier-max-turns", [
			"node", "pi", "--manifest-verifier-max-turns=42",
		]),
		"42",
	);
	assert.equal(launchFlagFromArgv("manifest-verifier-timeout-ms", ["node", "pi", "-e", "/repo"]), undefined);
});
