# claude-skills

Skills for Claude Code, kept outside the projects that use them.

| Skill | What it covers |
|---|---|
| [`usage-docs`](skills/usage-docs/SKILL.md) | Usage documentation for a system you built: config files, panel features, CLIs, APIs. Voice, scope, structure, the checks that keep claims true, and one merged style rule set from Strunk, the Google developer documentation style guide, and ASD-STE100. |

## Install

Claude Code loads skills from `~/.claude/skills`. A symlink keeps this repo the
single source:

```bash
ln -s "$PWD/skills/usage-docs" ~/.claude/skills/usage-docs
```

On Windows, from an elevated PowerShell prompt:

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\usage-docs" -Target "$PWD\skills\usage-docs"
```

Copying the directory works too, at the cost of drift.

## Layout

Each skill is a directory holding `SKILL.md`, whose frontmatter carries the
`name` and the `description` that decides when the skill loads. Longer material
sits in `references/`, which the skill reads only when it needs it.

```
skills/<name>/
    SKILL.md
    references/*.md
```
