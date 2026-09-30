# 作題流程

從「這週有新題目」到「解法驗證通過、Project 看板更新」的完整步驟。專案結構與 Project 設定見 [README.md](../README.md)。

## 流程總覽

```
problems.yaml ──► seed（建 issue）──► scaffold（產生 stub/README/測資）──► 實作 ──► 本地驗證 ──► PR ──► CI 驗證並寫回看板
```

## 1. 題目進入清單

題目的來源是 `problems.yaml`。用 `add_problem.py` 新增，會自動算好 `id`/`order`：

```bash
uv run .github/scripts/add_problem.py \
  --title "Longest Consecutive Sequence" --topic arrays-hashing \
  --difficulty medium --week 2 \
  --source-url https://leetcode.com/problems/longest-consecutive-sequence/
```

要讓 scaffold 能產生函式簽名，還要在該題補上這幾個欄位（手動編輯 YAML）：

```yaml
  signature:
    params: [{name: nums, type: "int[]"}, {name: target, type: int}]
    returns: "int[]"
  description: |
    題目說明（用自己的話簡述，完整題目看 source_url）
  constraints: ["2 <= nums.length <= 10^4"]
  examples:
    - {input: {nums: [2, 7, 11, 15], target: 9}, expected: [0, 1]}
```

- 型別只支援 `int`、`float`、`bool`、`string`，以及它們加上 `[]`（可巢狀，如 `string[][]`）。
- `examples` 會成為 `testcases/<id>-<slug>.json`，各語言共用。`input` 的 key 順序會依 `params` 順序輸出，Go 是靠順序對應參數的。
- 題目文字不要整段貼上 LeetCode 或 NeetCode 的原文。neetcode.io 是前端渲染的頁面，也抓不到內容。

## 2. 建立 issue

每週 `seed-weekly.yml` 會自動建立輪到那週的題目，也可以手動跑 `seed_problems.py`（環境變數見 README）。每題會有一個 parent issue，以及每個語言一個 sub-issue。重複執行不會覆蓋已記錄的 Verified 與 Handle-Status。

## 3. 產生起手檔

```bash
uv run .github/scripts/scaffold.py problems.yaml --languages python,go
```

會為每題建立下列檔案，**已存在的檔案絕不覆蓋**：

| 檔案 | 用途 |
| --- | --- |
| `testcases/<id>-<slug>.json` | 共用測資（來自 `examples`） |
| `<lang>/<topic>/<id>-<slug>/solution.<ext>` | 帶好簽名的 stub |
| `<lang>/<topic>/<id>-<slug>/README.md` | 題目說明、函式簽名、範例測資表 |

每題在每個語言下是獨立資料夾。Go 的解法都是 `package main` 並匯出 `Solve`，同一資料夾放兩題會重複定義，所以全部語言統一用這個結構。runner 與 CI 由資料夾名稱 `<id>-<slug>` 反查 `testcases/`，只會處理檔名為 `solution.*` 的檔案。

`seed-weekly.yml` 會在建立 issue 後自動執行這一步（語言由 repo variable `LANGUAGES` 決定），並把結果開成 `scaffold/week-N` 的 PR。sub-issue 內文會附上 README 與解法檔的路徑。手動執行的指令如上。

stub 內有一行 `TODO(scaffold)` 標記。開始實作時把它刪掉；還留著標記的檔案，`scripts/verify.sh` 與 CI 都會跳過，不會寫入 Failed。

## 4. 實作

在對應語言的 stub 內實作。各語言的簽名慣例：

- Python：`solve(<參數>)`，以關鍵字參數呼叫，名稱要與測資 key 一致。
- JavaScript：CommonJS，`solve({ a, b })` 解構 input，`module.exports = { solve }`。
- Go：`package main`、`func Solve(...)`，不可有 `func main`，依參數順序對應。
- Java：package-private `class Solution`，`static <ret> solve(...)`，依參數名稱對應。
- Rust：`fn solve(<參數>) -> <回傳值>`，用 owned 型別（`Vec<i64>`、`String`…），依參數順序對應。

## 5. 本地驗證

```bash
scripts/verify.sh                          # 驗證相對 master 有變更的解答
scripts/verify.sh go/arrays-hashing/0003-two-sum/solution.go
```

使用與 CI 相同的 runner，但不會寫回 Project。缺少 toolchain 的語言會 SKIP；有任何 FAIL 則 exit 1，可以當 pre-push 檢查。

## 6. Lint 與格式

```bash
scripts/lint.sh          # 檢查相對 master 有變更的解答
scripts/lint.sh --fix    # 自動修正格式（Python、JS、Go、Java、Rust）
```

| 語言 | 工具 | 設定 |
| --- | --- | --- |
| Python | `ruff check` + `ruff format`（透過 `uvx`） | `python/ruff.toml` |
| JavaScript | `biome check`（固定版本，透過 `npx`） | `javascript/biome.json` |
| Go | `gofmt` + `go vet`（和 driver 一起 vet，和 `run_go.sh` 做法相同） | 無 |
| Rust | `rustfmt --check` + `clippy`（和 driver 一起分析，`-D warnings`，和 `run_rust.sh` 做法相同） | `rust/rustfmt.toml` |
| Java | 缺少 import 檢查（`.github/scripts/java_imports.py`）+ `google-java-format --aosp` | 無（jar 首次執行自動下載到 `~/.cache/leetcode-tracker/`） |

Java 的 `--fix` 會先替常用 JDK 類別（`java.util`、`java.util.function`、`java.util.stream`）補上缺少的 `import`，再由 google-java-format 排序、移除未使用的 import 並統一格式。google-java-format 本身不會補 import，所以補 import 由 `java_imports.py` 負責；清單以外的類別要自己加。

Rust 的 `--fix` 只跑 `rustfmt`，clippy 的建議要自己改（自動修正可能改變語意）。`other/` 目前沒有設定 linter，會顯示 SKIP。含 `TODO(scaffold)` 的 stub 也會跳過。PR 上的 `lint.yml` 跑同一支腳本，獨立於驗證 workflow，lint 失敗不會改動 Verified 欄位。

## 7. 送出 PR

```bash
git switch -c <id>-<slug>/<lang>   # 例如 0004-group-anagrams/go
git add <解法檔>
git commit -m "✨ (<slug>): <lang> solution"
git push -u origin HEAD
gh pr create --base master
```

PR 會觸發 `verify-solutions.yml`。它會跑 runner，把 Verified、Runtime、Memory 寫回 sub-issue 的 Project 欄位，並在 issue 留言。

## 8. 重新驗證

合併後想重跑某一份解答，到 Actions 頁手動觸發 `verify-solutions.yml`，填入 `solution_path`：

```bash
gh workflow run verify-solutions.yml -f solution_path=go/arrays-hashing/0003-two-sum/solution.go
```
