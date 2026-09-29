#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Run a verification command for one problem+language solution, then record
the result on GitHub: update the sub-issue's Verified/Runtime/Memory Project
fields (latest snapshot) and post an issue comment (history of every run).

The Project only ever shows the *latest* value of a field, so the comment
trail is what lets you see how runtime/memory changed across attempts.

Env vars (same as seed_problems.py):
  GH_REPO, GH_PROJECT_OWNER, GH_PROJECT_NUMBER

Usage:
  uv run .github/scripts/record_result.py <problem-id> <language> -- <runner command...>

Example:
  uv run .github/scripts/record_result.py 0003 python -- \\
      uv run .github/scripts/run_python.py python/arrays-hashing/0003-two-sum.py testcases/0003-two-sum.json

The runner command must print one JSON line as its *last* line of stdout:
  {"status": "passed"|"failed", "runtime_ms": <float>, "memory_kb": <float>, "details": "..."}
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

from gh_project_lib import (
    add_item_to_project,
    comment_on_issue,
    find_issue,
    get_project_meta,
    set_number,
    set_single_select,
)


def parse_args(argv: list[str]) -> tuple[str, str, list[str]]:
    if "--" not in argv:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    sep = argv.index("--")
    problem_id, language = argv[:sep]
    runner_cmd = argv[sep + 1:]
    if not runner_cmd:
        print("error: no runner command given after --", file=sys.stderr)
        sys.exit(2)
    return problem_id, language, runner_cmd


def run_verifier(runner_cmd: list[str]) -> dict:
    proc = subprocess.run(runner_cmd, capture_output=True, text=True)
    stdout_lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    if not stdout_lines:
        print(proc.stdout, file=sys.stdout)
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError("runner produced no output; expected a trailing JSON line")
    try:
        return json.loads(stdout_lines[-1])
    except json.JSONDecodeError as exc:
        print(proc.stdout, file=sys.stdout)
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"could not parse runner's last output line as JSON: {exc}") from exc


def main() -> None:
    problem_id, language, runner_cmd = parse_args(sys.argv[1:])

    repo = os.environ["GH_REPO"]
    project_owner = os.environ["GH_PROJECT_OWNER"]
    project_number = os.environ["GH_PROJECT_NUMBER"]

    result = run_verifier(runner_cmd)
    print(f"result: {result}")

    sub_title_token = f"[{problem_id}][{language}]"
    sub_issue = find_issue(repo, sub_title_token)
    if sub_issue is None:
        raise RuntimeError(f"no sub-issue found with title containing '{sub_title_token}' — run seed_problems.py first")

    project_meta = get_project_meta(project_owner, project_number)
    fields = project_meta["fields"]
    item_id = add_item_to_project(project_owner, project_number, sub_issue["url"])

    verified_value = "Passed" if result["status"] == "passed" else "Failed"
    if "Verified" in fields:
        set_single_select(project_meta["id"], item_id, fields["Verified"], verified_value)
    if "Runtime (ms)" in fields and "runtime_ms" in result:
        set_number(project_meta["id"], item_id, fields["Runtime (ms)"], float(result["runtime_ms"]))
    if "Memory (KB)" in fields and "memory_kb" in result:
        set_number(project_meta["id"], item_id, fields["Memory (KB)"], float(result["memory_kb"]))

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    comment = (
        f"**Verification run — {timestamp}**\n\n"
        f"- Status: `{result['status']}`\n"
        f"- Runtime: {result.get('runtime_ms', 'n/a')} ms\n"
        f"- Memory: {result.get('memory_kb', 'n/a')} KB\n"
        f"- Details: {result.get('details', '')}\n"
    )
    comment_on_issue(sub_issue["url"], comment)
    print(f"recorded on {sub_issue['url']}")


if __name__ == "__main__":
    main()
