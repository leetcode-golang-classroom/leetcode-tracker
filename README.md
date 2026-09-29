# leetcode-tracker

NeetCode 風格的多語言刷題追蹤 repo，搭配 GitHub Projects v2 看板使用。完整設計方案見對話中確認的計畫（Topic 分類、Project 欄位、Views、批次腳本）。

## 目錄結構

```
leetcode-tracker/
├── python/<topic-slug>/<NNNN>-<problem-slug>.py
├── javascript/<topic-slug>/<NNNN>-<problem-slug>.js (or .ts)
├── go/<topic-slug>/<NNNN>-<problem-slug>.go
├── rust/<topic-slug>/<NNNN>-<problem-slug>.rs
├── java/<topic-slug>/<NNNN>-<problem-slug>.java
├── other/<lang>/<topic-slug>/<NNNN>-<problem-slug>.*
├── problems.yaml                     # 題目主清單（source of truth，人工維護）
├── testcases/<NNNN>-<problem-slug>.json  # 每題的測試案例（input/expected），驗證腳本共用
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── problem.yml               # 手動補開單一題目（主幹 issue）
    │   └── solution.yml              # 手動補開單一語言解法（子 issue）
    ├── workflows/
    │   ├── add-to-project.yml        # 新 issue 自動加入 org Project
    │   ├── seed-weekly.yml           # 排程：每週自動把「已提前寫好、輪到的那週」題目建出來
    │   └── verify-solutions.yml      # push 到任一語言資料夾時，自動驗證並寫回 Project + 留言
    └── scripts/
        ├── gh_project_lib.py         # 共用的 gh CLI / Projects v2 helper（issue、欄位、留言）
        ├── bootstrap_labels.sh       # 建立 topic / difficulty / lang / type 標籤
        ├── add_problem.py            # 自動算出下一個 id/order，附加一筆新題目到 problems.yaml
        ├── seed_problems.py          # 讀 problems.yaml，批次建立 parent + sub-issue 並設定 Project 欄位
        ├── record_result.py          # 執行任一語言的 runner，把結果寫回 Project 欄位 + issue 留言
        │                              （上述 .py 都用 uv 跑，依賴以 PEP 723 inline script metadata 宣告）
        ├── run_python.py             # Python 驗證 runner（uv run）
        ├── run_javascript.mjs        # JavaScript/TypeScript 驗證 runner（node）
        ├── run_go.go + run_go.sh     # Go 驗證 runner：go run 需同目錄，run_go.sh 先把檔案暫存過去再跑
        ├── run_rust.rs + run_rust.sh # Rust 驗證 runner：rustc 直接編譯（無 Cargo/serde），無外部依賴
        └── Runner.java + run_java.sh # Java 驗證 runner：javac/java 編譯執行，JSON 手刻無外部依賴
```

## Topic 分類（沿用 NeetCode 架構）

`arrays-hashing`、`two-pointers`、`sliding-window`、`stack`、`binary-search`、
`linked-list`、`trees`、`tries`、`heap-priority-queue`、`backtracking`、
`graphs`、`advanced-graphs`、`dp-1d`、`dp-2d`、`greedy`、`intervals`、
`math-geometry`、`bit-manipulation`

## Issue 結構

- **Parent issue（題目）**：語言無關，標題格式 `[0001] Two Sum`，標籤 `topic:*`、`difficulty:*`、`type:problem`。
- **Sub-issue（解法）**：每語言一個，標題格式 `[0001][Python] Two Sum`，標籤 `lang:*`、`type:solution`，用 GitHub 原生 Sub-issues 掛在 parent 下。
- 語言選項（`lang:*` 標籤、Project 的 Language 欄位、`LANGUAGES` 環境變數共用同一組值）：`python`、`javascript-typescript`、`go`、`rust`、`java`、`other`。

## 使用流程

1. 用 `add_problem.py` 幫每一題自動算好 `id`/`order` 並附加到 `problems.yaml`（同一批 7 題設定同一個 `week` 值）：
   ```bash
   uv run .github/scripts/add_problem.py \
     --title "Longest Consecutive Sequence" --topic arrays-hashing \
     --difficulty medium --week 2 \
     --source-url https://leetcode.com/problems/longest-consecutive-sequence/
   ```
   （也可以照 `problems.yaml` 現有格式直接手動編輯，`add_problem.py` 只是省去自己算編號。）
