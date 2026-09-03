# agents-skills

Skills for coding agents, kept outside the projects that use them. Claude Code
reads them from a plugin install or from `~/.claude/skills`, and any agent that
reads markdown instructions can use the same files.

| Skill | What it covers |
|---|---|
| [`technical-docs`](skills/technical-docs/SKILL.md) | Technical documentation for a system you built: config files, panel features, CLIs, APIs. Voice, scope, structure, and the checks that keep claims true. The system is the subject of every sentence. |
| [`todo-list`](skills/todo-list/SKILL.md) | An ordered todo list of the actions a person performs to reach an end state. One numbered line per action, verb first, with every path and value the action needs. |
| [`clear-output-style`](skills/clear-output-style/SKILL.md) | The voice an agent uses when it talks to a person: chat replies, progress reports, plans, review notes. The shared rules with the reader addressed directly, plus lists, numbered steps, and a named next action. Doubles as a Claude Code output style. |

The three share one rule set, [`rules/style.md`](rules/style.md): Strunk's
composition principles, the Google developer documentation style guide, and
ASD-STE100 merged into one. Each skill adds what follows from its reader: the
mood, the person, and the shape of the output. A table in `rules/style.md`
states the mood and the person side by side, and each skill sets its own shape.

## Plugin install

The repo is a plugin marketplace holding one plugin, so the three skills arrive
together:

```
/plugin marketplace add fantinodavide/agents-skills
/plugin install fantinodavide-agents-skills@agents-skills
```

An install tracks the repo, so a `/plugin update` brings later changes.
`technical-docs` and `todo-list` name the shared files through
`${CLAUDE_PLUGIN_ROOT}`, which a plugin install sets to the installed copy of
this repo.

## Loose skills

Claude Code also loads skills from `~/.claude/skills`, which suits work on the
skills themselves. A symlink keeps this repo the single source:

```bash
for skill in technical-docs todo-list clear-output-style; do
  ln -s "$PWD/skills/$skill" ~/.claude/skills/"$skill"
done
```

On Windows, from an elevated PowerShell prompt:

```powershell
foreach ($skill in 'technical-docs', 'todo-list', 'clear-output-style') {
  New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\$skill" -Target "$PWD\skills\$skill"
}
```

Copying the directory works too, at the cost of drift. Outside a plugin
install `${CLAUDE_PLUGIN_ROOT}` is unset, so `technical-docs` and `todo-list`
find `rules/style.md` only when the agent resolves that path to this checkout.
`clear-output-style` carries its copy of the shared sections inline and needs
no such path.

## Output styles

An output style and a skill are the same file: markdown with `name` and
`description` in the frontmatter. `clear-output-style` serves as both, and the
plugin ships it both ways.

As a style it governs every reply in the session. Select it under Output style
in `/config`. The plugin registers it as `fantinodavide-agents-skills:clear-output-style`,
which is the value `outputStyle` takes in `settings.json`; `clear-output-style`
alone does not resolve. The file sets `keep-coding-instructions: true`, so selecting
the style keeps Claude Code's built-in coding instructions and layers the voice on
top of them. As a skill it loads on demand, in this session or in a subagent that
writes something a person reads.

Outside a plugin install, a symlink does the same:

```bash
ln -s "$PWD/skills/clear-output-style/SKILL.md" ~/.claude/output-styles/clear-output-style.md
```

## One source for the shared rules

`rules/style.md` holds every shared rule once. `technical-docs` and `todo-list`
point at it and read it when they load. Claude Code reads `clear-output-style`
as one file when it runs as an output style, so that file carries copies of the
shared sections inline. Each copy sits between an opening and a closing marker:

```markdown
<!-- rules: style.md#sentences -->
## Sentences
...
<!-- /rules -->
```

The script `scripts/sync_rules.py` rewrites every copy from the section its
marker names. The section runs from its heading to the next heading of the same
or a higher level. The slug is the heading lowercased, with a hyphen for every
run of characters other than letters and digits. Text outside the markers is the
skill's own. An edit to a shared rule goes into `rules/style.md`, followed by:

