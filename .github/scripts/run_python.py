#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Generic verification runner for a Python solution file.

Dynamically imports the solution's `solve` function, calls it once per test
case (kwargs = the case's "input" object, so its keys must match `solve`'s
parameter names), and reports pass/fail + runtime + peak memory.

Usage:
  uv run .github/scripts/run_python.py <solution.py> <testcases.json>

testcases.json format:
  [{"input": {"<param_name>": <value>, ...}, "expected": <value>}, ...]

Prints exactly one JSON line to stdout:
  {"status": "passed"|"failed", "runtime_ms": <float>, "memory_kb": <float>, "details": "..."}
Exit code is 0 when all cases pass, 1 otherwise.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
import tracemalloc


def load_solution(path: str):
    spec = importlib.util.spec_from_file_location("solution", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: run_python.py <solution.py> <testcases.json>", file=sys.stderr)
        sys.exit(2)

    solve = load_solution(sys.argv[1])
    with open(sys.argv[2], encoding="utf-8") as f:
        cases = json.load(f)

    tracemalloc.start()
    start = time.perf_counter()
    failures = []
    for i, case in enumerate(cases):
        actual = solve(**case["input"])
        if actual != case["expected"]:
            failures.append(f"case {i}: expected {case['expected']!r}, got {actual!r}")
    elapsed_ms = (time.perf_counter() - start) * 1000
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        "status": "failed" if failures else "passed",
        "runtime_ms": round(elapsed_ms, 3),
        "memory_kb": round(peak_bytes / 1024, 1),
        "details": "; ".join(failures) if failures else f"{len(cases)} case(s) passed",
    }
    print(json.dumps(result))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
