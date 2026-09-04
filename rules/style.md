# The shared rule set

The rules every skill in this repository applies, merged from The Elements of
Style, the Google developer documentation style guide, and ASD-STE100. The goal
is the fewest words that leave out nothing the reader needs. Each skill adds
its person, mood, and shape. A skill read as one file carries copies of these
sections between `<!-- rules: -->` and `<!-- /rules -->` markers, and
`scripts/sync_rules.py` keeps them equal to this file.

## Read the source first

Every claim about a system is a claim about running code. Read the schema, the
defaults, the validation, the error strings, and the consumer before writing,
and copy keys, defaults, and refusal messages as they are. The source wins over
an earlier draft, and the contradiction gets reported. A claim nobody checked
is marked unchecked or left out, and a snippet nobody ran is marked untested.
Never invent a specific: a version, a date, a flag, a line number. Name the
file or command that settles it.

## Sentences

- Active voice. Passive only when the actor is unknown, never twice in a row.
- Simple tenses: present for what the system does, past for what happened. No
  present perfect.
- One action per sentence: about 20 words in a step, 25 in description.
- Keep the structure words: subject, verb, article, `that`.
- Positive form. `not` for denial and contrast only.
- Specific over general: `the parser refuses a config that names both forms`,
  not `robust validation`.
- Subject beside verb, modifier beside what it modifies.
- The consequence last.
- Parallel form in lists, tables, and series.
- Vary the shape, never the terms.

## Plain terms, never figurative

A metaphor makes the reader translate, and two readers translate differently:

| Figurative | Literal |
|---|---|
| The variables move the target. | The variables name a different instance. |
| The passwords ride in with the users. | The script applies the passwords from the JSON. |
| The value lands. | The value takes effect. |
| A file born from a dump. | A file derived from a dump. |
| Circle back to it. | Return to it. |

## Words

- One word, one meaning, every time. Synonym rotation is a defect.
- The plainest word: `use`, `about`, `to`, `lets you`.
- Cut: `just`, `simply`, `please`, `easy`, `obviously`, `of course`,
  `note that`, `keep in mind`, `be aware that`, `it is important to note`.
- Cut: `leverage`, `robust`, `seamless`, `streamline`, `underscore`,
  `underpin`, `delve`, `realm`, `landscape`, `tapestry`, `intricate`,
  `multifaceted`, `nuanced`, `crucial`, `vital`.
- Cut: `foster`, `garner`, `showcase`, `shed light on`, `align with`,
  `testament`, and `key` as an adjective. A domain term that matches stays, in
  code font: `landscape` as a page orientation.
- `must`, `should`, `can`: a requirement, a recommendation, an option.
- `for example` and `that is`, never `e.g.` and `i.e.`
- Noun clusters stop at three words.
- `-ing` forms as nouns only; a trailing gerund names no actor.
- they/them for a person whose pronouns are not stated.
- A domain term defined once; an abbreviation spelled out on first use.
- Code font for identifiers, paths, flags, and values.

## Say it once

One fact, one sentence, and a second only for the reason. Cover a sentence and
read on: if nothing is lost, cut it. A sentence opening with "so", "which
means", or "which keeps" folds into the one before. No summary section and no
closing recap. A text ends when the last fact ends.

## Paragraphs, lists, and sections

- One topic per paragraph, six sentences at most. The first sentence names the
  subject, the last carries the consequence.
- Three or more items go in a list: numbered for a sequence, bulleted for a set.
- Items start with the same part of speech.
- `**Label:** sentence` bullets are a table in disguise.
- Headings name the subject and stop: "Failure behavior", "Limits". Not
  "Getting started", not "What happens when it crashes", not a verb phrase.
- Sentence case for headings and items.

## Examples

Complete enough to paste, real enough to trust: plausible hosts and IDs,
secrets by reference. Show the multi-entry shape, because one entry makes a map
look like a scalar. A sentence ending in a colon introduces the block, and the
fence carries the language.

## Errors and output

Refusals and log lines verbatim, in a fenced block, so a search for the text
lands on the explanation. Cause first, then fix. Say where output goes and how
long it survives. Flat voice: no "Uh oh", no apology.

## Mechanics

- Bold for a label or the opening phrase of a callout only.
- One em dash per paragraph at most.
- No emoji in headings.
- No rule of three, no "not only X but also Y", no "from X to Y" ranges.
- Serial comma.
- Descriptive link text, never `here`.
- No `currently`, `now`, or `at this time` unless the timing is the point.
- US spelling, straight quotes.

## Claims that inform nothing

- The code restated: "`port` sets the port." Give the default, the range, and
  what happens when the port is taken.
- Paraphrased error text.
- Reassurance without a referent: "safe by default".
- An untested example.
- Placeholder residue: `<your-value-here>`, `2025-XX-XX`.
- Version drift: a flag or default the source no longer has.

## Where the sources conflict

1. Brevity against completeness: cut the words that carry no meaning, keep
   every word that carries structure.
2. Variety against repetition: vary the shape, never the terms.
3. Mood and person follow from who reads the text, so each skill sets them:

| Skill | Mood | Person |
|---|---|---|
| `technical-docs` | Indicative; imperative only inside a numbered procedure | The system is the subject; no `you` |
| `todo-list` | Imperative in every line | The reader performs the lines and is never named |
| `clear-output-style` | Imperative for what the reader performs | `you`, wherever the sentence is about the reader |

Where the reader is not named, a language with an impersonal form uses it:
Italian `si esegue` or `va eseguito`, never `esegui`.

## The pass over a finished draft

- Search for the cut words above, `allows you to`, `in order to`, `e.g.`,
  `i.e.`, and `currently`.
- Search for ` is ` and ` are ` followed by a past participle. Turn each passive
  around or justify it.
- Search for `ing,` and `ing.` at a clause end. Give each gerund an actor.
- Read the verbs alone. A verb of movement, birth, or arrival is a metaphor.
- One name per concept.
- Split any sentence that spans three lines.

`${CLAUDE_PLUGIN_ROOT}/scripts/style_lint.py` runs the searches, the perfect
tense, British spelling, `here` as link text, the second em dash, and the
sentence past 25 words. `--search` adds the passive and the gerund for a
reader to settle. On an edit, `--baseline OLD NEW` reports what NEW adds, so
the findings a page already carried leave the new one in plain sight.

## Provenance

The Elements of Style is public domain. Google's guide is CC BY 4.0 and
summarized here. ASD-STE100 is ASD's standard, paraphrased without its
dictionary. This file is CC BY 4.0.
