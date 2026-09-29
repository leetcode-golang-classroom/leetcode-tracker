#!/usr/bin/env bash
# Wrapper around run_rust.rs: compiles the driver with the solution spliced
# in via `include!(env!("SOLUTION_PATH"))`, then runs the resulting binary.
# No Cargo/serde needed — run_rust.rs hand-rolls its own minimal JSON value
# type/parser and is compiled directly with rustc.
#
# Usage:
#   .github/scripts/run_rust.sh <solution.rs> <testcases.json>
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: run_rust.sh <solution.rs> <testcases.json>" >&2
  exit 2
fi

SOLUTION="$(realpath "$1")"
TESTCASES="$(realpath "$2")"
DRIVER="$(dirname "$(realpath "$0")")/run_rust.rs"

TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

SOLUTION_PATH="$SOLUTION" rustc --edition 2021 -O "$DRIVER" -o "$TMPDIR/runner"
"$TMPDIR/runner" "$TESTCASES"
