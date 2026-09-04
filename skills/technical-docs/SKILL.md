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
2. The options side by side: a table where the file uses tables, a bulleted
   list where it does not.
3. One section per option: a complete example, then its rules.
4. Constraints as rules, with the reason.
5. What the system reports, quoted.
6. Limits, and the delay before a change takes hold.

Headings name the subject: "Password logins", "Log output", "Limits". Parts 1,
3, and 6 are the ones a reader cannot do without.

## Extending a page that exists

Most work adds a section to a file that already has conventions, and those
outrank this skill. Read the whole file first, then copy what it does:

- Heading depth, and whether sections nest at all.
- Tables or lists. A file with no table does not get its first one here.
- How much an example shows, and whether it carries a secret or points at a
  variable.
- Where limits live: one section per feature, or one list at the end.

A new heading level, a first table, or a section twice its neighbors all say
one thing: this feature outranks the page around it.

## Size

Length follows what the reader decides, not what the system does. Budget before
drafting:

- One example per option, and never a second that shows a variation.
- One sentence per rule, and a reason only where the rule looks arbitrary.
- One quoted line per failure the reader can cause. Name the rest in prose.
- No section under three sentences. Fold a shorter one into its neighbor.

Cut in this order: the second example, the reason behind an obvious rule, the
log line nobody acts on, the sentence restating its heading.

## Before you call it done

Run the searches over the lines added, not over the whole file:

```bash
grep -nE '\byou\b|\byour\b'     # empty, outside a quoted error
grep -nE '^[0-9]+\.'            # numbered only for a sequence, else bullets
grep -nE '^- \*\*[^*]+\.\*\*'   # a table in disguise, unless the file does it
grep -c '^|'                    # tables only where the file already has them
grep -nE '^#+ '                 # every heading a noun
```

Then the linter, against the file as it stood. A page under edit carries
findings that predate the work, and those hide the new one:

```bash
git show HEAD:docs/guide.md > /tmp/before.md
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/style_lint.py \
    --search --baseline /tmp/before.md docs/guide.md
```

It reports nothing, and each `--search` hit inside the added lines is settled.
What no search reaches:

- Every key, default, and error string checked against the source as it stands
  now. A value changed earlier in the session leaves stale text behind.
- Nothing automatic shown as configurable, nothing operator-only present.
- Every example complete, the multi-entry shape shown.
- No instruction outside a real sequence.
- No sentence restating the one above it, no figurative verb.
- The headings read as a table of contents.
