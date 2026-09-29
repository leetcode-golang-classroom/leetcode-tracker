#!/usr/bin/env node
/**
 * Generic verification runner for a JavaScript solution file.
 *
 * Convention: the solution file is CommonJS and exports a `solve(input)`
 * function, where `input` is the whole test case's "input" object (the
 * solution destructures whatever fields it needs out of it).
 *
 * Usage:
 *   node .github/scripts/run_javascript.mjs <solution.js> <testcases.json>
 *
 * testcases.json format:
 *   [{"input": {...}, "expected": <value>}, ...]
 *
 * Prints one JSON line to stdout:
 *   {"status": "passed"|"failed", "runtime_ms": <float>, "memory_kb": <float>, "details": "..."}
 * Memory is an approximate V8 heap delta (no forced GC), not a true peak.
 */
import { createRequire } from "module";
import { readFileSync } from "fs";
import { resolve } from "path";

function deepEqual(a, b) {
  if (Object.is(a, b)) return true;
  if (typeof a !== typeof b) return false;
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((v, i) => deepEqual(v, b[i]));
  }
  if (a && b && typeof a === "object") {
    const aKeys = Object.keys(a);
    const bKeys = Object.keys(b);
    if (aKeys.length !== bKeys.length) return false;
    return aKeys.every((k) => deepEqual(a[k], b[k]));
  }
  return a === b;
}

function main() {
  const [solutionPath, testcasesPath] = process.argv.slice(2);
  if (!solutionPath || !testcasesPath) {
    console.error("usage: run_javascript.mjs <solution.js> <testcases.json>");
    process.exit(2);
  }

  const require = createRequire(import.meta.url);
  const { solve } = require(resolve(solutionPath));
  const cases = JSON.parse(readFileSync(testcasesPath, "utf-8"));

  const memBefore = process.memoryUsage().heapUsed;
  const start = process.hrtime.bigint();
  const failures = [];
  cases.forEach((testCase, i) => {
    const actual = solve(testCase.input);
    if (!deepEqual(actual, testCase.expected)) {
      failures.push(`case ${i}: expected ${JSON.stringify(testCase.expected)}, got ${JSON.stringify(actual)}`);
    }
  });
  const elapsedMs = Number(process.hrtime.bigint() - start) / 1e6;
  const memAfter = process.memoryUsage().heapUsed;

  const result = {
    status: failures.length ? "failed" : "passed",
    runtime_ms: Math.round(elapsedMs * 1000) / 1000,
    memory_kb: Math.round(Math.max(0, memAfter - memBefore) / 1024 * 10) / 10,
    details: failures.length ? failures.join("; ") : `${cases.length} case(s) passed`,
  };
  console.log(JSON.stringify(result));
  process.exit(failures.length ? 1 : 0);
}

main();
