#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER_RE = re.compile(r"^(<<<<<<<|=======|>>>>>>>)")
SKIP_DIRS = {".git", "__pycache__", "downloads"}


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def main() -> int:
    findings: list[tuple[Path, int, str]] = []

    for path in sorted(ROOT.rglob("*")):
        if should_skip(path) or not path.is_file():
            continue

        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for lineno, line in enumerate(lines, start=1):
            if MARKER_RE.match(line):
                findings.append((path.relative_to(ROOT), lineno, line))

    if not findings:
        print("No merge conflict markers found.")
        return 0

    print("Merge conflict markers found:")
    for path, lineno, line in findings:
        print(f"  {path}:{lineno}: {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
