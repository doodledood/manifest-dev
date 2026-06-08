import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
// Reuses the shared Harness-level Do runtime from the core package. This extension is
// loaded only from the repo-root `pi.extensions` (it has no standalone `pi.extensions`),
// so the core source is always present at this in-repo relative path.
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
	// extension owns them (it always loads alongside in the repo-root install), so this
	// would just double the `pi --help` entries. /babysit-pr still honors the overrides
	// because resolveVerifierConfig reads the launch values from process.argv. Wire hooks
	// scoped to babysit-pr runs so it never double-verifies core's /do or /auto runs.
	wireRuntimeHooks(pi, state, TOOLS_COMMANDS);

	pi.registerCommand("babysit-pr", {
		description: "Synthesize a PR lifecycle manifest and run Harness-level Do for a GitHub PR.",
		handler: async (rawArgs, ctx) => {
			await startWrapper(pi, "babysit-pr", rawArgs, ctx, state);
		},
	});
}
