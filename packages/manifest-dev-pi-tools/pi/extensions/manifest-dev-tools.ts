import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
// Reuses the shared Harness-level Do runtime from the core package
// (@doodledood/manifest-dev-pi, declared in package.json dependencies). Pi
// installs manifest-dev as the whole repo, so the in-repo relative path is the
// resolved location of the dependency.
import {
	createRuntimeState,
	startWrapper,
	wireRuntimeHooks,
	type ManifestCommand,
} from "../../../../pi/extensions/manifest-dev.ts";

/** Commands owned by the tools (`@doodledood/manifest-dev-pi-tools`) package. */
const TOOLS_COMMANDS: ReadonlySet<ManifestCommand> = new Set<ManifestCommand>(["babysit-pr"]);

export default function manifestDevToolsExtension(pi: ExtensionAPI): void {
	const state = createRuntimeState();
	// The tools extension does NOT register the --manifest-verifier-* flags: the core
	// extension is their single public owner, so registering here would list each flag
	// twice in `pi --help` (Pi loads each extension as a fresh module instance, so the
	// two can't share an in-module owner guard). /babysit-pr still honors the overrides
	// because resolveVerifierConfig reads the launch values from process.argv when this
	// extension's getFlag doesn't have them. Wire hooks scoped to babysit-pr runs so it
	// never double-verifies the core package's /do or /auto runs.
	wireRuntimeHooks(pi, state, TOOLS_COMMANDS);

	pi.registerCommand("babysit-pr", {
		description: "Synthesize a PR lifecycle manifest and run Harness-level Do for a GitHub PR.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "babysit-pr", rawArgs, ctx, state);
		},
	});
}