2. 先跑 `.github/scripts/bootstrap_labels.sh <owner>/<repo>` 建立所需標籤（第一次或有新 topic 時才需要）。
3. 設定環境變數（`GH_REPO`、`GH_PROJECT_OWNER`、`GH_PROJECT_NUMBER`、`LANGUAGES`）後跑：
   ```
   uv run .github/scripts/seed_problems.py problems.yaml
   ```
   會建立 parent issue、各語言 sub-issue，並自動加入 org Project 與設定欄位值。
4. 到 org 的 Project（`https://github.com/orgs/<org>/projects`）依計畫設定 5 個 View：Topic Roadmap、語言 Kanban（每語言一個）、難度總覽、Hierarchy view、This Week。

## 排程自動建立（`seed-weekly.yml`）

這個 workflow **不會自己想題目**，它只負責「時間到了就把 `problems.yaml` 裡已經寫好、輪到那一週的題目建出來」。所以要先把未來 1–2 週的題目用 `add_problem.py` 提前寫進 `problems.yaml`，排程才不會空跑。

啟用前要設定：
- **Secret** `PROJECT_PAT`：一個有 `repo` + `project` scope 的 classic PAT（`gh auth refresh -s project` 產生的權限不夠用在 Actions 裡，要另外開一個 PAT 存進 repo secrets）。
- **Repo variables**：`WEEK1_START_DATE`（week 1 那個週一的日期，例如 `2026-09-28`）、`GH_PROJECT_OWNER`、`GH_PROJECT_NUMBER`、`LANGUAGES`。
- 預設排程時間是 `cron: "0 16 * * 0"`（UTC 週日 16:00 = 台灣時間週一 00:00），要改時間就調這行；也可以在 Actions 頁面手動按 `workflow_dispatch` 補跑。

運作方式：workflow 用 `WEEK1_START_DATE` 算出「今天是第幾週」，帶入 `seed_problems.py` 的 `MAX_WEEK` 環境變數 — 只有 `week <= 目前週數` 的題目會被建立，已建立過的靠既有的 idempotent 檢查跳過，所以就算補跑或重複觸發也不會重複建立 issue。

## 驗證與效能紀錄（Verification & Performance Tracking）

除了「有沒有解」之外，還要追蹤「解法對不對、跑多快、吃多少記憶體」。這靠三個 Project 欄位（只設在 sub-issue／解法 issue 上）＋兩支腳本：

| 欄位 | 類型 | 說明 |
|---|---|---|
| Verified | Single select | `Unverified` / `Passed` / `Failed`，最新一次驗證結果 |
| Runtime (ms) | Number | 最新一次驗證的執行時間 |
| Memory (KB) | Number | 最新一次驗證的峰值記憶體用量 |

因為 Project 欄位只會存「最新一次」的值，每次驗證同時也會在該 sub-issue 上留一則留言（timestamp、status、runtime、memory、details），留言串就是這題這個語言的歷史紀錄。

**測試案例格式**（`testcases/<NNNN>-<problem-slug>.json`）：

```json
[{"input": {"<參數名>": <值>, ...}, "expected": <預期輸出>}, ...]
```

放置規則：
- 檔名的 `<NNNN>-<problem-slug>` 要對應到 `problems.yaml` 裡該題的 `id` 與 `source_url` 慣例（例如 `0003-two-sum.json` 對應 `id: "0003"`），跟解法檔案的命名方式一致，這樣 `verify-solutions.yml` 才能用檔名反查到正確的測試案例。
- `input` 的 key 要跟語言 runner 的呼叫慣例對上（Python 是 `solve(**kwargs)` 的參數名，Go/Rust/Java 是丟進 `input` map 後自己取值），所以同一題不同語言共用同一份 testcase 檔案即可，不用每個語言各存一份。
- 沒有自動生成腳本，`expected` 必須手動抄自 LeetCode 題目頁面本身附的範例（通常 2–3 組），不要用自己的解法反推 expected，否則驗證會失去意義。

五種語言都已經有對應的 runner，且都用 `python/arrays-hashing/0003-two-sum.*` 這題實際跑過 pass/fail 兩種情況驗證過：

