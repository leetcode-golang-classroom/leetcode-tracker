#!/usr/bin/env bash
# Local sanity check for solutions, using the same runners as CI
# (.github/workflows/verify-solutions.yml) but WITHOUT recording results to
# the GitHub Project.
#
# Usage:
#   scripts/verify.sh [<solution_path>...]
#
# With no arguments, verifies every solution file changed vs master
# (committed, staged, unstaged and untracked).
#
# Exit code: 0 if nothing failed, 1 if any solution failed, 2 on usage errors.
# Solutions that are skipped (no testcases, `other/`, missing toolchain,
# unimplemented scaffold stubs containing TODO(scaffold)) do
# not cause a failure.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="$ROOT/.github/scripts"
cd "$ROOT"

collect_changed() {
  {
    git diff --name-only master...HEAD -- python javascript go rust java other 2>/dev/null
    git diff --name-only HEAD -- python javascript go rust java other
    git ls-files --others --exclude-standard -- python javascript go rust java other
  } | sort -u
}

if [ $# -gt 0 ]; then
  files=("$@")
else
  mapfile -t files < <(collect_changed)
fi

if [ ${#files[@]} -eq 0 ]; then
  echo "no changed solution files to verify"
  exit 0
fi

passed=0 failed=0 skipped=0

for file in "${files[@]}"; do
  [ -z "$file" ] && continue
  file="${file#./}"
  if [ ! -f "$file" ]; then
    echo "SKIP  $file (not found / deleted)"
    skipped=$((skipped + 1))
    continue
  fi

  if grep -q 'TODO(scaffold)' "$file"; then
    echo "SKIP  $file (unimplemented scaffold stub)"
    skipped=$((skipped + 1))
    continue
  fi

  base="$(basename "$file")"
  case "$base" in
    solution.*) ;;
    *) continue ;; # README.md and other non-solution files in a problem folder
  esac

  dir="${file%%/*}"
  stem="$(basename "$(dirname "$file")")" # <NNNN>-<slug>
  id="${stem%%-*}"
  slug="${stem#*-}"
  testcases="testcases/${id}-${slug}.json"

  if [ ! -f "$testcases" ]; then
    echo "SKIP  $file (no testcases at $testcases)"
    skipped=$((skipped + 1))
    continue
  fi

  case "$dir" in
    python)     tool=uv;   cmd=(uv run "$SCRIPTS/run_python.py" "$file" "$testcases") ;;
    javascript) tool=node; cmd=(node "$SCRIPTS/run_javascript.mjs" "$file" "$testcases") ;;
    go)         tool=go;   cmd=(bash "$SCRIPTS/run_go.sh" "$file" "$testcases") ;;
    rust)       tool=rustc; cmd=(bash "$SCRIPTS/run_rust.sh" "$file" "$testcases") ;;
    java)       tool=javac; cmd=(bash "$SCRIPTS/run_java.sh" "$file" "$testcases") ;;
    other)
      echo "SKIP  $file (no generic runner for other/ yet)"
      skipped=$((skipped + 1))
      continue
      ;;
    *)
      echo "SKIP  $file (unknown language dir '$dir')"
      skipped=$((skipped + 1))
      continue
      ;;
  esac

  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "SKIP  $file (toolchain '$tool' not installed)"
    skipped=$((skipped + 1))
    continue
  fi

  out="$("${cmd[@]}" 2>&1)"
  rc=$?
  last="$(printf '%s\n' "$out" | tail -n 1)"

  status="$(printf '%s' "$last" | sed -n 's/.*"status"[[:space:]]*:[[:space:]]*"\([a-z]*\)".*/\1/p')"
  if [ "$rc" -eq 0 ] && [ "$status" = "passed" ]; then
    echo "PASS  $file  $last"
    passed=$((passed + 1))
  else
    echo "FAIL  $file (exit $rc)"
    printf '%s\n' "$out" | sed 's/^/      /'
    failed=$((failed + 1))
  fi
done

echo
echo "passed=$passed failed=$failed skipped=$skipped"
[ "$failed" -eq 0 ]
