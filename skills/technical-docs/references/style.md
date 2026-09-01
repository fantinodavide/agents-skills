# The merged style rule set

Three sources, reconciled into one set of rules for technical documentation:

- **The Elements of Style**, Strunk's composition principles (rules 8–18). Cut
  what does no work; put the meaning where the reader's eye lands.
- **The Google developer documentation style guide.** Conventions for developer
  docs: person, tense, mood, word choice, formatting.
- **ASD-STE100**, Simplified Technical English. Ambiguity control for a reader
  who cannot ask a follow-up question. The rule categories are paraphrased here;
  the standard's approved-word dictionary is ASD's and is not reproduced.

Where they disagree, the resolution is stated at the end.

## Sentences

- **Active voice.** All three agree. Passive only when the actor is genuinely
  unknown or irrelevant, and never two passives in a row. "The server refuses
  the config", not "the config is refused".
- **Simple tenses.** Present for what the system does, past for what already
  happened. No present perfect: "we received the report", not "we have received
  the report".
- **One instruction per sentence.** About 20 words in a step, about 25 in
  description. A sentence carrying two actions splits into two sentences.
- **No ellipsis for brevity.** Keep the subject, the verb, the article, and
  `that`. Dropping them to shorten a sentence buys length at the cost of a
  second reading.
- **Positive form.** "The parser rejects a list" beats "the parser does not
  accept anything other than an object". Reserve `not` for denial and contrast.
- **Specific over general, definite over vague, concrete over abstract.** Not
  "robust validation" but "the parser refuses a config that names both forms".
- **Literal terms, never figurative.** A metaphor asks the reader to translate
  before they can act, and two readers translate it differently. Not "the
  variables move the target" but "the variables name a different instance".
- **Related words together.** Subject beside verb, modifier beside what it
  modifies, relative pronoun straight after its antecedent.
- **The emphatic word last.** End the sentence on the consequence:
  "…and everyone signed in at the time signs out."
- **Parallel form for coordinate ideas.** List items, table cells, and clauses
  in a series take the same shape and the same part of speech.
- **Vary the shape, never the terms.** Successive loose sentences strung on
  "and" read as a drone; break them with a period or a semicolon.

## Words

- **One word, one meaning, every time.** Pick one verb for one action and reuse
  it: always "refuses", never "refuses" then "rejects" then "declines" for the
  same behavior. Synonym rotation is a virtue in prose and a defect in
  documentation.
- **The plainest common word.** `use` over `utilize`, `help` over `facilitate`,
  `about` over `approximately`, `lets you` over `allows you to`, `to` over
  `in order to`.
- **Cut on sight**: just, simply, please, easy, obviously, of course, note that.
  They add nothing, or they condescend to a reader who is stuck.
- **`must`, `should`, `can`** carry their exact senses: a requirement, a
  recommendation, an option. Never `should` where the system enforces `must`.
- **`for example` and `that is`**, not `e.g.` and `i.e.`
- **Noun clusters stop at three words.** "fuel pump valve" is fine; "high
  pressure fuel pump inlet valve assembly" becomes a phrase with a preposition.
- **`-ing` forms as nouns only.** No trailing gerund clauses: "…ensuring the
  login stays intact" names no actor and states no mechanism.
- **they/them** for a person whose pronouns you don't know.
- **Domain terms** stay when they are the real name of the thing, and get
  defined once on first use. Spell out an abbreviation on first use, with the
  abbreviation in parentheses after it.

## Say it once

The commonest defect in a careful draft is not a wrong sentence but a second
sentence restating the first from a new angle, and a third drawing the moral.
One fact, one sentence.

> Use a deploy key with read access to that one repository. The reader can read
> every file on the server, the key included, so a broader key exposes more than
> the fork. An address that needs no credential avoids the question entirely.

The first sentence gives the rule, the second the reason. The third repeats the
second as advice and goes. Three tests catch this before publishing:

- Cover a sentence and read on. If nothing is lost, it was scaffolding.
- Find the sentences that open with "and", "so", "which keeps", or "which
  means". Each is a candidate for folding into the sentence before it.
- Count how many sentences a paragraph spends on one fact. Two is the ceiling:
  the fact and its reason.

The same applies to a clause that restates its own subject: "the two are not
interchangeable" before explaining why is a sentence spent on suspense.

## Paragraphs, lists, and sections

- One topic per paragraph, about six sentences at most.
- The first sentence says what the paragraph is about; the last carries the
  consequence.
- Three or more steps or conditions go in a vertical list, not inside a
  sentence. Numbered for a sequence, bulleted for a set.
- Every list item starts with the same part of speech.
- Sentence case for headings and list items: first word and proper nouns only.

## Mechanics

- Serial comma: `suppliers, materials, and certifications`.
- Code font for identifiers, paths, flags, and literal values.
- Fenced blocks for command output and multi-line code, tagged with the
  language, introduced by a sentence ending in a colon.
- Descriptive link text. Never link the word `here`.
- No `currently`, `now`, or `at this time` unless the timing is the point.
- US spelling. Straight quotes, not curly.

## Where the three conflict

1. **Mood.** STE-100 requires the imperative for procedures; technical
   documentation describes the system rather than commanding the reader.
   Resolution: the imperative appears only inside a genuine numbered procedure,
   and the indicative carries everything else. STE's sentence mechanics apply to
   both.
2. **Brevity against completeness.** Strunk says omit needless words; STE says
   never omit a structural word. Resolution: cut the words that carry no
   meaning, keep every word that carries structure.
3. **Variety against repetition.** Strunk warns off monotonous sentence
   patterns; STE demands identical wording for identical things. Resolution:
   vary the sentence shape, never the terminology.
4. **Person.** Google writes in second person; a technical doc describes a system
   rather than a session with a reader. Resolution: the system, the file, or the
   setting is the subject of every sentence, and the reader never appears as
   `you`. A language with an impersonal form uses it, such as Italian `si esegue`
   or `va eseguito` for `esegui`.

## The pass over a finished draft

- Search the draft for `just`, `simply`, `please`, `easy`, `allows you to`,
  `in order to`, `e.g.`, `i.e.`, `currently`. Each hit is a cut or a swap.
- Search for `you`, `your`, and the second-person forms of the language. Each hit
  is a sentence to turn around onto the system.
- Read the verbs on their own. A verb that describes a physical movement, a
  birth, or an arrival is a metaphor standing where a plain verb belongs.
- Search for ` is ` and ` are ` followed by a past participle. Each hit is a
  passive to turn around or to justify.
- Search for `ing,` and `ing.` at a clause end. Each hit is a gerund that names
  no actor.
- Read the nouns for one concept across the page. If it has two names, it keeps
  the first one.
- Read the first and last sentence of each paragraph on their own. They should
  still tell the story.
- Count the words in any sentence that spans three lines. Split it.

## Provenance

The Elements of Style is public domain. The Google developer documentation style
guide is published under CC BY 4.0, and its rules are summarized here rather
than reproduced. ASD-STE100 is ASD's standard, free to download from
asd-ste100.org; this file paraphrases rule categories only. Documentation with a
contractual STE requirement is checked word by word against the official
dictionary, not against this summary.
