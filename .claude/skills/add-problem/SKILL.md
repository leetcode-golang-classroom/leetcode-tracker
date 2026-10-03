---
name: add-problem
description: Register a new LeetCode problem in this repo end-to-end — append to problems.yaml, fill signature/examples, scaffold testcases + per-language stubs, and create the parent/sub-issues. Use when the user asks to pull/add/initialize a LeetCode problem (e.g. "拉取 valid palindrome 並建立 issue").
argument-hint: <title> [topic] [difficulty] [week] [languages]
---

# add-problem

Shared steps are fixed; only the parameters below vary. Ask (AskUserQuestion) only for parameters that can't be inferred.

## Parameters
| name | meaning | default / how to get |
|---|---|---|
| `TITLE` | LeetCode title | from `$ARGUMENTS` |
| `SLUG` | LeetCode url slug | kebab-case of TITLE; `SOURCE_URL=https://leetcode.com/problems/$SLUG/` |
| `TOPIC` | folder/topic label (e.g. `two-pointers`, `arrays-hashing`) | infer from problem; reuse existing topics in problems.yaml |
| `DIFFICULTY` | easy / medium / hard | from LeetCode |
| `WEEK` | study week | ask; suggest the week of neighbouring problems |
| `LANGUAGES` | comma list | `python,go,rust,java` (javascript has no stub template in scaffold.py — skip it and tell the user) |
| `ISSUES` | whether to create issues | yes |

## Steps (in order, from repo root)
1. **Add entry** — `uv run .github/scripts/add_problem.py --title "$TITLE" --topic $TOPIC --difficulty $DIFFICULTY --week $WEEK --source-url $SOURCE_URL`. It auto-assigns the next repo id (not LeetCode's number); note the printed id as `ID`.
2. **Complete the entry** in `problems.yaml` (the script leaves these empty), matching the style of existing entries:
   - `signature`: `params: [{name, type}]`, `returns`
   - Traditional-Chinese `description` in your own words, `constraints`, and ≥3 `examples` (input keys follow param order; include edge cases).
3. **Scaffold** — `uv run .github/scripts/scaffold.py problems.yaml --languages $LANGUAGES`. Creates `testcases/$ID-*.json` and `<lang>/$TOPIC/$ID-*/{solution.*,README.md}` stubs carrying `TODO(scaffold)`. Never overwrites. Validate with `python -m json.tool testcases/$ID-*.json`.
4. **Issues** — `uv run .github/scripts/create_issues.py --id $ID --languages $LANGUAGES`. Creates `[ID] Title` (labels `type:problem`, `topic:*`, `difficulty:*`) and `[ID][lang] Title` sub-issues (`type:solution`, `lang:*`), linked as native sub-issues; skips ones that already exist. Uses plain `gh`, so Project fields are not set (use `seed_problems.py` if the user wants those).
5. **Report** the files, issue numbers, and skipped languages. Do NOT commit/push/open a PR unless asked. Conventions if asked: branch `<slug>/<lang>`, commit `✨ (<slug>): message`.

## Notes
- Detailed pipeline: `docs/WORKFLOW.md`. Stubs with `TODO(scaffold)` are skipped by `scripts/verify.sh`/CI.
