#!/usr/bin/env python3
"""Deterministic checks for an enterprise-radius-review output.

Checks structure (advisory line, Scope & Method, Radius Summary) and
recomputes the current credible radius from the Radius Summary table using
the ceiling rule, then compares it with the radius the review states.

It does NOT judge whether the evidence labels themselves are right; that
stays with the reviewer and a human.

Usage:
  python3 check_review.py REVIEW.md
  python3 check_review.py REVIEW.md --expected calibration/case-01-small-prototype.md \
      --log calibration/run-log.md --note "fresh session, run 2"
  python3 check_review.py -            # read the review from stdin

Exit codes: 0 = PASS, 1 = FAIL, 2 = usage or file error.
Standard library only; Python 3.8+.
"""
import argparse
import datetime
import os
import re
import sys

LEVELS = ("Verified", "Documented", "Reported", "Unknown")
STATUSES = ("Reached", "Not reached", "N/A")


def section(text, heading):
    """Body of a '## heading' section, up to the next '## ' heading."""
    m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$", text, re.M)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^##\s", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def clean(cell):
    return cell.replace("*", "").replace("`", "").strip()


def match_word(value, options):
    v = value.lower()
    for o in sorted(options, key=len, reverse=True):  # "Not reached" before "Reached"
        if v.startswith(o.lower()):
            return o
    return None


def parse_summary(body):
    rows = {}
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [clean(c) for c in line.strip().strip("|").split("|")]
        m = re.match(r"(?:R(?:adius)?\s*)?([1-5])\b", cells[0])
        if m and len(cells) >= 4:
            rows.setdefault(int(m.group(1)), cells)
    return rows


def compute(rows):
    """Apply the ceiling rule. Returns (radius, ceiling, problems)."""
    problems = []
    status = {}
    for n in range(1, 6):
        if n not in rows:
            problems.append("Radius Summary is missing the row for Radius %d" % n)
            continue
        _, st, ev, gap = rows[n][:4]
        s = match_word(st, STATUSES)
        if not s:
            problems.append("Radius %d: Status must be Reached, Not reached or N/A (got %r)" % (n, st))
            continue
        status[n] = s
        if s == "N/A":
            continue
        e = match_word(ev, LEVELS)
        g = match_word(gap, ("Yes", "No"))
        if not e:
            problems.append("Radius %d: Core evidence must be one of %s (got %r)" % (n, "/".join(LEVELS), ev))
        if not g:
            problems.append("Radius %d: Unknown material gap must be Yes or No (got %r)" % (n, gap))
        if e and g:
            qualifies = e in ("Verified", "Documented") and g == "No"
            if s == "Reached" and not qualifies:
                problems.append(
                    "Radius %d is marked Reached but core evidence is %s and Unknown material gap is %s; "
                    "the ceiling rule requires Verified/Documented and no Unknown gap" % (n, e, g))
            if s == "Not reached" and qualifies:
                problems.append(
                    "Radius %d is marked Not reached but its row qualifies as Reached; "
                    "fix the row or name the missing evidence" % n)
    seen_na = False
    for n in range(1, 6):
        if status.get(n) == "N/A":
            seen_na = True
        elif seen_na and status.get(n) == "Reached":
            problems.append("Radius %d is Reached but a lower radius is N/A" % n)
    radius = 0
    for n in range(1, 6):
        if status.get(n) == "Reached":
            radius = n
        else:
            break
    if radius == 5:
        ceiling = "none"
    elif status.get(radius + 1) == "N/A":
        ceiling = "scope"
    else:
        ceiling = "Radius %d" % (radius + 1)
    return radius, ceiling, problems


def parse_ceiling(s):
    s = clean(s)
    m = re.match(r"(?:R(?:adius)?\s*)?([1-5])\b", s)
    if m:
        return "Radius %s" % m.group(1)
    low = s.lower()
    for w in ("scope", "none"):
        if low.startswith(w):
            return w
    return None


def stated(body):
    r = re.search(r"^\s*\**Radius:?\**:?\s*\**\s*([0-5])\b", body, re.M | re.I)
    c = re.search(r"^\s*\**Ceiling:?\**:?\s*(.+)$", body, re.M | re.I)
    return (int(r.group(1)) if r else None), (parse_ceiling(c.group(1)) if c else None)


