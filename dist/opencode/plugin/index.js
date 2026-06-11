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

import { existsSync, readdirSync, readFileSync } from "node:fs"
import { join } from "node:path"
import { fileURLToPath } from "node:url"

const distRoot = fileURLToPath(new URL("..", import.meta.url))

const stripYamlQuotes = (value) => {
  const trimmed = value.trim()
  if (trimmed.length >= 2) {
    const first = trimmed[0]
    const last = trimmed[trimmed.length - 1]
    if ((first === "'" && last === "'") || (first === '"' && last === '"')) {
      return trimmed.slice(1, -1)
    }
  }
  return trimmed
}

const parseFrontmatter = (content) => {
  if (!content.startsWith("---")) return {}
  const end = content.indexOf("\n---", 3)
  if (end === -1) return {}

  const frontmatter = {}
  for (const line of content.slice(3, end).split("\n")) {
    if (!line || line.startsWith(" ") || !line.includes(":")) continue
    const separator = line.indexOf(":")
    const key = line.slice(0, separator).trim()
    const value = line.slice(separator + 1).trim()
    frontmatter[key] = stripYamlQuotes(value)
  }
  return frontmatter
}

const discoverCommandSkills = (skillsDir) => {
  const commands = []
  for (const entry of readdirSync(skillsDir, { withFileTypes: true })) {
    if (!entry.isDirectory()) continue

    const skillPath = join(skillsDir, entry.name, "SKILL.md")
    if (!existsSync(skillPath)) continue

    const frontmatter = parseFrontmatter(readFileSync(skillPath, "utf8"))
    const name = frontmatter.name ?? entry.name
    const description = frontmatter.description
    const userInvocable = (frontmatter["user-invocable"] ?? "true").toLowerCase()

    if (!description || userInvocable === "false") continue
    commands.push({ name, description })
  }
  return commands.sort((a, b) => a.name.localeCompare(b.name))
}

const registerSkillCommandWrappers = (cfg, skillsDir) => {
  cfg.command = cfg.command ?? {}
  for (const skill of discoverCommandSkills(skillsDir)) {
    if (Object.prototype.hasOwnProperty.call(cfg.command, skill.name)) continue
    cfg.command[skill.name] = {
      description: skill.description,
      template: `Use the ${skill.name} skill with: $ARGUMENTS`,
    }
  }
}

export const ManifestDevPlugin = async () => {
  return {
    config: async (cfg) => {
      try {
        const skillsDir = join(distRoot, "skills")
        if (existsSync(skillsDir)) {
          cfg.skills = cfg.skills ?? {}
          cfg.skills.paths = [...(cfg.skills.paths ?? []), skillsDir]
          registerSkillCommandWrappers(cfg, skillsDir)
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
