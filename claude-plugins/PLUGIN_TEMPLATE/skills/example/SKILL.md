---
name: example
description: 'Analyzes the current project structure and tech stack. Use when asked to explore, understand, or summarize a project. Trigger terms: project overview, analyze codebase, what is this project.'
---

# Example Skill

Analyze the current project: $ARGUMENTS

---

**Steps**:
1. Read package.json or similar manifest
2. Identify main technologies and frameworks
3. List key directories and their purposes
4. Summarize in 2-3 sentences

**Output**:
- **Project Name**: From manifest file
- **Tech Stack**: Languages, frameworks, libraries
- **Structure**: Key directories and contents
- **Summary**: Brief description of what project does

If no manifest exists, infer from file extensions and directory structure. Keep summary concise and actionable.
