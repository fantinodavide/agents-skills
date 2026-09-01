# agents-skills

Skills for coding agents, kept outside the projects that use them. Claude Code
reads them from `~/.claude/skills`, and any agent that reads markdown
instructions can use the same files.

| Skill | What it covers |
|---|---|
| [`technical-docs`](skills/technical-docs/SKILL.md) | Technical documentation for a system you built: config files, panel features, CLIs, APIs. Voice, scope, structure, the checks that keep claims true, and one merged style rule set from Strunk, the Google developer documentation style guide, and ASD-STE100. |
| [`clear-output-style`](skills/clear-output-style/SKILL.md) | The voice an agent uses when it talks to a person: chat replies, progress reports, plans, review notes. The `technical-docs` rules with the reader addressed directly, plus lists, numbered steps, and a named next action. Doubles as a Claude Code output style. |

## Install as a plugin

The repo is a plugin marketplace holding one plugin, so both skills arrive
together:

```
/plugin marketplace add fantinodavide/agents-skills
/plugin install fantinodavide-agents-skills@agents-skills
```

An install tracks the repo, so a `/plugin update` brings later changes.

## Install as loose skills

Claude Code also loads skills from `~/.claude/skills`. A symlink keeps this repo
the single source, and suits work on the skills themselves:

```bash
ln -s "$PWD/skills/technical-docs" ~/.claude/skills/technical-docs
```

On Windows, from an elevated PowerShell prompt:

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\technical-docs" -Target "$PWD\skills\technical-docs"
```

Copying the directory works too, at the cost of drift.

## Output styles

An output style and a skill are the same file: markdown with `name` and
`description` in the frontmatter. `clear-output-style` is written to serve as
both, so a second symlink turns the skill into a style `/output-style` lists:

```bash
ln -s "$PWD/skills/clear-output-style/SKILL.md" ~/.claude/output-styles/clear-output-style.md
```

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\output-styles\clear-output-style.md" -Target "$PWD\skills\clear-output-style\SKILL.md"
```

As a style it governs every reply in the session. As a skill it loads on demand,
in this session or in a subagent that writes something a person reads.

## Layout

Each skill is a directory holding `SKILL.md`, whose frontmatter carries the
`name` and the `description` that decides when the skill loads. Longer material
sits in `references/`, which the skill reads only when it needs it.

```
.claude-plugin/
    marketplace.json
    plugin.json
skills/<name>/
    SKILL.md
    references/*.md
```

A plugin install carries the skills and not the output style, which Claude Code
reads from `~/.claude/output-styles`. The symlink above stays the way to get it.

## Credits

The rules in these skills come from five sources.

| Source | Author | License | What it supplies |
|---|---|---|---|
| [The Elements of Style](https://www.gutenberg.org/ebooks/37134) (1918) | William Strunk Jr. | Public domain | Composition principles: cut what does no work, put the meaning where the eye lands. |
| [Google developer documentation style guide](https://developers.google.com/style) | Google | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Developer conventions: person, tense, mood, word choice, formatting. |
| [ASD-STE100](https://asd-ste100.org) | AeroSpace and Defence Industries Association of Europe | ASD's own terms, free to download | Ambiguity control: one meaning per word, one action per sentence, short sentences. |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Ayoub Ghriss | MIT | The output shape: answer first, numbered steps, state restated each turn, wins visible. |
| [caveman](https://github.com/JuliusBrussee/caveman) | Julius Brussee | MIT | The compressed mode `clear-output-style` hands the non-user-facing half of the output to. |

The Google style guide and ASD-STE100 are summarized rather than reproduced. No
approved-word dictionary from ASD-STE100 appears here, and text under a
contractual STE requirement is checked against the official dictionary rather
than against these files.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), full text in
[`LICENSE`](LICENSE). Copyright 2026 Davide Fantino. Reuse and adaptation are
free with attribution.