| 語言 | Runner | 呼叫方式 | 解法檔案要求 |
|---|---|---|---|
| Python | `run_python.py` | `uv run .github/scripts/run_python.py <sol.py> <tc.json>` | `def solve(**kwargs)`，參數名對到 input 的 key |
| JavaScript/TypeScript | `run_javascript.mjs` | `node .github/scripts/run_javascript.mjs <sol.js> <tc.json>` | CommonJS `module.exports.solve = function(input) {...}`（`.ts` 需自行 transpile 成 `.js`） |
| Go | `run_go.sh` | `.github/scripts/run_go.sh <sol.go> <tc.json>` | `package main`，`func Solve(input map[string]any) any`，不含 `func main` |
| Rust | `run_rust.sh` | `.github/scripts/run_rust.sh <sol.rs> <tc.json>` | `fn solve(input: &Value) -> Value`（`Value` 是 runner 提供的手刻 JSON 型別，見 `run_rust.rs`） |
| Java | `run_java.sh` | `.github/scripts/run_java.sh <sol.java> <tc.json>` | 非 public 的 `class Solution`，`static Object solve(Map<String,Object> input)` |
| Other | — | 尚未提供 | 之後要加時，寫一個輸出格式相同的 runner即可接上 `record_result.py` |

Go/Rust/Java 都是靜態語言，沒辦法像 Python/JS 一樣真的動態載入任意函式，所以用上面表格的**固定簽名慣例**：runner 負責計時、量記憶體、比對結果，你的解法只要照這個簽名寫。Go 用 `go run` 把 driver 和解法一起編譯（`run_go.sh` 會先把兩個檔案複製到同一個暫存目錄，因為 `go run` 要求所有檔案在同一層）；Rust 用 `include!` 在編譯期把解法檔案直接拼進 driver、以 `rustc` 直接編譯（沒有用 Cargo/serde，JSON 是手刻的最小 parser）；Java 用 `javac` 把 driver 跟解法（複製並改名為 `Solution.java`）一起編譯，JSON 也是手刻的。

輸出格式統一是最後一行印一個 JSON：`{"status": "passed"|"failed", "runtime_ms": <float>, "memory_kb": <float>, "details": "..."}`；Runtime/Memory 的量測方式每個語言略有不同（Python 用 `tracemalloc` 峰值、JS 用 V8 heap delta、Go 用 `TotalAlloc` delta、Rust 用 `/proc/self/status` 的 `VmHWM`、Java 用 heap 用量 delta），彼此之間**不是完全同單位可比**，但同一語言、同一題目跨次比較是有意義的。

**本機手動驗證一次**：

```bash
uv run .github/scripts/run_python.py python/arrays-hashing/0003-two-sum.py testcases/0003-two-sum.json
```

**自動化：`verify-solutions.yml`**

push 到 `main` 且改動了 `python/**`、`javascript/**`、`go/**`、`rust/**`、`java/**`、`other/**` 底下的檔案時，這個 workflow 會自動：找出這次 push 改到的解法檔、依所在資料夾判斷語言、找對應 `testcases/<id>-<slug>.json`、跑對應的 runner，最後呼叫 `record_result.py` 把結果寫回該題該語言 sub-issue 的 Verified / Runtime (ms) / Memory (KB) 欄位並留言記錄。也可以在 Actions 頁面用 `workflow_dispatch` 手動針對單一檔案重跑。**你平常只要 push 程式碼，不需要自己手動跑 `record_result.py`**——本機手動跑是給你想在 push 之前先確認解法對不對用的。

需要的環境設定跟 `seed-weekly.yml`共用同一組：`PROJECT_PAT` secret、`GH_PROJECT_OWNER`/`GH_PROJECT_NUMBER` repo variables。

## 尚待你確認/填入的設定

- 這個 repo 要 push 到哪個 GitHub repo（例如 `Egg-Village-Python-Workshop/leetcode-tracker`）。
- org Project 的編號（`GH_PROJECT_NUMBER`），需要先在 GitHub 上手動建立好這個 Project 並加上八個自訂欄位（Topic / Difficulty / Handle-Status / Language / Order / Verified / Runtime (ms) / Memory (KB)，Iteration 欄位另外在 Project UI 設定週期）。GitHub 內建的 `Status` 欄位名稱系統保留（無法改名/刪除），所以自訂的刷題狀態欄位要叫 `Handle-Status`，不要跟內建的 `Status` 搞混。
- 是否要在本機先安裝 `gh` CLI（並 `gh auth refresh -s project` 取得 project 權限）與 `uv`，才能跑這些腳本。
- 若要啟用 `seed-weekly.yml` 排程：`WEEK1_START_DATE` 定在哪一天、`PROJECT_PAT` secret 要不要現在就建。
