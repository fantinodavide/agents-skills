# agents-skills

Skills for coding agents, kept outside the projects that use them. Claude Code
reads them from a plugin install or from `~/.claude/skills`, and any agent that
reads markdown instructions can use the same files.

| Skill | What it covers |
|---|---|
| [`technical-docs`](skills/technical-docs/SKILL.md) | Technical documentation for a system you built: config files, panel features, CLIs, APIs. Voice, scope, structure, and the checks that keep claims true. The system is the subject of every sentence. |
| [`todo-list`](skills/todo-list/SKILL.md) | An ordered todo list of the actions a person performs to reach an end state. One numbered line per action, verb first, with every path and value the action needs. |
| [`clear-output-style`](skills/clear-output-style/SKILL.md) | The voice an agent uses when it talks to a person: chat replies, progress reports, plans, review notes. Connected explanations, relevant detail, and natural wording. Doubles as a Claude Code output style. |

`technical-docs` and `todo-list` share [`rules/style.md`](rules/style.md):
Strunk's composition principles, the Google developer documentation style
guide, and ASD-STE100 merged into one. Each skill sets its mood, person, and
structure. `clear-output-style` is self-contained, with conversational rules
and complete examples. It prioritizes understanding and useful completeness
over sentence length and formatting conventions.

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
`clear-output-style` contains its own rules and needs no shared-rule path.

## Output styles

A skill and an output style both use Markdown instructions, but their metadata
and loading behavior differ. `clear-output-style` serves as both, and the
plugin ships the same file through both mechanisms.

As a style it governs every reply in the session. Select it under Output style
in `/config`. The plugin registers it as `fantinodavide-agents-skills:clear-output-style`,
which is the value `outputStyle` takes in `settings.json`; `clear-output-style`
alone does not resolve. The file sets `keep-coding-instructions: true`, so selecting
the style keeps Claude Code's built-in coding instructions and layers the voice on
top of them. As a skill it loads on demand, in this session or in a subagent that
writes something a person reads. A new Claude Code session loads changes to the
selected output style. The `keep-coding-instructions` field is valid output-style
metadata; a generic skill validator may reject it because its schema differs.
These behaviors follow the [Claude Code output-style documentation](https://code.claude.com/docs/en/output-styles).

Outside a plugin install, a symlink does the same:

```bash
ln -s "$PWD/skills/clear-output-style/SKILL.md" ~/.claude/output-styles/clear-output-style.md
```

## Rule ownership

`rules/style.md` holds the shared documentation rules. `technical-docs` and
`todo-list` read that file when they load. Conversational changes belong in
`skills/clear-output-style/SKILL.md`, including its complete response examples.

The conversational skill has no synced documentation sections. The
`scripts/sync_rules.py` helper remains available for files that use
`<!-- rules: -->` markers. With `--check`, it exits 1 when a marked copy differs
from its source. Files without markers remain unchanged.

## Draft checks

`scripts/style_lint.py` checks mechanical wording conventions. The default
`strict` profile follows the documentation rules. The `conversation` profile
permits perfect tense and treats sentence length, timing words, and repeated
em dashes as review hints:

```bash
python3 scripts/style_lint.py --profile conversation skills/clear-output-style/SKILL.md
cat reply.md | python3 scripts/style_lint.py --profile conversation -
git show HEAD:docs/guide.md > /tmp/before.md
python3 scripts/style_lint.py --baseline /tmp/before.md docs/guide.md
```

The script needs Python 3 and nothing else. It reports the filler words, part of
the signal-free vocabulary, `e.g.` and `i.e.`, `currently`, the perfect tense,
and British spelling. It also reports `here`, `this`, or `link` as link text, a
second em dash in a paragraph, and a sentence past 25 words. In the
`conversation` profile, review hints print with `review:` and do not cause a
failed check. Other findings still produce exit status 1. An unknown profile
produces an error.

`--baseline OLD NEW` reports what NEW adds to OLD, so an edit to a page that
already breaks a rule is judged on the edit. A finding matches the baseline by
rule and message rather than by a line number, which moves.

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

The script cannot establish whether a reply works. A reader or judge checks
the response against its request and evidence:

- Does the opening answer the actual request?
- Does the reply cover every material part with enough reason to understand it?
- Do the sentences connect, and does each detail help the reader?
- Are claims supported and meaningful limits clear?
- Does the reply stop when complete, with a next action only if needed?

The [conversational evaluation](evaluations/clear-output-style/REVIEW.md)
records a comparison with the previous checkpoint, the supplied cases, and
the remaining behavioral limits. These evaluation files stay outside the skill
so they do not become examples in the model's prompt.

## Layout

Each skill is a directory holding `SKILL.md`, whose frontmatter carries the
`name` and the `description` that decides when the skill loads. Material that
belongs to one skill sits in its `references/`, which the skill reads only when
it needs it. Only `technical-docs` has one. Material shared by the documentation skills sits
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
| [attention-control](https://github.com/aaddrick/attention-control) | aaddrick | MIT | Ownership and evidence in conversational reports. |

This repository summarizes the Google style guide and ASD-STE100; it reproduces
neither. No approved-word dictionary from ASD-STE100 appears here. Check text
under a contractual STE requirement against the official dictionary, not against
these files.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), full text in
[`LICENSE`](LICENSE). Copyright 2026 Davide Fantino. Reuse and adaptation are
free with attribution.
