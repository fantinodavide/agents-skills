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

Claude Code also loads skills from `~/.claude/skills`, which suits work on the
skills themselves. A symlink keeps this repo the single source:

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
`description` in the frontmatter. `clear-output-style` serves as both, and the
plugin ships it both ways.

As a style it governs every reply in the session, selected with `/output-style`.
The plugin registers it as `fantinodavide-agents-skills:clear-output-style`,
which is the value `outputStyle` takes in `settings.json`; `clear-output-style`
alone does not resolve. As a skill it loads on demand, in this session or in a
subagent that writes something a person reads.

Outside a plugin install, a symlink does the same:

```bash
ln -s "$PWD/skills/clear-output-style/SKILL.md" ~/.claude/output-styles/clear-output-style.md
```

## Checking a draft

`clear-output-style` states part of its pre-send check as searches, so a script
can run that part:

```bash
python3 scripts/style_lint.py output-styles/clear-output-style.md
cat reply.md | python3 scripts/style_lint.py -
```

The script needs Python 3 and nothing else. It reports the filler words, the
signal-free vocabulary, `e.g.` and `i.e.`, the perfect tense, the passive voice,
British spelling, `here` as link text, a second em dash in a paragraph, and a
sentence past 25 words. `--search` adds the gerund check, which reports hits for
a reader to settle rather than errors. `--selftest` runs the assertions.

The script reads prose. It skips fenced code, inline code, and YAML frontmatter.
A line ending in `<!-- style-lint: ignore -->` is skipped, and a
`<!-- style-lint: ignore-block -->` comment skips every line under it until the
next blank line. The example tables carry the block marker, because a table of
defects quotes the defects it names.

What the script cannot check is the half that decides whether a reply works:
whether the answer leads, whether you did the work you own, whether the state is
restated, and whether the next action is one the reader can run. That half needs
a reader or a judge.

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

The plugin ships the output style as well, through the `outputStyles` path in
`plugin.json`, which points at the `clear-output-style` skill directory rather
than a second copy of the same text. `/output-style` lists it after an install.

## Credits

The rules in these skills come from six sources.

| Source | Author | License | What it supplies |
|---|---|---|---|
| [The Elements of Style](https://www.gutenberg.org/ebooks/37134) (1918) | William Strunk Jr. | Public domain | Composition principles: cut what does no work, put the meaning where the eye lands. |
| [Google developer documentation style guide](https://developers.google.com/style) | Google | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Developer conventions: person, tense, mood, word choice, formatting. |
| [ASD-STE100](https://asd-ste100.org) | AeroSpace and Defence Industries Association of Europe | ASD's own terms, free to download | Ambiguity control: one meaning per word, one action per sentence, short sentences. |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Ayoub Ghriss | MIT | The output shape: answer first, numbered steps, state restated each turn, wins visible. |
| [caveman](https://github.com/JuliusBrussee/caveman) | Julius Brussee | MIT | The compressed mode `clear-output-style` hands the non-user-facing half of the output to. |
| [attention-control](https://github.com/aaddrick/attention-control) | aaddrick | MIT | Three rules in `clear-output-style`: own the work you can finish, never invent a specific, and the full reach of an irreversible action. |

The Google style guide and ASD-STE100 are summarized rather than reproduced. No
approved-word dictionary from ASD-STE100 appears here, and text under a
contractual STE requirement is checked against the official dictionary rather
than against these files.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), full text in
[`LICENSE`](LICENSE). Copyright 2026 Davide Fantino. Reuse and adaptation are
free with attribution.
