#!/usr/bin/env bash
# Wrapper: compiles the driver (Runner.java) together with the solution file
# and runs it. The solution file must declare a package-private `class
# Solution` with `static <ret> solve(<params using the problem's natural
# types>)` (no external deps). It's copied to Solution.java before compiling
# since Java requires a *public* class's name to match its file name — a
# non-public class has no such restriction, so any original file name is
# fine. Compiled with `-parameters` so Runner can match testcases.json
# "input" keys to solve()'s parameters by name via reflection.
#
# Usage:
#   .github/scripts/run_java.sh <solution.java> <testcases.json>
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: run_java.sh <solution.java> <testcases.json>" >&2
  exit 2
fi

SOLUTION="$(realpath "$1")"
TESTCASES="$(realpath "$2")"
DRIVER="$(dirname "$(realpath "$0")")/Runner.java"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cp "$SOLUTION" "$TMPDIR/Solution.java"
javac -parameters -d "$TMPDIR" "$DRIVER" "$TMPDIR/Solution.java"
java -cp "$TMPDIR" Runner "$TESTCASES"
