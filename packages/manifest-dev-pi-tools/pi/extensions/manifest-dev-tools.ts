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
	// registerVerifierFlags has a single public owner: in the repo-root install the
	// core extension loads first and publishes the --manifest-verifier-* flags, so
	// this call is a no-op (no duplicate flags in `pi --help`) and /babysit-pr reads
	// the parsed values through the core owner. In a standalone tools install this
	// call publishes the flags itself. Then wire hooks scoped to babysit-pr runs so
	// it never double-verifies the core package's /do or /auto runs.
	registerVerifierFlags(pi);
	wireRuntimeHooks(pi, state, TOOLS_COMMANDS);

	pi.registerCommand("babysit-pr", {
		description: "Synthesize a PR lifecycle manifest and run Harness-level Do for a GitHub PR.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "babysit-pr", rawArgs, ctx, state);
		},
	});
}
