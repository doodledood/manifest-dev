import test from "node:test";
import assert from "node:assert/strict";
import manifestDevToolsExtension from "../packages/manifest-dev-pi-tools/pi/extensions/manifest-dev-tools.ts";

test("tools extension registers babysit-pr and wires Harness verification hooks", () => {
	const events = new Map();
	const commands = new Map();
	const flags = [];
	const pi = {
		events: { on() {} },
		registerFlag(name) { flags.push(name); },
		on(name, handler) { events.set(name, handler); },
		registerCommand(name, command) { commands.set(name, command); },
	};

	// Loaded standalone here (no core extension first), so the tools extension owns and
	// registers the verifier flags itself — otherwise Pi rejects --manifest-verifier-*
	// as unknown before /babysit-pr runs. In the repo-root install core owns them and
	// this is a globalThis-guarded no-op. See pi_extension_flag_ownership.test.mjs.
	delete globalThis[Symbol.for("@doodledood/manifest-dev:verifier-flags-registered")];
	manifestDevToolsExtension(pi);

	// Tools owns only babysit-pr; do/auto stay in the core package.
	assert.equal(commands.has("babysit-pr"), true);
	assert.equal(commands.has("do"), false);
	assert.equal(commands.has("auto"), false);
	// It reuses the core runtime wiring (verification on executor checkpoint).
	assert.equal(typeof events.get("agent_end"), "function");
	assert.equal(typeof events.get("before_agent_start"), "function");
	assert.equal(typeof events.get("session_start"), "function");
	assert.equal(flags.includes("manifest-verifier-max-concurrent"), true);
	assert.equal(flags.includes("manifest-verifier-max-turns"), true);
	assert.equal(flags.includes("manifest-verifier-timeout-ms"), true);
});
