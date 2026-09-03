---
name: technical-docs
description: Write technical documentation for a system you built — a config file, a panel feature, a CLI, an API, a service someone else operates. Use for a knowledgebase article, a user guide, a README section, or docs for a feature that was just implemented. Triggers include "write a guide", "document this", "knowledgebase article", "user docs", "explain how to use". Not for internal design notes or code comments.
---

# Technical documentation

What a system does and which parts of it the reader controls. Not a task
list, not a tour of the implementation, not the decision record. The reader
holds a goal and asks which setting gets them there, and what happens if they
get it wrong.

`${CLAUDE_PLUGIN_ROOT}/rules/style.md` governs every sentence; read the whole
file before drafting. "Read the source first", "Examples", and "Errors and
output" cost the most here. Mood and person are set below.

## Describe the system, don't command the reader

The reader decides. The text says what the system does and what each setting
means:

| Instead of | Write |
|---|---|
| Open Files, select `auth.json`, save, and restart. | The server reads `auth.json` at every start, so a change takes effect at the next restart. |
| Set `cookie_secret` to a random string. | `cookie_secret` signs sessions. Left out, each start invents a new one, and everyone signed in signs out. |
| Don't put the file in `data/`. | The server refuses a config in `data/`, because the reader can write there. |

The imperative fits only a sequence performed in order, such as registering an
application at a third party. `references/rewrites.md` holds more pairs.

## Keep the reader out of the sentence

The subject is the system, the file, or the setting. No `you`, and no
instruction outside a numbered procedure. The same sentence then serves the
operator, the auditor, and the reader a year later.

| Addressing the reader | Describing the system |
|---|---|
| Use `seed.sh` to set up a new environment. | `seed.sh` loads the fixtures into an empty database. |
| Change the value in `credentials` and run the script again. | A new value in `credentials` takes effect at the next run with `ON_CONFLICT=replace`. |
| You can point it at another instance with `DB_URL`. | `DB_URL` names the instance the script configures. |

Italian uses `si esegue` or `va eseguito`, never `esegui`.

## Document what the reader controls

- Reader-controlled: keys, values, files, UI actions. The subject of the page.
- Automatic: stated as behavior in the indicative, never as a knob.
- Operator-only: build flags, host commands, self-tests. The operator's README,
  not the user's guide.

A default shown as configurable gets configured. An operator command in a user
guide sends the reader somewhere they cannot go.

## Structure

1. What it is, what governs it, and when a change takes effect. One paragraph.
2. The options side by side, in a table.
3. One section per option: a complete example, then its rules.
4. Constraints as rules, with the reason.
5. What the system reports, quoted.
6. Limits.

Headings name the subject: "Password logins", "Log output", "Limits".

## Before you call it done

- Every key, default, and error string checked against the source.
- Nothing automatic shown as configurable, nothing operator-only present.
- Every example complete, the multi-entry shape shown.
- No `you`, no instruction outside a real sequence.
- No sentence restating the one above it, no figurative verb.
- Every heading a noun, and the set reads as a table of contents.
- `${CLAUDE_PLUGIN_ROOT}/scripts/style_lint.py` reports nothing, and each
  `--search` hit is settled.