```bash
python3 scripts/sync_rules.py
```

With `--check` the script exits 1 when a copy differs from the source. The
`style-lint` workflow runs it, so a copy edited by hand fails the build until
`rules/style.md` carries the change.

## Draft checks

`rules/style.md` states part of its final pass as searches, so a script can run
that part:

```bash
python3 scripts/style_lint.py skills/clear-output-style/SKILL.md
cat reply.md | python3 scripts/style_lint.py -
```

The script needs Python 3 and nothing else. It reports the filler words, part of
the signal-free vocabulary, `e.g.` and `i.e.`, `currently`, the perfect tense,
and British spelling. It also reports `here`, `this`, or `link` as link text, a
second em dash in a paragraph, and a sentence past 25 words.

A sentence wrapped across lines counts as one sentence. `--search` adds the passive voice and the
gerund check, which report hits for a reader to settle rather than errors. The
style allows a passive where the actor is unknown, and the pattern cannot tell a
trailing gerund from a noun. The assertions run with `--selftest`. The
`style-lint` workflow runs the self-tests, the sync check, and the linter on
every push to `main` and on every pull request.

The script reads prose. It skips fenced code, inline code, and YAML frontmatter.
A line containing `<!-- style-lint: ignore -->` is skipped, and a
`<!-- style-lint: ignore-block -->` comment skips every line under it until the
next blank line. The example tables carry the block marker, because a table of
defects quotes the defects it names. A domain term that matches a banned word,
such as `landscape` for a page orientation, goes in code font, which the script
skips.

The script cannot check the half that decides whether a reply works. That half
needs a reader or a judge, and it asks four questions:

- Does the answer lead?
- Did you do the work you own?
- Does the reply restate the state?
- Can the reader run the next action?

## Layout

Each skill is a directory holding `SKILL.md`, whose frontmatter carries the
`name` and the `description` that decides when the skill loads. Material that
belongs to one skill sits in its `references/`, which the skill reads only when
it needs it. Only `technical-docs` has one. Material shared by every skill sits
in `rules/`.

```
.claude-plugin/
    marketplace.json
    plugin.json
.github/workflows/
    style-lint.yml
rules/
    style.md
scripts/
    style_lint.py
    sync_rules.py
skills/<name>/
    SKILL.md
    references/*.md
```

The plugin ships the output style as well, through the `outputStyles` path in
`plugin.json`. That path points at the `clear-output-style` skill directory
rather than a second copy of the same text. After an install, `/config` lists it
under Output style.

## Credits

The rules in these skills come from six sources.

| Source | Author | License | What it supplies |
|---|---|---|---|
| [The Elements of Style](https://www.gutenberg.org/ebooks/37134) (1918) | William Strunk Jr. | Public domain | Composition principles: cut what does no work, and put the meaning where the eye lands. |
| [Google developer documentation style guide](https://developers.google.com/style) | Google | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Developer conventions: person, tense, mood, word choice, and formatting. |
| [ASD-STE100](https://asd-ste100.org) | AeroSpace and Defence Industries Association of Europe | ASD's own terms, free to download | Ambiguity control: one meaning per word, one action per sentence, short sentences. |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Ayoub Ghriss | MIT | The output shape: answer first, numbered steps, state restated each turn, wins visible. |
| [caveman](https://github.com/JuliusBrussee/caveman) | Julius Brussee | MIT (`skills/`) | The compressed mode for the half of the output no user reads. |
| [attention-control](https://github.com/aaddrick/attention-control) | aaddrick | MIT | Three rules in `clear-output-style`: own the work you can finish, never invent a specific, and state the full reach of an irreversible action. |

This repository summarizes the Google style guide and ASD-STE100; it reproduces
neither. No approved-word dictionary from ASD-STE100 appears here. Check text
under a contractual STE requirement against the official dictionary, not against
these files.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), full text in
[`LICENSE`](LICENSE). Copyright 2026 Davide Fantino. Reuse and adaptation are
free with attribution.
