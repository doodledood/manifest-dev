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
	// Pi's getFlag only returns values for flags registered by THIS extension, so
	// the tools extension must register the verifier flags itself for /babysit-pr
	// to honor --manifest-verifier-* overrides (it would otherwise fall back to
	// defaults). Then wire its own hooks, scoped to babysit-pr runs so it never
	// double-verifies the core package's /do or /auto runs.
	registerVerifierFlags(pi);
	wireRuntimeHooks(pi, state, TOOLS_COMMANDS);

	pi.registerCommand("babysit-pr", {
		description: "Synthesize a PR lifecycle manifest and run Harness-level Do for a GitHub PR.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "babysit-pr", rawArgs, ctx, state);
		},
	});
}
