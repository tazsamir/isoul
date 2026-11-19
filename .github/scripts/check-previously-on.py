#!/usr/bin/env python3
"""Refuse to publish an Off the Stack article with a stale recap link."""

import datetime as dt
import pathlib
import re
import sys

SECTION = pathlib.Path("content/off-the-stack")
RECAP = re.compile(r"^> \*\*Previously on isoul\.uk:\*\* \[[^]]+\]\(([^)]+)\)", re.M)


def metadata(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing front matter: {path}")
    front = text.split("---", 2)[1]
    date = re.search(r"^date:\s*(\S+)", front, re.M)
    if not date:
        raise ValueError(f"Missing date: {path}")
    timestamp = dt.datetime.fromisoformat(date.group(1).replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=dt.timezone.utc)
    slug = re.search(r"^slug:\s*['\"]?([^'\"\s]+)", front, re.M)
    name = slug.group(1) if slug else (path.parent.name if path.name == "index.md" else path.stem)
    draft = bool(re.search(r"^draft:\s*true\s*$", front, re.M))
    return timestamp.astimezone(dt.timezone.utc), name, draft, text


def check(candidate):
    if not candidate.is_file() or SECTION not in candidate.parents:
        raise ValueError(f"Not an Off the Stack article: {candidate}")
    articles = []
    for path in SECTION.rglob("*.md"):
        if path.name == "_index.md" or path == candidate:
            continue
        timestamp, slug, draft, _ = metadata(path)
        if not draft:
            articles.append((timestamp, slug))
    if not articles:
        return
    latest = max(date for date, _ in articles)
    predecessors = [slug for date, slug in articles if date == latest]
    if len(predecessors) != 1:
        raise ValueError(f"Ambiguous latest published date {latest}: {predecessors}")
    expected = f"/off-the-stack/{predecessors[0]}/"
    _, _, _, text = metadata(candidate)
    recap = RECAP.search(text)
    if not recap or recap.group(1) != expected:
        got = recap.group(1) if recap else "(missing)"
        raise ValueError(f"Previously on must link to {expected}; found {got}")
    print(f"Verified Previously on: {expected}")


if __name__ == "__main__":
    try:
        check(pathlib.Path(sys.argv[1]))
    except (IndexError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
