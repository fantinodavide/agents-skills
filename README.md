# claude-skills

Skills for Claude Code, kept outside the projects that use them.

| Skill | What it covers |
|---|---|
| [`usage-docs`](skills/usage-docs/SKILL.md) | Usage documentation for a system you built: config files, panel features, CLIs, APIs. Voice, scope, structure, the checks that keep claims true, and one merged style rule set from Strunk, the Google developer documentation style guide, and ASD-STE100. |
| [`clear-replies`](skills/clear-replies/SKILL.md) | The voice an agent uses when it talks to a person: chat replies, progress reports, plans, review notes. The `usage-docs` rules with the reader addressed directly, plus lists, numbered steps, and a named next action. Doubles as a Claude Code output style. |

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

## Output styles

An output style and a skill are the same file: markdown with `name` and
`description` in the frontmatter. `clear-replies` is written to serve as both, so
a second symlink turns the skill into a style `/output-style` lists:

```bash
ln -s "$PWD/skills/clear-replies/SKILL.md" ~/.claude/output-styles/clear-replies.md
```

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\output-styles\clear-replies.md" -Target "$PWD\skills\clear-replies\SKILL.md"
```

As a style it governs every reply in the session. As a skill it loads on demand,
in this session or in a subagent that writes something a person reads.

## Layout

Each skill is a directory holding `SKILL.md`, whose frontmatter carries the
`name` and the `description` that decides when the skill loads. Longer material
sits in `references/`, which the skill reads only when it needs it.

```
skills/<name>/
    SKILL.md
    references/*.md
```
