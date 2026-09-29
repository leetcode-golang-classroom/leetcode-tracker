#!/usr/bin/env bash
# Wrapper around run_go.go: `go run` requires all source files to live in
# the same directory, so this stages the driver + the solution file into a
# temp dir before invoking it.
#
# Usage:
#   .github/scripts/run_go.sh <solution.go> <testcases.json>
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: run_go.sh <solution.go> <testcases.json>" >&2
  exit 2
fi

SOLUTION="$(realpath "$1")"
TESTCASES="$(realpath "$2")"
DRIVER="$(dirname "$(realpath "$0")")/run_go.go"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

cp "$DRIVER" "$TMPDIR/driver.go"
cp "$SOLUTION" "$TMPDIR/solution.go"

cd "$TMPDIR"
go run driver.go solution.go "$TESTCASES"
