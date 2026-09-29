#!/usr/bin/env bash
# 建立本專案需要的所有標籤（topic / difficulty / lang / type）。
# 用法：./bootstrap_labels.sh <owner>/<repo>
# 需要先 `gh auth login` 且對該 repo 有寫入權限。
set -euo pipefail

REPO="${1:?用法: bootstrap_labels.sh <owner>/<repo>}"

TOPICS=(
  arrays-hashing two-pointers sliding-window stack binary-search
  linked-list trees tries heap-priority-queue backtracking
  graphs advanced-graphs dp-1d dp-2d greedy intervals
  math-geometry bit-manipulation
)

create_label() {
  local name="$1" color="$2" description="$3"
  if gh label list --repo "$REPO" --search "$name" --json name -q '.[].name' | grep -qx "$name"; then
    echo "skip (exists): $name"
  else
    gh label create "$name" --repo "$REPO" --color "$color" --description "$description"
    echo "created: $name"
  fi
}

for topic in "${TOPICS[@]}"; do
  create_label "topic:$topic" "1D76DB" "Topic: $topic"
done

create_label "difficulty:easy"   "3BB143" "Easy"
create_label "difficulty:medium" "E8A33D" "Medium"
create_label "difficulty:hard"   "D93F3F" "Hard"

create_label "lang:python"                 "3776AB" "Python solution"
create_label "lang:javascript-typescript"  "F0DB4F" "JavaScript/TypeScript solution"
create_label "lang:go"                     "00ADD8" "Go solution"
create_label "lang:rust"                   "DEA584" "Rust solution"
create_label "lang:java"                   "B07219" "Java solution"
create_label "lang:other"                  "777777" "Other language solution"

create_label "type:problem"  "8250DF" "Parent issue for a problem"
create_label "type:solution" "0E8A16" "Sub-issue for a language solution"
