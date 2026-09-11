---
name: technical-docs
description: Write or update concise technical documentation from verified behavior. Use for configuration references, user guides, README sections, API or CLI documentation, and troubleshooting. Keep the facts needed for the reader's task, with no storytelling. Not for internal design notes, code comments, or standalone todo lists.
---

# Technical documentation

Write concise documentation with clear labels and the facts needed for the
requested task. State the behavior directly. Reduce unnecessary reading while
preserving useful layout and qualifications.

Keep technical docs very concise. Omit storytelling, analogies, rhetorical
questions, author commentary, and implementation history. A small setting or
action usually needs a few sentences or a compact table. Requested detail and
necessary distinctions justify more space; available source material does not.

These instructions govern the document. Conversation with the user follows
the conversational style. Documenting a system does not authorize changing it.

## Keep the requested scope

Identify the audience and the task from the request and surrounding page.
Include only the actions available to that audience. An operator can need host
commands; a panel user can need only panel actions.

A paragraph replacement returns a paragraph. A short help section explains
the control, its result, and any failure the reader must handle. Source files
verify those claims; they do not define the document's table of contents.
Include a newly discovered detail only if it changes the reader's action,
choice, or interpretation. State relevant restrictions briefly. Leave internal
rationales, diagnostic transcripts, and adjacent features out of a general guide
unless needed for its task.

A repository's documentation describes only what the repository contains and
reads: its modules, its environment variables, and the paths it serves. It
names no other repository, shared workspace file, proxy, deployment definition,
or consuming application. Only an explicit user directive overrides this rule;
source files, surrounding pages, and other skills do not.

For example, given a button that pauses scheduled imports, lets the current
import finish, and requires an administrator to resume, this is complete:

> **Pause imports** stops new imports. The current import finishes.
> An administrator can resume scheduled imports.

## Verify the claims

Read the inputs, defaults, validation, consumers, and failure paths relevant to
the requested topic. A name, comment, or plausible design is not proof of
behavior. Trace each claimed effect through the operation that produces it.
Reading settings does not establish that displayed data refreshes; a condition
that reports whether work is due does not establish that the work runs.

Keep these distinctions explicit when they matter:

- Enforced constraint: the implementation rejects, changes, or prevents an input.
- Documented requirement: the supported workflow requires something, even if
  the implementation does not check it.
- Recommendation: guidance favors a choice without claiming alternatives fail.

A rewrite preserves meaning. Advice to store files in a particular directory
does not prove that the loader rejects other directories. Automatic behavior
does not prove the developer's reason for it.

Bound claims to the source examined. An absent check in one function does not
prove that callers omit it. Preserve relevant uncertainty without inventing
defaults, enforcement, side effects, or recovery guarantees. Put material source
discrepancies in the handoff; keep unrelated unknowns out of the document.

## Choose the necessary facts and form

Select the facts that answer the requested question: relevant defaults, units,
allowed values, omitted or zero values, activation, persistence, and failure
state. These are possible details, not a checklist to fill in every section.

| Document | Include |
|---|---|
| Reference | The behavior and values needed to choose an input or call an operation. |
| Explanation | The mechanism and consequences needed to answer the stated question. |
| Procedure | Necessary prerequisites, ordered actions, and a check of the result. |
| Troubleshooting | The symptom, its supported cause, the state left behind, and the correction. |

Use a paragraph for one point, a table for comparable values, and numbered
steps for a sequence. Preserve useful bold lead-ins and emphasis when editing.
Short bold labels can make a list easier to scan; they do not require a table.
Add headings only when they help navigation. State each fact once: a table
needs no prose that repeats its rows, and a complete section needs no recap.
Do not pad sections to a sentence count.

Use the system, setting, file, or operation as the subject of explanatory prose.
Use present tense for behavior, without `you` or `your`. Numbered procedures
use imperative actions. Italian prose uses impersonal forms such as `si esegue`
or `va eseguito`. Describe automatic actions as automatic; include an operator
override only when it exists and belongs to the task.

## Examples and errors

Give the smallest complete example that demonstrates the requested behavior.
Show contrasting forms when requested or needed to distinguish their effects.
An example of omission omits the setting; an explicit default illustrates a
different form. Extra collection entries belong only when they clarify the shape.

Keep syntax and names consistent with the implementation. Identify necessary
deployment placeholders. Use only supported secret references. Commands must
match the stated environment; avoid shell-specific verification steps when
the environment is unspecified.

Copy relevant errors exactly. Describe the failure state and supported recovery
without implying rollback, retry, or persistence the source does not provide.
Quote a log line when the reader needs to recognize or diagnose that message.
A general guide can state the failure and correction without showing the log.
Include a full error catalog only when the requested reference needs one.

Read [the worked examples](references/rewrites.md) when a rewrite risks changing
meaning or needs a complete model of the intended document.

## Update and finish

Read the surrounding page. Separate factual corrections from wording changes.
Correct outdated claims in place; preserve useful terminology, formatting,
structure, and navigation. Keep accurate defaults and option descriptions unless
the requested scope excludes them. Newly discovered implementation details do
not replace existing reference information. The finished page describes the
resulting behavior without an account of the edit.

Check material claims and example syntax. Run examples or focused checks when
feasible and relevant. Do not perform destructive or external actions to validate
prose. Report a material verification limit in the handoff.

Apply [the shared wording rules](../../rules/style.md) as a final editing pass.
Prefer familiar, literal words, stable terms, and active voice. The conventions
are defaults: the scope, meaning, and concision above take priority. The core
skill still applies when the shared file is unavailable.

The optional `scripts/style_lint.py --profile documentation` check reports
wording issues. Sentence length, tense, and punctuation hints require judgment.
A clean result does not verify facts or usefulness.

Before finishing, check what the edit makes easier to find, understand, or do.
Remove unnecessary reading without removing useful emphasis or reference facts.
Keep necessary behavior and qualifications; stop there.