def expected(case_text):
    r = re.search(r"Current credible radius:\s*\**\s*([0-5])\b", case_text, re.I)
    c = re.search(r"Ceiling set by:\s*(.+)$", case_text, re.I | re.M)
    return (int(r.group(1)) if r else None), (parse_ceiling(c.group(1)) if c else None)


def check(text):
    """Returns (problems, computed_radius, computed_ceiling)."""
    problems = []
    if not re.search(r"^>\s*.*\badvisory\b", text, re.M | re.I):
        problems.append("Missing the advisory line (a '> Advisory review ...' blockquote)")
    sm = section(text, "Scope & Method")
    if sm is None:
        problems.append("Missing '## Scope & Method' section")
    else:
        for label in ("Unit rated", "Ran", "Read"):
            # Accept "- Ran:", "- **Ran:**", "- **Ran (on a copy):**" and similar.
            if not re.search(r"^\s*(?:[-*]\s*)?\**\s*" + label + r"\b", sm, re.M | re.I):
                problems.append("Scope & Method is missing '%s:'" % label)
    radius = ceiling = None
    rs = section(text, "Radius Summary")
    if rs is None:
        problems.append("Missing '## Radius Summary' table")
    else:
        radius, ceiling, p = compute(parse_summary(rs))
        problems += p
    cr = section(text, "Current Credible Radius")
    if cr is None:
        problems.append("Missing '## Current Credible Radius' section")
    elif radius is not None:
        s_r, s_c = stated(cr)
        if s_r is None:
            problems.append("Current Credible Radius has no 'Radius: N' line")
        elif s_r != radius:
            problems.append("Stated radius %d but the Radius Summary supports %d (ceiling rule)" % (s_r, radius))
        if s_c is None:
            problems.append("Current Credible Radius has no 'Ceiling: Radius M | scope | none' line")
        elif s_c != ceiling:
            problems.append("Stated ceiling '%s' but the Radius Summary gives '%s'" % (s_c, ceiling))
    return problems, radius, ceiling


def skill_version():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "SKILL.md")
    try:
        with open(path, encoding="utf-8") as f:
            m = re.search(r"^version:\s*(\S+)", f.read(), re.M)
            return m.group(1) if m else "?"
    except OSError:
        return "?"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("review", help="review Markdown file, or - for stdin")
    ap.add_argument("--expected", help="calibration case file to score against")
    ap.add_argument("--log", help="run-log.md to append a result row to (needs --expected)")
    ap.add_argument("--note", default="", help="note for the run-log row")
    a = ap.parse_args(argv)
    if a.log and not a.expected:
        ap.error("--log needs --expected")
    try:
        if a.review == "-":
            text = sys.stdin.read()
        else:
            with open(a.review, encoding="utf-8") as f:
                text = f.read()
        case = None
        if a.expected:
            with open(a.expected, encoding="utf-8") as f:
                case = f.read()
    except OSError as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2

    problems, radius, ceiling = check(text)
    structure_ok = not problems
    if radius is not None:
        print("Computed: Radius %d, ceiling %s" % (radius, ceiling))

    match = None
    if case is not None:
        e_r, e_c = expected(case)
        if e_r is None or e_c is None:
            print("ERROR: case file has no parsable 'Current credible radius:' / 'Ceiling set by:' "
                  "(is it registered yet?)", file=sys.stderr)
            return 2
        match = (radius, ceiling) == (e_r, e_c)
        print("Expected: Radius %d, ceiling %s -> %s" % (e_r, e_c, "MATCH" if match else "MISMATCH"))
        if not match:
            problems.append("Result does not match the pre-registered expectation")

    for p in problems:
        print("FAIL: " + p)
    print("PASS" if not problems else "RESULT: FAIL (%d problem%s)" % (len(problems), "" if len(problems) == 1 else "s"))

    if a.log:
        row = "| %s | %s | %s | %s | Radius %s / %s | Radius %s / %s | not checked | %s | %s | %s |\n" % (
            datetime.date.today().isoformat(),
            os.path.basename(a.expected).split("-")[1] if "-" in os.path.basename(a.expected) else a.expected,
            skill_version(), "?", e_r, e_c, radius, ceiling,
            "yes" if structure_ok else "no", "yes" if not problems else "no",
            (a.note + " " if a.note else "") + "(check_review.py)")
        with open(a.log, "a", encoding="utf-8") as f:
            f.write(row)
        print("Logged to %s" % a.log)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
