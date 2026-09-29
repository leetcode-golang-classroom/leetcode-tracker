#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Append one new problem to problems.yaml with an auto-computed id/order.

Reads the existing file only to find the current max `id`/`order` (so numbering
always continues from wherever it left off); the new entry is appended as raw
text so existing comments/formatting in problems.yaml are left untouched.

Usage:
  uv run .github/scripts/add_problem.py \\
    --title "Longest Consecutive Sequence" --topic arrays-hashing \\
    --difficulty medium --week 2 \\
    --source-url https://leetcode.com/problems/longest-consecutive-sequence/
"""
from __future__ import annotations

import argparse

import yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="problems.yaml")
    parser.add_argument("--title", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--difficulty", required=True, choices=["easy", "medium", "hard"])
    parser.add_argument("--week", required=True, type=int)
    parser.add_argument("--source-url", default="")
    args = parser.parse_args()

    with open(args.file, encoding="utf-8") as f:
        problems = yaml.safe_load(f) or []

    next_id = max((int(p["id"]) for p in problems), default=0) + 1
    next_order = max((int(p["order"]) for p in problems), default=0) + 1
    id_str = f"{next_id:04d}"

    block = (
        f'\n- id: "{id_str}"\n'
        f'  title: "{args.title}"\n'
        f"  topic: {args.topic}\n"
        f"  difficulty: {args.difficulty}\n"
        f"  order: {next_order}\n"
        f"  week: {args.week}\n"
        f"  source_url: {args.source_url}\n"
    )
    with open(args.file, "a", encoding="utf-8") as f:
        f.write(block)

    print(f"appended id={id_str} order={next_order} week={args.week} -> {args.title}")


if __name__ == "__main__":
    main()
