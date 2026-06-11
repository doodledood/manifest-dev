// manifest-dev OpenCode plugin.
//
// Registers the sibling `../skills` payload via `skills.paths` and the sibling
// `../AGENTS.md` via `instructions`, both resolved from this file's location so
// the clone can live anywhere. The `config` hook mutates the live merged config
// once at startup (verified on opencode 1.2.16 → 1.17.3; see ../README.md).
//
// Failure-soft by design: a missing asset logs a warning instead of throwing,
// because a throwing config hook would take down OpenCode startup for the
// user's every project.

import { existsSync } from "node:fs"
import { join } from "node:path"
import { fileURLToPath } from "node:url"

const distRoot = fileURLToPath(new URL("..", import.meta.url))

export const ManifestDevPlugin = async () => {
  return {
    config: async (cfg) => {
      try {
        const skillsDir = join(distRoot, "skills")
        if (existsSync(skillsDir)) {
          cfg.skills = cfg.skills ?? {}
          cfg.skills.paths = [...(cfg.skills.paths ?? []), skillsDir]
        } else {
          console.warn(`[manifest-dev] skills directory not found, skipping: ${skillsDir}`)
        }

        const agentsFile = join(distRoot, "AGENTS.md")
        if (existsSync(agentsFile)) {
          cfg.instructions = [...(cfg.instructions ?? []), agentsFile]
        } else {
          console.warn(`[manifest-dev] AGENTS.md not found, skipping: ${agentsFile}`)
        }
      } catch (error) {
        console.error(`[manifest-dev] config hook failed, continuing without manifest-dev: ${error}`)
      }
    },
  }
}
