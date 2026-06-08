import test from "node:test";
import assert from "node:assert/strict";
import manifestDevExtension from "../pi/extensions/manifest-dev.ts";
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

// In the repo-root install Pi loads BOTH extensions from the same shared module.
// Each verifier flag must be registered exactly once (a single public owner) so
// `pi --help` does not list every --manifest-verifier-* flag twice.
test("repo-root install registers each verifier flag once across both extensions", () => {
	const core = makePi();
	const tools = makePi();

	// Core loads first (listed first in the repo-root pi.extensions), so it owns the flags.
	manifestDevExtension(core);
	manifestDevToolsExtension(tools);

	for (const flag of VERIFIER_FLAGS) {
		assert.equal(core.flags.filter((name) => name === flag).length, 1);
		// The tools extension does not re-register — it reads parsed values through the owner.
		assert.equal(tools.flags.includes(flag), false);
	}
});
