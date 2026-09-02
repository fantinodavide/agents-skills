#!/usr/bin/env python3
"""Check text against the mechanical rules in clear-output-style.

The rules this script covers are the ones the "Before you send" section states as
searches. The rules it cannot cover need a reader: whether the answer leads, whether
the work was owned, whether a next action is runnable.

Usage:
    python3 scripts/style_lint.py [--search] FILE [FILE ...]
    cat reply.md | python3 scripts/style_lint.py -
    python3 scripts/style_lint.py --selftest

A finding prints as `path:line: rule: message`. The exit status is 1 when a file has
an error finding, and 0 when it has none. `--search` adds the checks a reader has to
settle, and a search finding never changes the exit status. Two checks sit there: the
passive, which the style allows where the actor is unknown, and the gerund at a clause
end, which the pattern cannot tell from a noun.

Sentence length and the em dash count run over a paragraph rather than a line, because
the markdown here wraps one sentence across several lines. A blank line, a fence, a
heading, a table row, and a new list item each end a paragraph, and a heading or a
table row stands as a paragraph of its own.

A line ending in `<!-- style-lint: ignore -->` is skipped, and so is every line under
a `<!-- style-lint: ignore-block -->` comment until the next blank line. The rule
inventories in the style files need it, because they quote the words they ban.
"""

import bisect
import re
import sys

FILLER = (
    r"it is important to note|in order to|be aware that|keep in mind|of course|"
    r"note that|obviously|simply|please|just|easy"
)
SIGNAL_FREE = (
    r"shed light on|align with|leverage|robust|seamless|streamline|underscore|"
    r"delve|realm|landscape|intricate|nuanced|crucial|vital|foster|showcase|testament"
)
BRITISH = r"behaviour|recognise|organisation|licence|centre|analyse|catalogue|colour"

IRREGULAR_PARTICIPLES = sorted(
    (
        "been run made taken given written done seen read put set found known left "
        "lost met paid said sold told thought understood won gone come become begun "
        "broken brought built bought caught chosen cut drawn driven eaten fallen felt "
        "fought forgotten got gotten grown had heard held hidden hit kept laid led "
        "let lit meant ridden risen sent shown shut spent spoken stood stuck struck "
        "sworn thrown worn"
    ).split(),
    key=len,
    reverse=True,
)

BASE_VERBS_IN_ED = (
    "need red bed seed feed speed shed deed indeed breed creed greed weed reed "
    "embed bleed exceed proceed succeed"
).split()

PARTICIPLE = r"(?!(?:%s)\b)(?:%s|\w+ed)" % (
    "|".join(BASE_VERBS_IN_ED),
    "|".join(IRREGULAR_PARTICIPLES),
)
ADVERB_OR_NEGATION = r"(?:(?:not|never|already|also|\w+ly)\s+)?"

PERFECT = re.compile(
    r"\b(?:has|have|had)\s+%s(?:%s)\b" % (ADVERB_OR_NEGATION, PARTICIPLE), re.I
)
PASSIVE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|get|gets|got)\s+%s(?:%s)\b"
    % (ADVERB_OR_NEGATION, PARTICIPLE),
    re.I,
)
LINK_TEXT = re.compile(r"\[(?:here|this|link)\]\(", re.I)

NON_GERUNDS = set(
    "anything everything nothing something during thing things ring rings string "
    "strings king kings wing wings sing swing sting cling sling bring morning "
    "evening spring sibling siblings building buildings ceiling meaning warning "
    "setting settings being beginning ending heading headings listing wording "
    "spelling engineering".split()
)
DETERMINERS = set(
    "a an the this that these those my your his her its our their no any some "
    "every each one two three another".split()
)
GERUND = re.compile(
    r",\s+(?P<opener>[A-Za-z]+ing)\b"
    r"|(?:(?P<lead>[A-Za-z]+)\s+)?(?P<trailer>[A-Za-z]+ing)(?=[,.])",
    re.I,
)

SENTENCE_LIMIT = 25
EM_DASH = "—"
FENCE = re.compile(r"^\s*```")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])[*_\"')\]]*\s+(?=[\"'(\[*_]*[A-Z`])|\s*\|\s*")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
TABLE_ROW = re.compile(r"^\s*\|")
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
LINE_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)]|>|#{1,6})\s+")
IGNORE_LINE = "<!-- style-lint: ignore -->"
IGNORE_BLOCK = "<!-- style-lint: ignore-block -->"


