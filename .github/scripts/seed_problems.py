#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Seed parent (Problem) issues + per-language (Solution) sub-issues from problems.yaml,
add them to a GitHub Projects v2 board, and populate its custom fields.

Requires: `gh` CLI, logged in with a token that has the `project` scope
(`gh auth refresh -s project`), and write access to GH_REPO. Also requires `uv`
(https://docs.astral.sh/uv/) to resolve the PyYAML dependency declared above.

Env vars:
  GH_REPO            owner/repo to create issues in, e.g. Egg-Village-Python-Workshop/leetcode-tracker
  GH_PROJECT_OWNER    org login that owns the Project, e.g. Egg-Village-Python-Workshop
  GH_PROJECT_NUMBER   the Project's number (from its URL .../projects/<number>)
  LANGUAGES           comma-separated subset of languages to create solution sub-issues for
                       (default: python). Options: python,javascript-typescript,go,rust,java,other
  MAX_WEEK            optional; if set, only seed problems whose `week` is <= this value.
                       Used by the scheduled workflow so problems.yaml can hold several
                       future weeks in advance without them all being created immediately.

Usage:
  uv run .github/scripts/seed_problems.py problems.yaml
"""
from __future__ import annotations

import os
import sys

import yaml

from gh_project_lib import (
    add_item_to_project,
    add_sub_issue,
    create_issue,
    find_issue,
    get_project_meta,
    set_iteration_by_index,
    set_number,
    set_single_select,
)

LANGUAGE_LABELS = {
    "python": "lang:python",
    "javascript-typescript": "lang:javascript-typescript",
    "go": "lang:go",
    "rust": "lang:rust",
    "java": "lang:java",
    "other": "lang:other",
}


def seed_problem(repo: str, project_owner: str, project_number: str, project_meta: dict, problem: dict, languages: list[str]) -> None:
    pid = problem["id"]
    title_token = f"[{pid}]"
    parent_title = f"[{pid}] {problem['title']}"
    print(f"Problem {parent_title}")

    existing = find_issue(repo, title_token)
    parent_is_new = existing is None
    if existing:
        print("  parent exists, reusing")
        parent = existing
    else:
        body = f"Source: {problem.get('source_url', '')}"
        labels = ["type:problem", f"topic:{problem['topic']}", f"difficulty:{problem['difficulty']}"]
        parent = create_issue(repo, parent_title, body, labels)
        print(f"  created parent #{parent['number']}")

    parent_item_id = add_item_to_project(project_owner, project_number, parent["url"])
    fields = project_meta["fields"]
    if "Topic" in fields:
        set_single_select(project_meta["id"], parent_item_id, fields["Topic"], problem["topic"])
    if "Difficulty" in fields:
        set_single_select(project_meta["id"], parent_item_id, fields["Difficulty"], problem["difficulty"])
    # Only seed initial state on new issues: re-running the seed must not
    # clobber progress (Handle-Status) already recorded on existing items.
    if parent_is_new and "Handle-Status" in fields:
        set_single_select(project_meta["id"], parent_item_id, fields["Handle-Status"], "Backlog")
    if "Order" in fields:
        set_number(project_meta["id"], parent_item_id, fields["Order"], float(problem["order"]))
    if "Week" in fields and fields["Week"].get("type") == "ProjectV2IterationField":
        set_iteration_by_index(project_meta["id"], parent_item_id, fields["Week"], int(problem["week"]))

    for lang in languages:
        sub_title_token = f"[{pid}][{lang}]"
        sub_title = f"[{pid}][{lang}] {problem['title']}"
        existing_sub = find_issue(repo, sub_title_token)
        sub_is_new = existing_sub is None
        if existing_sub:
            print(f"  sub-issue ({lang}) exists, reusing")
            sub = existing_sub
        else:
            labels = ["type:solution", LANGUAGE_LABELS[lang]]
            sub = create_issue(repo, sub_title, "", labels)
            print(f"  created sub-issue #{sub['number']} ({lang})")
            add_sub_issue(parent["id"], sub["id"])

        sub_item_id = add_item_to_project(project_owner, project_number, sub["url"])
        if "Language" in fields:
            set_single_select(project_meta["id"], sub_item_id, fields["Language"], lang)
        # Don't reset Verified/Handle-Status on existing sub-issues, or a
        # re-seed wipes results recorded by record_result.py.
        if sub_is_new and "Handle-Status" in fields:
            set_single_select(project_meta["id"], sub_item_id, fields["Handle-Status"], "Backlog")
        if sub_is_new and "Verified" in fields:
            set_single_select(project_meta["id"], sub_item_id, fields["Verified"], "Unverified")


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: seed_problems.py <problems.yaml>", file=sys.stderr)
        sys.exit(1)

    repo = os.environ["GH_REPO"]
    project_owner = os.environ["GH_PROJECT_OWNER"]
    project_number = os.environ["GH_PROJECT_NUMBER"]
    languages = [lang.strip() for lang in os.environ.get("LANGUAGES", "python").split(",") if lang.strip()]
    max_week_raw = os.environ.get("MAX_WEEK", "").strip()
    max_week = int(max_week_raw) if max_week_raw else None

    with open(sys.argv[1], encoding="utf-8") as f:
        problems = yaml.safe_load(f)

    if max_week is not None:
        skipped = [p["id"] for p in problems if int(p["week"]) > max_week]
        problems = [p for p in problems if int(p["week"]) <= max_week]
        if skipped:
            print(f"MAX_WEEK={max_week}: skipping not-yet-due problem(s) {skipped}")

    project_meta = get_project_meta(project_owner, project_number)

    for problem in problems:
        seed_problem(repo, project_owner, project_number, project_meta, problem, languages)


if __name__ == "__main__":
    main()
