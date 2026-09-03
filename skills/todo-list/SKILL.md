---
name: todo-list
description: Write an ordered todo list of the actions a person performs to reach an end state — a deployment, a migration, an onboarding. One numbered line per action, verb first, with every path and value it needs. Use for "what do I need to do", "give me the steps", "todo list", "runbook". Not for a checklist of states, and not for documentation of how the system works.
---

# Todo list

The ordered actions that take a person from where they are to a named end
state. The reader runs it top to bottom without opening anything else, and the
list is the whole reply.

| Form | A line holds | Reader wants |
|---|---|---|
| Todo list | An action: "Run `api/scripts/dev`." | To do the work in order |
| Checklist | A state: "`api.service` is enabled." | To audit work already done |
| Technical document | What the system does and which setting governs it | To decide |

## Rules

1. Read the source first. Every path, script, variable, and value comes from a
   file read in this session. A tool the source runs but never installs gets
   its own line: "Install `air`."
2. Numbered lines in execution order. No bullets, no checkboxes, no headings,
   no prose between lines.
3. One action per line: imperative verb, object, then the file or value.
   "Set `STRIPE_KEY=<stripe-key>` in `api/.env`."
4. Paths are relative to the repository root. A file outside the repository is
   absolute: `/etc/ledger/env`.
5. A value the code fixes is literal. A value that differs per environment is a
   placeholder named after the thing, `<host>`, spelled the same in every line.
6. Lines on the same file fold into one when nothing runs between them.
7. No reason inside a line. The one clause allowed turns the reader away from a
   sibling with a similar name: "Run `api/scripts/dev`, not `web/scripts/dev`."
8. Verification closes the list as actions: "Open `http://localhost:5173`." A
   value to read appears only where the source states it.
9. At most one short line before the list, what is in hand or missing from the
   source, and one after, where a failure shows. Both indicative, system as
   subject, no `you`, no quoted error text.
10. Past about fifteen lines, split into phases under noun headings; the
    numbering continues.

Italian lines use the infinitive or `si` form, never `esegui`. The shared rules
in `${CLAUDE_PLUGIN_ROOT}/rules/style.md` govern every word.

## Example

First day on a monorepo with `api/` (Go) and `web/` (Vite), each with its own
`scripts/dev`:

```markdown
The `STRIPE_KEY` value is in the `#payments` channel, not in the repository.

1. Install `asdf`, the `golang` and `nodejs` asdf plugins, and Docker.
2. Clone the `shop` repository.
3. Run `make setup` in the repository root.
4. Install `air`.
5. Set `STRIPE_KEY=<stripe-key>` in `api/.env`.
6. Run `make db`.
7. Run `api/scripts/dev`, not `web/scripts/dev`.
8. Run `make seed` in a second terminal.
9. Run `web/scripts/dev` in a third terminal.
10. Open `http://localhost:5173` in a browser.

On failure the cause is in the terminal where `api/scripts/dev` runs.
```

## Before sending

- Each line: imperative verb first, one action, its path or value present.
- Top to bottom: each line runnable with only the lines above it done.
- No state, no checkbox, no past tense, no reason inside a line.
- `${CLAUDE_PLUGIN_ROOT}/scripts/style_lint.py` reports nothing.
