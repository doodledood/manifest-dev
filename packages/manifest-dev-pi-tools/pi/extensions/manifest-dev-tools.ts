import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
// Reuses the shared Harness-level Do runtime from the core package
// (@doodledood/manifest-dev-pi, declared in package.json dependencies). Pi
// installs manifest-dev as the whole repo, so the in-repo relative path is the
// resolved location of the dependency.
import {
	createRuntimeState,
	registerVerifierFlags,
	startWrapper,
	wireRuntimeHooks,
	type ManifestCommand,
} from "../../../../pi/extensions/manifest-dev.ts";

/** Commands owned by the tools (`@doodledood/manifest-dev-pi-tools`) package. */
const TOOLS_COMMANDS: ReadonlySet<ManifestCommand> = new Set<ManifestCommand>(["babysit-pr"]);

export default function manifestDevToolsExtension(pi: ExtensionAPI): void {
	const state = createRuntimeState();
	// registerVerifierFlags claims a single owner per process via a globalThis marker
	// (Pi loads each extension as a fresh module instance, so module-level state isn't
	// shared, but globalThis is). In the repo-root install core loads first and owns the
	// flags, so this call is a no-op (one `pi --help` entry) and /babysit-pr reads the
	// values via the process.argv fallback. In a standalone tools install this call owns
	// and registers the flags, so Pi accepts the --manifest-verifier-* overrides. Wire
	// hooks scoped to babysit-pr runs so it never double-verifies core's /do or /auto runs.
	registerVerifierFlags(pi);
	wireRuntimeHooks(pi, state, TOOLS_COMMANDS);

	pi.registerCommand("babysit-pr", {
		description: "Synthesize a PR lifecycle manifest and run Harness-level Do for a GitHub PR.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "babysit-pr", rawArgs, ctx, state);
		},
	});
}
