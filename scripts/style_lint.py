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
findings, 0 when it has none. `--search` adds the checks that need a reader to settle,
which is why they stay out of the default run.

A line ending in `<!-- style-lint: ignore -->` is skipped, and so is every line under
a `<!-- style-lint: ignore-block -->` comment until the next blank line. The rule
inventories in the style files need it, because they quote the words they ban.
"""

import re
import sys

FILLER = r"just|simply|please|obviously|of course|note that|keep in mind|be aware that"
SIGNAL_FREE = (
    r"leverage|robust|seamless|streamline|underscore|delve|realm|landscape|"
    r"intricate|nuanced|crucial|vital|foster|showcase|shed light on|testament"
)
BRITISH = r"behaviour|recognise|organisation|licence|centre|analyse|catalogue|colour"

ERRORS = [
    ("filler", re.compile(r"\b(%s)\b" % FILLER, re.I), "cut on sight: %s"),
    ("signal-free", re.compile(r"\b(%s)\b" % SIGNAL_FREE, re.I), "carries no signal: %s"),
    ("latin", re.compile(r"\b(e\.g\.|i\.e\.)"), "write it out: %s"),
    ("timing", re.compile(r"\b(currently|at this time)\b", re.I), "drop unless timing is the point: %s"),
    ("perfect", re.compile(r"\b(has|have|had)\s+(been|\w+ed)\b", re.I), "perfect tense: %s"),
    ("passive", re.compile(r"\b(is|are|was|were)\s+(\w+ed|written|made|given|taken|shown|held|kept|built|sent)\b", re.I), "passive, name the actor: %s"),
    ("spelling", re.compile(r"\b(%s)\b" % BRITISH, re.I), "US spelling: %s"),
    ("link", re.compile(r"\[(here|this|link)\]\(", re.I), "link text names the target: %s"),
]

# A gerund at a clause end needs a reader, not a rule. "Working memory is small"
# is correct, and "ensuring the login stays intact" is the defect. The pattern
# cannot separate them, so it reports under --search and never fails a run.
SEARCHES = [
    ("gerund", re.compile(r"\b\w+ing[,.]", re.I), "gerund at a clause end, give it an actor: %s"),
]

SENTENCE_LIMIT = 25
FENCE = re.compile(r"^\s*```")
INLINE_CODE = re.compile(r"`[^`]*`")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`])")
IGNORE_LINE = "<!-- style-lint: ignore -->"
IGNORE_BLOCK = "<!-- style-lint: ignore-block -->"


def strip_noise(line):
    """Remove inline code, links targets, and headings, which the rules do not govern."""
    line = INLINE_CODE.sub(" ", line)
    line = re.sub(r"\]\([^)]*\)", "] ", line)
    return line


def check(text, path="-", searches=False):
    findings = []
    in_fence = False
    in_ignore_block = False
    lines = text.splitlines()
    start = 0
    if lines and lines[0].strip() == "---":  # YAML frontmatter is metadata, not prose
        for offset, line in enumerate(lines[1:], 2):
            if line.strip() == "---":
                start = offset
                break
    for number, raw in enumerate(lines[start:], start + 1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if IGNORE_BLOCK in raw:
            in_ignore_block = True
            continue
        if not raw.strip():
            in_ignore_block = False
            continue
        if in_ignore_block or IGNORE_LINE in raw:
            continue
        line = strip_noise(raw)
        for name, pattern, message in ERRORS + (SEARCHES if searches else []):
            for hit in pattern.finditer(line):
                findings.append((path, number, name, message % hit.group(0).strip()))
        if raw.count("—") > 1:
            findings.append((path, number, "em-dash", "one em dash per paragraph at most"))
        for sentence in SENTENCE_SPLIT.split(line.lstrip("#-*> ")):
            words = len(sentence.split())
            if words > SENTENCE_LIMIT:
                findings.append((path, number, "length", "%d words, split it" % words))
    return findings


def selftest():
    assert check("We just did it.")[0][2] == "filler"
    assert check("A robust, seamless design.")[0][2] == "signal-free"
    assert check("The file has been changed.")[0][2] == "perfect"
    assert check("The rows are skipped.")[0][2] == "passive"
    assert check("Use `just` here.") == [], "inline code is not prose"
    assert check("```\njust\n```") == [], "fenced code is not prose"
    assert check("just <!-- style-lint: ignore -->") == [], "ignore marker holds"
    assert check("%s\njust" % IGNORE_BLOCK) == [], "ignore block holds"
    assert check("word " * 30) and check("word " * 30)[0][2] == "length"
    assert check("Working memory is small, and it holds nothing.") == []
    assert check("Working memory is small, and it holds nothing.", searches=True)[0][2] == "gerund"
    assert check("The parser rejects the file, so the load fails.") == []
    assert check("---\nname: just\n---\nA clean line.") == [], "frontmatter is not prose"
    print("selftest ok")


def main(argv):
    if "--selftest" in argv:
        selftest()
        return 0
    searches = "--search" in argv
    paths = [a for a in argv if not a.startswith("-")] or ["-"]
    findings = []
    for path in paths:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        findings += check(text, path, searches)
    for path, number, name, message in findings:
        print("%s:%d: %s: %s" % (path, number, name, message))
    print("%d finding(s)" % len(findings), file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
