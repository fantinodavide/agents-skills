# Conversational style evaluation

The revised skill produces more focused corrections and completion reports in
this sample. Some replies still add unnecessary advice or unsupported details.
All 28 generations completed; that is not a claim that all responses meet the
behavioral criteria.

## Method

The comparison ran on 2026-09-08 through Claude Code 2.1.263. The response model
reported by the CLI was `claude-opus-5[1m]`. The baseline is checkpoint
`f7ff634`. The final skill's normalized SHA256 is in [the recorded results](results.json).

Each [case](cases.json) supplies context, a user message, and assessment criteria.
Only the context and user message went to Claude. The criteria stayed outside
the prompt. The skill body replaced the system prompt for each isolated reply.
Both versions used the same generation controls, with no model or effort override.

The CLI ran with `--safe-mode`, `--strict-mcp-config`,
`--disable-slash-commands`, `--no-session-persistence`, and an empty `--tools`
list. Each request had a 120-second timeout and a USD 0.50 budget ceiling.
Two requests ran concurrently. The initial sandboxed request timed out; the
successful comparisons ran outside the sandbox with approval.

The first eight cases informed two revisions. Four cases were added after the
first comparison, and two after the second. Existing baseline replies were
reused. The final dataset contains one baseline and one final reply per case.
Review was manual and unblinded, by the authoring agent. Word counts describe
the outputs; shorter replies do not automatically receive a better assessment.

## Findings

| Response type | Observed result |
|---|---|
| Corrections | The restart correction shrank from 108 words to 26 and stopped inventing an investigation history. The time-zone correction shrank from 90 words to 23 and removed the offer for unrelated follow-up work. |
| Completion reports | All three final reports named the completed work and the missing check. The Windows report stopped claiming that no Windows host was available. The load-test report omitted the tool-availability detail. |
| Focused answers | Export names, deletion timing, and the weekly chart remained brief under both styles. The revision did not consistently shorten these already focused replies. |
| Explanation and recommendation | The duplicate-job explanation shrank from 254 words to 155 but still added an analogy and unrequested implementation advice. The queue recommendation covered the requested topics but remained longer than necessary. |
| Requested depth | The version-conflict explanation retained the mechanism, an ordered example, and guidance for preserving the draft. It used 475 words against the baseline's 544. |

The strongest improvement concerns which details deserve space. Removing the
automatic follow-up and modeling a brief correction helped more than
restrictions on individual words. The skill therefore prioritizes useful
information, connected explanations, and a natural voice. Wording conventions
come last.

## Remaining limits

The archive case still inferred that hiding an item preserves it, although
the fixture supplied no storage information. It also discussed unrelated
unknowns. That response does not meet the evidence-boundary criterion.

Some replies still use figurative language, filler, or implementation advice
outside the question's scope. The style instructions reduce some of these
habits; they do not establish factual correctness.

The run tests isolated replies with the style body as the system prompt. It
does not test the full Claude Code coding prompt, plugin activation, tool use,
long conversations, other Claude models, or the user's personal preference.
The two final prompts were unseen during revision, but two cases provide
limited evidence of transfer. The results support this revision without
establishing consistent behavior across future conversations.

## Repository checks

The linter and sync self-tests pass. The documentation profile passes on the
documentation sources, and the conversation profile passes on the revised
skill. Eight additional CLI checks cover profile selection, warning-only
sentence length, retained filler errors, invalid arguments, and baseline comparison.

The skill validator passes on a temporary copy with the output-style extension
excluded. The real file retains `keep-coding-instructions: true`, and the
plugin's output-style path resolves to that file. The field is supported by
[Claude Code's output-style schema](https://code.claude.com/docs/en/output-styles).

Further comparisons can reuse the context and user fields in `cases.json`.
Its criteria and this report belong to evaluation, not the model's prompt.
Fresh cases are needed to assess later revisions without relying only on
examples already used for calibration.
