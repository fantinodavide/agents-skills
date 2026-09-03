#!/usr/bin/env python3
"""Copy sections of rules/*.md into the skills that carry them inline.

Usage:
    python3 scripts/sync_rules.py            # rewrite every copy
    python3 scripts/sync_rules.py --check    # exit 1 when a copy differs
    python3 scripts/sync_rules.py --selftest

A skill marks a copy with two HTML comments. The opening one names the source
file under rules/ and the heading slug of the section it copies, and the closing
one ends the copy:

    <!-- rules: style.md#sentences -->
    ## Sentences
    ...
    <!-- /rules -->

The section runs from the heading to the next heading of the same or a higher
level. The slug is the heading text lowercased, with every run of characters
other than letters and digits replaced by one hyphen. Anything between the two
markers is replaced, so a skill-specific paragraph goes after the closing marker.
"""

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(ROOT, "rules")
SKILL_FILES = os.path.join(ROOT, "skills", "*", "SKILL.md")

BLOCK = re.compile(
    r"(?P<open><!-- rules: (?P<file>[^#\s]+)#(?P<slug>[^\s]+) -->\n)"
    r"(?P<body>.*?)"
    r"(?P<close><!-- /rules -->)",
    re.S,
)
HEADING = re.compile(r"^(?P<level>#{1,6})\s+(?P<text>.+?)\s*$")


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def section(source, slug):
    lines = source.splitlines()
    start = None
    level = None
    for index, line in enumerate(lines):
        heading = HEADING.match(line)
        if heading is None:
            continue
        if start is None:
            if slugify(heading.group("text")) == slug:
                start = index
                level = len(heading.group("level"))
        elif len(heading.group("level")) <= level:
            return "\n".join(lines[start:index]).rstrip("\n")
    if start is None:
        raise KeyError(slug)
    return "\n".join(lines[start:]).rstrip("\n")


def render(text, read_rules):
    def replace(match):
        source = read_rules(match.group("file"))
        body = section(source, match.group("slug"))
        return match.group("open") + body + "\n\n" + match.group("close")

    return BLOCK.sub(replace, text)


def read_rules_file(name):
    with open(os.path.join(RULES_DIR, name), encoding="utf-8") as handle:
        return handle.read()


def sync(check):
    stale = []
    for path in sorted(glob.glob(SKILL_FILES)):
        with open(path, encoding="utf-8") as handle:
            current = handle.read()
        try:
            wanted = render(current, read_rules_file)
        except KeyError as missing:
            print("%s: no section %s in rules/" % (path, missing), file=sys.stderr)
            return 2
        if wanted == current:
            continue
        stale.append(os.path.relpath(path, ROOT))
        if not check:
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(wanted)
    for path in stale:
        print("%s: %s" % (path, "out of date" if check else "updated"))
    if check and stale:
        return 1
    return 0


def selftest():
    rules = {"r.md": "# T\n\nintro\n\n## One\n\na\n\n### Sub\n\nb\n\n## Two\n\nc\n"}
    read = lambda name: rules[name]
    assert section(rules["r.md"], "one") == "## One\n\na\n\n### Sub\n\nb", "section ends at next same-level heading"
    assert section(rules["r.md"], "two") == "## Two\n\nc", "last section runs to the end"
    assert section(rules["r.md"], "sub") == "### Sub\n\nb", "nested section ends at a higher level"
    skill = "x\n<!-- rules: r.md#one -->\nstale\n<!-- /rules -->\nown text\n"
    wanted = "x\n<!-- rules: r.md#one -->\n## One\n\na\n\n### Sub\n\nb\n\n<!-- /rules -->\nown text\n"
    assert render(skill, read) == wanted, "block body is replaced, text outside stays"
    assert render(wanted, read) == wanted, "rendering is idempotent"
    assert slugify("Paragraphs, lists, and sections") == "paragraphs-lists-and-sections", "slug"
    try:
        render("<!-- rules: r.md#none -->\n<!-- /rules -->", read)
    except KeyError:
        pass
    else:
        raise AssertionError("a missing section raises")
    print("selftest ok")


def main(argv):
    if "--selftest" in argv:
        selftest()
        return 0
    return sync(check="--check" in argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
