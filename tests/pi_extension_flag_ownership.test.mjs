import test from "node:test";
import assert from "node:assert/strict";
import manifestDevExtension, { launchFlagFromArgv } from "../pi/extensions/manifest-dev.ts";
import manifestDevToolsExtension from "../packages/manifest-dev-pi-tools/pi/extensions/manifest-dev-tools.ts";

const VERIFIER_FLAGS = [
	"manifest-verifier-max-turns",
	"manifest-verifier-timeout-ms",
	"manifest-verifier-max-concurrent",
];

// Process-wide ownership marker (kept on globalThis so it is shared across Pi's
// fresh per-extension module instances). Reset before each load-path simulation.
const OWNED = Symbol.for("@doodledood/manifest-dev:verifier-flags-registered");

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

// Repo-root install: both extensions load (core first). Core owns the flags; tools
// skips, so `pi --help` lists each --manifest-verifier-* flag exactly once (3, not 6).
test("repo-root load registers each verifier flag once (core owns, tools skips)", () => {
	delete globalThis[OWNED];
	const core = makePi();
	const tools = makePi();

	manifestDevExtension(core);
	manifestDevToolsExtension(tools);

	for (const flag of VERIFIER_FLAGS) {
		assert.equal(core.flags.filter((name) => name === flag).length, 1, `core registers ${flag} once`);
		assert.equal(tools.flags.includes(flag), false, `tools skips ${flag}`);
	}
});

// Standalone tools install (`pi -e packages/manifest-dev-pi-tools`): tools is the only
// loader, so it owns and registers the flags — otherwise Pi rejects --manifest-verifier-*
// as an unknown option before /babysit-pr can run.
test("standalone tools load registers the verifier flags itself", () => {
	delete globalThis[OWNED];
	const tools = makePi();

	manifestDevToolsExtension(tools);

	for (const flag of VERIFIER_FLAGS) {
		assert.equal(tools.flags.includes(flag), true, `tools registers ${flag} when standalone`);
	}
});

// The non-owning extension recovers the launch value from process.argv (process-global,
// shared across module instances) so /babysit-pr honors overrides without re-registering.
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
