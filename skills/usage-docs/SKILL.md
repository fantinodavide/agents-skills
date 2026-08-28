---
name: usage-docs
description: Write usage documentation for a system you built — a config file, a panel feature, a CLI, an API, a service someone else operates. Use for a knowledgebase article, a user guide, a README section, or docs for a feature that was just implemented. Triggers include "write a guide", "document this", "knowledgebase article", "user docs", "explain how to use". Not for internal design notes or code comments.
---

# Usage documentation

Usage documentation tells a reader what a system does and which parts of it they
control. It is not a task list, not a tour of the implementation, and not a
transcript of the decisions that produced the feature.

The reader arrives holding a goal and a question: which setting gets me there,
and what happens if I get it wrong. Everything below serves that.

## Read the source before writing a line

Every claim in the document is a claim about running code, so read the code that
implements the feature: the parser or schema, the defaults, the validation
rules, the error strings, and the place the values are consumed. Note the exact
keys, the exact defaults, and the exact refusal messages.

Three failures come from skipping this:

- A key documented with the wrong type, such as a list where the code requires
  an object.
- A constraint stated too loosely, such as "any provider" where the code accepts
  two.
- An error message paraphrased instead of quoted, which no one can search for.

When the source contradicts an earlier draft or an existing doc, the source
wins, and the contradiction is worth reporting rather than quietly fixing.

## Describe the system, don't command the reader

A usage doc is read by someone deciding, not by someone taking dictation. Write
what the system does and what each setting means, so the reader chooses.

| Instead of | Write |
|---|---|
| Open Files, select `auth.json`, save, and restart. | The server writes `auth.json` at first start and reads it again at every start, so a change takes effect at the next restart. |
| Set `cookie_secret` to a random string. | `cookie_secret` holds the key that signs sessions. Left out, each start invents a new one, and everyone signed in at the time signs out. |
| Don't put the file in `data/`. | The server refuses a config it finds in `data/`, because the reader can write there and could edit its own login away. |

Imperative mood still fits a genuine sequence the reader performs in order, such
as registering an application at a third party before the config will work. Use
it there, and nowhere else. `references/rewrites.md` holds more pairs.

## Document what the reader controls, and nothing else

Draw the line before writing the outline:

- **Reader-controlled**: keys they set, values they choose, files they edit,
  actions they take in a UI. These are the subject of the document.
- **Automatic**: what the system decides on its own. State it as behavior, in
  the indicative — "the panel port closes", "the reader moves to a loopback
  port". Never as a knob, and never with an override the reader wasn't meant to
  reach for.
- **Operator-only**: build flags, host commands, self-tests, environment set by
  the platform. These belong in the operator's README, not the user's guide.

Presenting an internal default as configurable invites someone to configure it.
Presenting an operator command in a user guide sends a reader somewhere they
have no access to.

## A structure that answers the reader's questions in order

1. **What the thing is and what governs it.** One short paragraph: the feature,
   the file or setting that controls it, and when a change takes effect.
2. **The options, side by side.** A table of modes or values, each with what it
   does and what it fits. The table is where a reader picks.
3. **One section per option**, each opening with a sentence that introduces a
   complete, working example, then the rules that govern it.
4. **Constraints as rules, with the reason attached.** A rule the reader
   understands is a rule they don't fight.
5. **What the system reports.** Where its output goes, what the startup lines
   name, and what a refusal looks like, quoted.
6. **Limits.** What the feature does not cover, in plain terms.

Section headings are noun phrases naming the subject: "Password logins",
"Cloudflare tunnels", "What the server reports". Not "Getting started", not
"Overview", not a verb phrase ordering the reader around.

## Examples carry the document

Every example is complete enough to paste and real enough to trust: plausible
hostnames, plausible IDs, plausible secrets by reference rather than value. Show
the shape a reader will actually write, including the multi-entry case when one
entry hides the shape — a single-user example makes a map look like a scalar.

Introduce each block with a sentence ending in a colon, and tag the fence with
its language.

## Errors and output

Quote refusals and log lines verbatim, in a fenced block, so a reader searching
for the text they saw lands on the page that explains it. Say where the output
goes and how long it survives. When the system fails closed, say what it closed
and why that is the safe end of the trade.

## Style

Follow the Google developer documentation style guide: second person for what
the reader does, active voice, present tense, sentence case, serial comma, code
font for identifiers and paths, US spelling. Cut `just`, `simply`, `please`,
`easy`, `note that`. Prefer `lets you` to `allows you to`.

Read `references/anti-patterns.md` before finishing. It lists the tells that
make documentation read as generated: adjective padding, the rule of three,
inline-header bullet lists, summary sections, and the vocabulary cluster around
"leverage", "robust", "seamless", and "underscore".

## Before you call it done

- Every key, default, and error string checked against the source.
- Nothing automatic presented as configurable, nothing operator-only present.
- Every example complete, and the multi-entry shape shown where it matters.
- No section that only restates the section above it.
- No sentence that tells the reader what to do outside a real sequence.
- Headings scan as a table of contents someone could navigate by.
