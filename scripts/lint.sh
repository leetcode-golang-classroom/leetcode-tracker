#!/usr/bin/env bash
# Local lint/format check for solutions (python: ruff, javascript: biome,
# go: gofmt + go vet). rust/java/other are not configured yet and are skipped.
#
# Usage:
#   scripts/lint.sh [--fix] [<solution_path>...]
#
# With no paths, checks every solution.* file changed vs master (committed,
# staged, unstaged, untracked). --fix applies formatting / safe lint fixes
# (python and javascript; gofmt for go).
#
# Exit code: 0 if nothing failed, 1 if any check failed. Missing toolchains,
# unconfigured languages and unimplemented scaffold stubs (TODO(scaffold))
# are skipped, not failures.
[ -n "${BASH_VERSION:-}" ] || exec bash "$0" "$@" # re-run under bash when invoked via `sh`
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="$ROOT/.github/scripts"
BIOME_VERSION="2.5.15"
cd "$ROOT"

fix=0
if [ "${1:-}" = "--fix" ]; then fix=1; shift; fi

base=master
git rev-parse --verify -q master >/dev/null || base=origin/master

collect_changed() {
  {
    git diff --name-only "$base"...HEAD -- python javascript go rust java other 2>/dev/null
    git diff --name-only HEAD -- python javascript go rust java other
    git ls-files --others --exclude-standard -- python javascript go rust java other
  } | sort -u
}

if [ $# -gt 0 ]; then files=("$@"); else mapfile -t files < <(collect_changed); fi
if [ ${#files[@]} -eq 0 ]; then echo "no changed solution files to lint"; exit 0; fi

passed=0 failed=0 skipped=0

check() { # <file> <command...>: run, record result
  local file="$1"; shift
  if out="$("$@" 2>&1)"; then
    echo "PASS  $file"; passed=$((passed + 1))
  else
    echo "FAIL  $file"; printf '%s\n' "$out" | sed 's/^/      /'; failed=$((failed + 1))
  fi
}

skip() { echo "SKIP  $1 ($2)"; skipped=$((skipped + 1)); }

go_vet() { # vet a solution together with the runner driver, as run_go.sh does
  local tmp; tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' RETURN
  cp "$SCRIPTS/run_go.go" "$tmp/driver.go"; cp "$1" "$tmp/solution.go"
  (cd "$tmp" && go vet driver.go solution.go)
}

for file in "${files[@]}"; do
  [ -z "$file" ] && continue
  file="${file#./}"
  case "$(basename "$file")" in solution.*) ;; *) continue ;; esac
  [ -f "$file" ] || { skip "$file" "not found / deleted"; continue; }
  if grep -q 'TODO(scaffold)' "$file"; then skip "$file" "unimplemented scaffold stub"; continue; fi

  case "${file%%/*}" in
    python)
      command -v uvx >/dev/null || { skip "$file" "uv not installed"; continue; }
      if [ $fix -eq 1 ]; then
        check "$file" bash -c 'uvx ruff check --config python/ruff.toml --fix "$0" && uvx ruff format --config python/ruff.toml "$0"' "$file"
      else
        check "$file" bash -c 'uvx ruff check --config python/ruff.toml "$0" && uvx ruff format --config python/ruff.toml --check "$0"' "$file"
      fi ;;
    javascript)
      command -v npx >/dev/null || { skip "$file" "node not installed"; continue; }
      if [ $fix -eq 1 ]; then mode=(--write); else mode=(); fi
      # run from javascript/ so biome picks up javascript/biome.json as its root config
      check "$file" bash -c 'cd javascript && npx --yes "@biomejs/biome@$0" check "$@"' \
        "$BIOME_VERSION" "${mode[@]}" "${file#javascript/}" ;;
    go)
      command -v go >/dev/null || { skip "$file" "go not installed"; continue; }
      if [ $fix -eq 1 ]; then gofmt -w "$file"; fi
      check "$file" bash -c 'test -z "$(gofmt -l "$0")" || { echo "needs gofmt: $0"; exit 1; }' "$file"
      [ $fix -eq 1 ] || check "$file (vet)" go_vet "$file" ;;
    *) skip "$file" "no linter configured for this language yet" ;;
  esac
done

echo
echo "passed=$passed failed=$failed skipped=$skipped"
[ "$failed" -eq 0 ]
