# What makes documentation read as generated

Two families. The first is generic writing that could describe any product. The
second is documentation-specific: prose that sounds informative and tells the
reader nothing they can act on.

## Vocabulary that signals nothing

Cut on sight: leverage, robust, seamless, streamline, underscore, underpin,
delve, realm, landscape, tapestry, intricate, multifaceted, nuanced, crucial,
vital, key (as an adjective), foster, garner, showcase, shed light on, align
with, testament.

One of these is a slip. Three in a paragraph is a tell.

Replace with the specific thing: not "robust validation" but "the parser refuses
a config that names both forms".

## Sentence patterns

- **Trailing gerunds.** "...ensuring the login stays intact", "...highlighting
  the risk". Inanimate systems do not ensure or highlight. State the mechanism.
- **The rule of three.** Three adjectives, three clauses, three benefits, none
  of them load-bearing. Say the one that matters.
- **Negative parallelism.** "Not only a login, but also a tunnel." Say both
  plainly.
- **False ranges.** "From a single password to enterprise SSO." Ranges pad; the
  table already lists the options.
- **Didactic disclaimers.** "It's important to note", "keep in mind", "be aware
  that". Delete the frame and keep the fact.
- **Summary sections.** "In summary", "Overall", a closing paragraph restating
  the page. A reference document ends when the last fact ends.

## Formatting

- **Bold as emphasis spray.** Bold the first phrase of a callout, or the label
  of a rule. Not every occurrence of a term.
- **Inline-header bullets.** A list where every item is `**Thing:** sentence` is
  a table wearing a disguise. If the items share fields, use a table. If they
  don't, use prose.
- **Emoji in headings.** No.
- **Em dash pileups.** One per paragraph at most; a comma or a full stop usually
  reads better.

## Documentation-specific tells

- **Restating the code in English.** "The `port` field sets the port." Say what
  it defaults to, what happens when it's taken, what range is valid.
- **Paraphrased error text.** A reader searches for the string they saw. Quote
  it exactly, in a fenced block.
- **Invented reassurance.** "This is safe by default" without naming what the
  default is and what it protects against.
- **Untested examples.** An example that was never run against the parser is a
  bug report waiting in the queue.
- **Placeholder residue.** `<your-value-here>`, `2025-XX-XX`, `example.com` in a
  field that needs a real ID format. Show the shape of the real thing.
- **Version drift.** Naming a flag, a path, or a default that the current source
  no longer has. Check before shipping, not after a reader finds it.