def matching(pattern):
    def find(line):
        for hit in pattern.finditer(line):
            yield hit.group(0).strip()

    return find


def find_gerunds(line):
    for hit in GERUND.finditer(line):
        word = hit.group("opener") or hit.group("trailer")
        if word.lower() in NON_GERUNDS:
            continue
        lead = hit.group("lead")
        if lead and lead.lower() in DETERMINERS:
            continue
        yield word


PROSE_RULES = [
    ("filler", matching(re.compile(r"\b(?:%s)\b" % FILLER, re.I)), "cut on sight: %s"),
    (
        "signal-free",
        matching(re.compile(r"\b(?:%s)\b" % SIGNAL_FREE, re.I)),
        "carries no signal: %s",
    ),
    ("latin", matching(re.compile(r"\b(?:e\.g\.|i\.e\.)")), "write it out: %s"),
    (
        "timing",
        matching(re.compile(r"\b(?:currently|at this time)\b", re.I)),
        "drop unless timing is the point: %s",
    ),
    ("perfect", matching(PERFECT), "perfect tense: %s"),
    ("spelling", matching(re.compile(r"\b(?:%s)\b" % BRITISH, re.I)), "US spelling: %s"),
]

LINK_RULES = [("link", matching(LINK_TEXT), "link text names the target: %s")]

SEARCH_RULES = [
    ("passive", matching(PASSIVE), "passive, name the actor: %s"),
    ("gerund", find_gerunds, "gerund at a clause end, give it an actor: %s"),
]

SEARCH_RULE_NAMES = {name for name, _, _ in SEARCH_RULES}


def strip_code_spans(line):
    return INLINE_CODE.sub("`", line)


def strip_link_targets(line):
    return LINK_TARGET.sub("] ", line)


def starts_paragraph(raw):
    return bool(HEADING.match(raw) or TABLE_ROW.match(raw) or LIST_ITEM.match(raw))


def stands_alone(raw):
    return bool(HEADING.match(raw) or TABLE_ROW.match(raw))


def paragraph_text(raw, prose):
    if TABLE_ROW.match(raw):
        return prose.strip().strip("|")
    return LINE_MARKER.sub("", prose).strip()


def split_sentences(text):
    start = 0
    for boundary in SENTENCE_SPLIT.finditer(text):
        yield start, text[start:boundary.start()]
        start = boundary.end()
    yield start, text[start:]


def line_at(offsets, numbers, position):
    index = max(bisect.bisect_right(offsets, position) - 1, 0)
    return numbers[index]


def paragraph_findings(paragraph, path):
    if not paragraph:
        return []
    findings = []
    offsets = []
    numbers = []
    offset = 0
    for number, part in paragraph:
        offsets.append(offset)
        numbers.append(number)
        offset += len(part) + 1
    text = " ".join(part for _, part in paragraph)
    if text.count(EM_DASH) > 1:
        findings.append(
            (path, numbers[0], "em-dash", "one em dash per paragraph at most")
        )
    for position, sentence in split_sentences(text):
        words = len(sentence.split())
        if words > SENTENCE_LIMIT:
            findings.append(
                (
                    path,
                    line_at(offsets, numbers, position),
                    "length",
                    "%d words, split it" % words,
                )
            )
    return findings


def body_start(lines):
    if not lines or lines[0].strip() != "---":
        return 0
    for offset, line in enumerate(lines[1:], 2):
        if line.strip() == "---":
            return offset
    return 0


