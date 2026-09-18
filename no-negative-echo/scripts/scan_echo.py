#!/usr/bin/env python3
"""Literal scanner for suspected negative-echo terms.

This is intentionally simple: it reports occurrences but does not decide
whether they are valid. Semantic classification belongs to the agent/user.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

DEFAULT_IGNORES = {".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", ".venv", "venv"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan text files for literal terms associated with rejected/superseded ideas."
    )
    parser.add_argument(
        "--forbidden",
        action="append",
        default=[],
        help="Literal term to search for. Repeat for multiple terms.",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Use case-sensitive matching (default: case-insensitive).",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Files or directories to scan.",
    )
    return parser.parse_args()


def iter_files(paths: list[str]):
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            print(f"warning: path not found: {path}", file=sys.stderr)
            continue
        if path.is_file():
            yield path
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file():
                continue
            if any(part in DEFAULT_IGNORES for part in candidate.parts):
                continue
            yield candidate


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError as exc:
        print(f"warning: cannot read {path}: {exc}", file=sys.stderr)
        return None
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("utf-8-sig")
        except UnicodeDecodeError:
            return None


def main() -> int:
    args = parse_args()
    terms = [t for t in args.forbidden if t]
    if not terms:
        print("error: provide at least one --forbidden term", file=sys.stderr)
        return 2

    normalized_terms = terms if args.case_sensitive else [t.casefold() for t in terms]
    hits = 0

    for path in iter_files(args.paths):
        text = read_text(path)
        if text is None:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            haystack = line if args.case_sensitive else line.casefold()
            matched = [original for original, needle in zip(terms, normalized_terms) if needle in haystack]
            if matched:
                hits += 1
                joined = ", ".join(repr(item) for item in matched)
                print(f"{path}:{line_no}: [{joined}] {line.strip()}")

    if hits:
        print(f"\n{hits} suspicious line(s) found. Review semantically before editing.")
        return 1

    print("No literal matches found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
