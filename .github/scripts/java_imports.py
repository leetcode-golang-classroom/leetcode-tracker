#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Add missing `import` lines for common JDK classes used in a Java solution.

google-java-format sorts imports and drops unused ones but cannot add missing
ones, so this fills that gap for the classes LeetCode solutions usually need
(java.util, java.util.function, java.util.stream). Only classes that are used
and not already imported (explicitly or via a wildcard) are added; ordering is
left to `google-java-format --fix-imports-only`.

Usage:
  java_imports.py [--check] <solution.java>...

Without --check the files are rewritten in place. With --check nothing is
written; exit code 1 means some file has missing imports.
"""
from __future__ import annotations

import re
import sys

PACKAGES = {
    "java.util": """ArrayDeque ArrayList Arrays BitSet Collections Comparator Deque HashMap
        HashSet Iterator LinkedHashMap LinkedHashSet LinkedList List Map Objects
        Optional PriorityQueue Queue Set Stack TreeMap TreeSet""",
    "java.util.function": "BiFunction Consumer Function Predicate Supplier",
    "java.util.stream": "Collectors IntStream Stream",
}
CLASSES = {name: pkg for pkg, names in PACKAGES.items() for name in names.split()}

STRING_OR_COMMENT = re.compile(
    r'//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\\n])*"|\'(?:\\.|[^\'\\\n])*\'', re.S
)
IMPORT = re.compile(r"^import\s+(?:static\s+)?([\w.]+(?:\.\*)?)\s*;", re.M)


def missing_imports(source: str) -> list[str]:
    imported = set(IMPORT.findall(source))
    code = IMPORT.sub("", STRING_OR_COMMENT.sub("", source))
    needed = []
    for name, pkg in sorted(CLASSES.items()):
        if f"{pkg}.{name}" in imported or f"{pkg}.*" in imported:
            continue
        # a bare use, not a member access (`foo.List`) or a qualified name
        if re.search(rf"(?<![\w.]){name}\b", code):
            needed.append(f"{pkg}.{name}")
    return needed


def add_imports(source: str, names: list[str]) -> str:
    lines = "".join(f"import {n};\n" for n in names)
    existing = list(IMPORT.finditer(source))
    if existing:
        end = existing[-1].end()
        return source[:end] + "\n" + lines.rstrip("\n") + source[end:]
    package = re.search(r"^package\s+[\w.]+\s*;[^\n]*\n", source, re.M)
    if package:
        return source[: package.end()] + "\n" + lines + source[package.end():]
    return lines + "\n" + source


def main() -> int:
    args = sys.argv[1:]
    check = "--check" in args
    files = [a for a in args if a != "--check"]
    rc = 0
    for path in files:
        with open(path, encoding="utf-8") as f:
            source = f.read()
        names = missing_imports(source)
        if not names:
            continue
        if check:
            print(f"{path}: missing import(s): {', '.join(names)}")
            rc = 1
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(add_imports(source, names))
            print(f"{path}: added {', '.join(names)}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