def check(text, path="-", searches=False):
    findings = []
    paragraph = []
    in_fence = False
    in_ignore_block = False
    rules = PROSE_RULES + (SEARCH_RULES if searches else [])

    def flush():
        findings.extend(paragraph_findings(paragraph, path))
        paragraph.clear()

    lines = text.splitlines()
    start = body_start(lines)
    for number, raw in enumerate(lines[start:], start + 1):
        if FENCE.match(raw):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if IGNORE_BLOCK in raw:
            flush()
            in_ignore_block = True
            continue
        if not raw.strip():
            flush()
            in_ignore_block = False
            continue
        if in_ignore_block or IGNORE_LINE in raw:
            flush()
            continue
        coded = strip_code_spans(raw)
        prose = strip_link_targets(coded)
        for name, find, message in rules:
            for hit in find(prose):
                findings.append((path, number, name, message % hit))
        for name, find, message in LINK_RULES:
            for hit in find(coded):
                findings.append((path, number, name, message % hit))
        if starts_paragraph(raw):
            flush()
        paragraph.append((number, paragraph_text(raw, prose)))
        if stands_alone(raw):
            flush()
    flush()
    return findings


def selftest():
    def rules_of(text, searches=False):
        return [name for _, _, name, _ in check(text, searches=searches)]

    assert rules_of("We just did it.") == ["filler"]
    assert rules_of("Restart it in order to load the key.") == ["filler"]
    assert rules_of("The setup is easy.") == ["filler"]
    assert rules_of("It is important to note the flag.") == ["filler"]
    assert rules_of("A robust, seamless design.")[0] == "signal-free"
    assert rules_of("The defaults align with the plan.") == ["signal-free"]
    assert rules_of("The file has been changed.") == ["perfect"]
    assert rules_of("The test has run.") == ["perfect"]
    assert rules_of("The file has not been read.") == ["perfect"]
    assert rules_of("We have made it.") == ["perfect"]
    assert "passive" not in rules_of("The rows are skipped."), "passive is a search"
    assert "passive" in rules_of("The rows are skipped.", searches=True)
    assert "passive" in rules_of("The row will be sent.", searches=True)
    assert "passive" in rules_of("It is being done.", searches=True)
    assert "passive" in rules_of("The bug was found.", searches=True)
    assert rules_of("Click [here](https://x.y) now.") == ["link"]
    assert rules_of("Read the [upgrade notes](https://x.y) now.") == []
    assert check("Use `just` here.") == [], "inline code is not prose"
    assert check("```\njust\n```") == [], "fenced code is not prose"
    assert check("just <!-- style-lint: ignore -->") == [], "ignore marker holds"
    assert check("%s\njust" % IGNORE_BLOCK) == [], "ignore block holds"
    assert rules_of("word " * 30) == ["length"]
    assert rules_of("word " * 25) == []
    assert rules_of("| %s | %s |" % ("cell " * 15, "cell " * 15)) == [], "a table cell is a sentence"
    bold_lead = "**%s.** Word %s." % (("word " * 10).strip(), ("word " * 25).strip())
    assert check(bold_lead)[0][3] == "26 words, split it", "a sentence ends before the closing bold"
    wrapped = ("word " * 13).strip() + "\n" + ("word " * 12).strip() + " end."
    assert check(wrapped)[0][2] == "length", "a wrapped sentence is one sentence"
    assert check(wrapped)[0][3] == "26 words, split it"
    assert rules_of("A line %s one\nand a second %s two." % (EM_DASH, EM_DASH)) == [
        "em-dash"
    ], "an em dash pair spans the paragraph"
    assert check("A line %s one.\n\nA second %s two." % (EM_DASH, EM_DASH)) == []
    assert rules_of("Rotate the key, ensuring the login stays intact.", True) == [
        "gerund"
    ]
    assert rules_of("It holds nothing.", True) == []
    assert rules_of("During, the ring. A string.", True) == []
    assert check("Working memory is small, and it holds nothing.", searches=True) == []
    assert check("The parser rejects the file, so the load fails.") == []
    assert check("---\nname: just\n---\nA clean line.") == [], "frontmatter is not prose"
    print("selftest ok")


def read_source(path):
    if path == "-":
        return sys.stdin.buffer.read().decode("utf-8")
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def main(argv):
    if "--selftest" in argv:
        selftest()
        return 0
    searches = "--search" in argv
    paths = [a for a in argv if not a.startswith("-")] or ["-"]
    findings = []
    for path in paths:
        findings += check(read_source(path), path, searches)
    for path, number, name, message in findings:
        print("%s:%d: %s: %s" % (path, number, name, message))
    print("%d finding(s)" % len(findings), file=sys.stderr)
    return 1 if any(name not in SEARCH_RULE_NAMES for _, _, name, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
