#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Generate starter files for problems in problems.yaml so solving can start right away.

For every problem that has a `signature` block, creates (never overwrites):
  - testcases/<id>-<slug>.json                          from the problem's `examples` (shared by all runners)
  - <lang>/<topic>/<id>-<slug>/solution.<ext>           a stub with the solve signature
  - <lang>/<topic>/<id>-<slug>/README.md                problem statement + example table
One folder per problem and language: Go needs it (every solution is `package main` with
`Solve`, so two solutions can't share a directory), and the other languages follow for
consistency.

Stubs carry a `TODO(scaffold)` marker; CI and scripts/verify.sh skip files that still
contain it, so an untouched stub never records a "Failed" result. Delete the marker
line when you start implementing.

problems.yaml fields used (all optional except `signature` to be scaffolded):
  signature: {params: [{name: nums, type: "int[]"}, ...], returns: "int[]"}
  description: free text (Markdown)
  constraints: [list of strings]
  examples: [{input: {nums: [..], target: 9}, expected: [0, 1]}, ...]
Types: int, float, bool, string, and any of those suffixed with [] (nested allowed).
Rust maps them to i64, f64, bool, String, Vec<..>.

Env / usage:
  LANGUAGES   comma-separated (default: python); same values as seed_problems.py
  uv run .github/scripts/scaffold.py problems.yaml [--languages python,go]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

MARKER = "TODO(scaffold)"

LANG_DIR_EXT = {
    "python": ("python", "py"),
    "javascript-typescript": ("javascript", "js"),
    "go": ("go", "go"),
    "rust": ("rust", "rs"),
    "java": ("java", "java"),
}

SCALARS = {
    "python": {"int": "int", "float": "float", "bool": "bool", "string": "str"},
    "javascript-typescript": {"int": "number", "float": "number", "bool": "boolean", "string": "string"},
    "go": {"int": "int", "float": "float64", "bool": "bool", "string": "string"},
    "java": {"int": "int", "float": "double", "bool": "boolean", "string": "String"},
    "rust": {"int": "i64", "float": "f64", "bool": "bool", "string": "String"},
}


def split_type(t: str) -> tuple[str, int]:
    depth = 0
    while t.endswith("[]"):
        t = t[:-2]
        depth += 1
    if t not in ("int", "float", "bool", "string"):
        raise ValueError(f"unsupported type base '{t}'")
    return t, depth


def lang_type(lang: str, t: str) -> str:
    base, depth = split_type(t)
    s = SCALARS[lang][base]
    if lang == "python":
        return "list[" * depth + s + "]" * depth
    if lang == "go":
        return "[]" * depth + s
    if lang == "rust":
        return "Vec<" * depth + s + ">" * depth
    return s + "[]" * depth  # js (JSDoc) / java


def slug_of(problem: dict) -> str:
    url = problem.get("source_url", "").rstrip("/")
    if "/problems/" in url:
        return url.rsplit("/", 1)[-1]
    return re.sub(r"[^a-z0-9]+", "-", problem["title"].lower()).strip("-")


def stem(problem: dict) -> str:
    return f"{problem['id']}-{slug_of(problem)}"


def problem_dir(problem: dict, lang: str) -> Path | None:
    if lang not in LANG_DIR_EXT:
        return None
    return Path(LANG_DIR_EXT[lang][0]) / problem["topic"] / stem(problem)


def solution_path(problem: dict, lang: str) -> Path | None:
    d = problem_dir(problem, lang)
    return d / f"solution.{LANG_DIR_EXT[lang][1]}" if d else None


def readme_path(problem: dict, lang: str) -> Path | None:
    d = problem_dir(problem, lang)
    return d / "README.md" if d else None


def testcases_path(problem: dict) -> Path:
    return Path("testcases") / f"{stem(problem)}.json"


# ---- stub renderers -------------------------------------------------------

def stub_python(p: dict) -> str:
    sig = p["signature"]
    params = ", ".join(f"{a['name']}: {lang_type('python', a['type'])}" for a in sig["params"])
    return (
        f"def solve({params}) -> {lang_type('python', sig['returns'])}:\n"
        f"    # {MARKER}: implement, then delete this line\n"
        f"    raise NotImplementedError\n"
    )


def stub_javascript(p: dict) -> str:
    sig = p["signature"]
    names = ", ".join(a["name"] for a in sig["params"])
    doc_params = ", ".join(f"{a['name']}: {lang_type('javascript-typescript', a['type'])}" for a in sig["params"])
    return (
        "/**\n"
        f" * @param {{{{{doc_params}}}}} input\n"
        f" * @returns {{{lang_type('javascript-typescript', sig['returns'])}}}\n"
        " */\n"
        f"function solve({{ {names} }}) {{\n"
        f"  // {MARKER}: implement, then delete this line\n"
        "  throw new Error(\"not implemented\");\n"
        "}\n\n"
        "module.exports = { solve };\n"
    )


def stub_go(p: dict) -> str:
    sig = p["signature"]
    params = ", ".join(f"{a['name']} {lang_type('go', a['type'])}" for a in sig["params"])
    return (
        "package main\n\n"
        f"func Solve({params}) {lang_type('go', sig['returns'])} {{\n"
        f"\t// {MARKER}: implement, then delete this line\n"
        "\tpanic(\"not implemented\")\n"
        "}\n"
    )


def stub_java(p: dict) -> str:
    sig = p["signature"]
    params = ", ".join(f"{lang_type('java', a['type'])} {a['name']}" for a in sig["params"])
    return (
        "class Solution {\n"
        f"    static {lang_type('java', sig['returns'])} solve({params}) {{\n"
        f"        // {MARKER}: implement, then delete this line\n"
        "        throw new UnsupportedOperationException(\"not implemented\");\n"
        "    }\n"
        "}\n"
    )


def stub_rust(p: dict) -> str:
    sig = p["signature"]
    params = ", ".join(f"{a['name']}: {lang_type('rust', a['type'])}" for a in sig["params"])
    return (
        f"fn solve({params}) -> {lang_type('rust', sig['returns'])} {{\n"
        f"    // {MARKER}: implement, then delete this line\n"
        "    todo!()\n"
        "}\n"
    )


STUBS = {
    "python": stub_python,
    "javascript-typescript": stub_javascript,
    "go": stub_go,
    "java": stub_java,
    "rust": stub_rust,
}


# ---- README / testcases ---------------------------------------------------

def render_readme(p: dict) -> str:
    sig = p["signature"]
    out = [
        f"# [{p['id']}] {p['title']}",
        "",
        f"- 難度：{p['difficulty']}　主題：`{p['topic']}`",
        f"- 題目連結：{p.get('source_url', '')}",
        "",
    ]
    if p.get("description"):
        out += ["## 題目說明", "", p["description"].strip(), ""]
    out += ["## 函式簽名", "", "| 參數 | 型別 |", "| --- | --- |"]
    out += [f"| `{a['name']}` | `{a['type']}` |" for a in sig["params"]]
    out += ["", f"回傳：`{sig['returns']}`", ""]
    if p.get("constraints"):
        out += ["## 限制", ""] + [f"- {c}" for c in p["constraints"]] + [""]
    examples = p.get("examples") or []
    if examples:
        out += ["## 範例測資", "", "| # | input | expected |", "| --- | --- | --- |"]
        for i, ex in enumerate(examples, 1):
            inp = json.dumps(ex["input"], ensure_ascii=False)
            exp = json.dumps(ex["expected"], ensure_ascii=False)
            out.append(f"| {i} | `{inp}` | `{exp}` |")
        out += ["", f"完整測資見 `{testcases_path(p)}`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。", ""]
    return "\n".join(out)


def render_testcases(p: dict) -> str:
    order = [a["name"] for a in p["signature"]["params"]]
    rows = []
    for ex in p["examples"]:
        inp = {k: ex["input"][k] for k in order}
        rows.append("  " + json.dumps({"input": inp, "expected": ex["expected"]}, ensure_ascii=False))
    return "[\n" + ",\n".join(rows) + "\n]\n"


# ---- driver ---------------------------------------------------------------

def write_new(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  created {path}")
    return True


def scaffold_problem(p: dict, languages: list[str]) -> int:
    if "signature" not in p:
        print(f"[{p['id']}] {p['title']}: no `signature` in problems.yaml, skipping")
        return 0
    print(f"[{p['id']}] {p['title']}")
    n = 0
    if p.get("examples"):
        n += int(write_new(testcases_path(p), render_testcases(p)))
    for lang in languages:
        path = solution_path(p, lang)
        if path is None:
            print(f"  (no stub template for '{lang}')")
            continue
        n += int(write_new(path, STUBS[lang](p)))
        n += int(write_new(readme_path(p, lang), render_readme(p)))
    return n


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", default="problems.yaml")
    ap.add_argument("--languages", default=os.environ.get("LANGUAGES", "python"))
    ap.add_argument("--max-week", type=int, default=int(os.environ["MAX_WEEK"]) if os.environ.get("MAX_WEEK") else None)
    args = ap.parse_args()

    languages = [x.strip() for x in args.languages.split(",") if x.strip()]
    problems = yaml.safe_load(Path(args.file).read_text(encoding="utf-8"))
    if args.max_week is not None:
        problems = [p for p in problems if int(p["week"]) <= args.max_week]

    created = sum(scaffold_problem(p, languages) for p in problems)
    print(f"{created} file(s) created")


if __name__ == "__main__":
    sys.exit(main())
