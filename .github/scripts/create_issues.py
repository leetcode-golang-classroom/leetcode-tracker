#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Create the parent `[id] Title` issue and per-language sub-issues for one problem.

Everything variable (title/topic/difficulty) is read from problems.yaml by id;
only --id and --languages are parameters. Skips issues that already exist.

Usage:
  uv run .github/scripts/create_issues.py --id 0008 --languages python,go,rust,java,javascript-typescript
"""
from __future__ import annotations

import argparse
import json
import subprocess

import yaml

# issue-title language -> (folder, solution file); same keys as scaffold.py LANG_DIR_EXT
LANG_DIR_FILE = {"python": ("python", "solution.py"), "go": ("go", "solution.go"),
                 "rust": ("rust", "solution.rs"), "java": ("java", "solution.java"),
                 "javascript-typescript": ("javascript", "solution.js")}


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout.strip()


def find_issue(repo: str, title: str) -> dict | None:
    out = json.loads(gh("issue", "list", "-R", repo, "--state", "all", "--search", f'"{title}" in:title',
                        "--json", "number,title,id", "--limit", "20"))
    return next((i for i in out if i["title"] == title), None)


def ensure(repo: str, title: str, labels: str, body: str) -> dict:
    if (found := find_issue(repo, title)):
        print(f"exists  #{found['number']} {title}")
        return found
    url = gh("issue", "create", "-R", repo, "--title", title, "--label", labels, "--body", body)
    num = int(url.rsplit("/", 1)[1])
    issue = json.loads(gh("api", f"repos/{repo}/issues/{num}"))
    print(f"created #{num} {title}")
    return {"number": num, "id": issue["id"], "title": title}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="problems.yaml")
    ap.add_argument("--id", required=True)
    ap.add_argument("--languages", required=True)
    ap.add_argument("--repo", default=None)
    a = ap.parse_args()

    p = next(x for x in yaml.safe_load(open(a.file, encoding="utf-8")) if str(x["id"]) == a.id)
    repo = a.repo or json.loads(gh("repo", "view", "--json", "nameWithOwner"))["nameWithOwner"]
    slug = p["title"].lower().replace(" ", "-")
    folder = f"{p['topic']}/{p['id']}-{slug}"

    parent = ensure(repo, f"[{p['id']}] {p['title']}",
                    f"type:problem,topic:{p['topic']},difficulty:{p['difficulty']}",
                    f"LeetCode: {p.get('source_url', '')}\n\nWeek {p['week']} · testcases/{p['id']}-{slug}.json")
    for lang in a.languages.split(","):
        sub = ensure(repo, f"[{p['id']}][{lang}] {p['title']}",
                     f"type:solution,lang:{lang}",
                     f"Implement `{LANG_DIR_FILE.get(lang, (lang, 'solution'))[0]}/{folder}/"
                     f"{LANG_DIR_FILE.get(lang, (lang, 'solution'))[1]}` "
                     f"(see README.md there). Remove the `TODO(scaffold)` marker when done and run `scripts/verify.sh`.")
        subprocess.run(["gh", "api", f"repos/{repo}/issues/{parent['number']}/sub_issues",
                        "-F", f"sub_issue_id={sub['id']}"], capture_output=True)
        print(f"linked  #{sub['number']} -> #{parent['number']}")


if __name__ == "__main__":
    main()
