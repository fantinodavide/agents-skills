# Technical documentation evaluation

The revision produces shorter documentation in seven of eight cases, with no
storytelling. Some replies still add unnecessary detail or unsupported claims.
Generation success does not establish documentation correctness.

## Method

The comparison ran on 2026-09-08 against checkpoint `d051ac6`. Claude Code
reported the response model as `claude-opus-5[1m]`. Each version received the
shared rules, its skill body, and its worked examples in the system prompt.
Each user prompt contained the complete [fixture](panel_fixture.py), the
[case](cases.json) context and request, and an explicit concision instruction.
Assessment criteria stayed outside the prompt.

The CLI used safe mode, strict MCP configuration, disabled slash commands,
no session persistence, and no tools. Each request had a USD 0.50 ceiling and
a 120-second timeout. Two requests ran concurrently, without model or effort
overrides. All 16 fresh generations completed.

Two exploratory comparisons informed the revision. All eight cases were seen
before this final comparison, including those retaining `heldout_` identifiers.
Review was manual and unblinded, by the authoring agent. This run does not test
unseen tasks, plugin activation, tool use, or other models.

## Findings

Counts use whitespace-separated words, including Markdown and code.
Total output falls from 1,613 to 994 words; length alone is not a quality score.

| Task | Checkpoint → revision | Assessment |
|---|---|---|
| Directory correction | 160 → 63 | Returns a paragraph and distinguishes guidance from enforcement. Its exhaustive failure claim omits JSON parse errors. |
| Panel help | 181 → 77 | Preserves active settings on failure and routes correction to an operator. Error examples add avoidable length. |
| Failed reload | 275 → 111 | Distinguishes active settings from the invalid disk file. Adds an unsupported `panel.py` command. |
| CLI validation | 290 → 160 | Gives the command, output, exit status, and absence of changes. Drops the shell-specific exit-status command but retains excess detail. |
| Reference and page update | 281 → 216; 218 → 162 | Covers defaults, zero, reload timing, and valid examples. Still adds validation material and describes actual refreshes that the fixture does not perform. |

The API entry states the predicate and absence of refresh or timer-reset effects,
but adds a table that repeats the prose. Startup troubleshooting supplies the
correction, but incorrectly places validation before instance creation and adds
an unnecessary validation command.

## Verification

Fixture checks, linter and sync self-tests, skill validation, and repository
lint checks pass. All eight generated JSON examples parse and load through the
fixture. Recorded source hashes match the final files. [The results](results.json)
preserve complete replies and prompt hashes for inspection.

The revision improves scope and length in this sample. Generated documentation
still requires factual and editorial review.
