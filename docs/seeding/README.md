# 題目建立與排程（Seed）

題目的來源是 [`problems.yaml`](../../problems.yaml)。整體作題流程見 [WORKFLOW.md](../WORKFLOW.md)，這份文件專注在 issue 與 Project 的建立。

## 手動建立

1. 用 `add_problem.py` 幫每一題自動算好 `id`/`order` 並附加到 `problems.yaml`（同一批 7 題設定同一個 `week` 值）：
   ```bash
   uv run .github/scripts/add_problem.py \
     --title "Longest Consecutive Sequence" --topic arrays-hashing \
     --difficulty medium --week 2 \
     --source-url https://leetcode.com/problems/longest-consecutive-sequence/
   ```
   也可以照 `problems.yaml` 現有格式直接手動編輯。要產生起手檔的話，還要補 `signature`、`description`、`examples`，見 [WORKFLOW.md](../WORKFLOW.md)。
2. 先跑 `.github/scripts/bootstrap_labels.sh <owner>/<repo>` 建立所需標籤（第一次或有新 topic 時才需要）。
3. 設定環境變數（`GH_REPO`、`GH_PROJECT_OWNER`、`GH_PROJECT_NUMBER`、`LANGUAGES`）後跑：
   ```bash
   uv run .github/scripts/seed_problems.py problems.yaml
   ```
   會建立 parent issue、各語言 sub-issue，並自動加入 org Project 與設定欄位值。
   重複執行是安全的：已存在的 issue 會沿用，Verified 與 Handle-Status 只會在新建時設定，不會被覆蓋。

## 排程自動建立（`seed-weekly.yml`）

這個 workflow **不會自己想題目**，它只負責「時間到了就把 `problems.yaml` 裡已經寫好、輪到那一週的題目建出來」。所以要先把未來 1–2 週的題目提前寫進 `problems.yaml`，排程才不會空跑。

啟用前要設定：
- **Secret** `PROJECT_PAT`：一個有 `repo` + `project` scope 的 classic PAT（`gh auth refresh -s project` 產生的權限不夠用在 Actions 裡，要另外開一個 PAT 存進 repo secrets）。
- **Repo variables**：`WEEK1_START_DATE`（week 1 那個週一的日期，例如 `2026-09-28`）、`GH_PROJECT_OWNER`、`GH_PROJECT_NUMBER`、`LANGUAGES`。
- 預設排程時間是 `cron: "0 16 * * 0"`（UTC 週日 16:00 = 台灣時間週一 00:00），要改時間就調這行；也可以在 Actions 頁面手動按 `workflow_dispatch` 補跑。

運作方式：
1. 用 `WEEK1_START_DATE` 算出「今天是第幾週」，帶入 `seed_problems.py` 的 `MAX_WEEK`，只有 `week <= 目前週數` 的題目會被建立，已建立過的會跳過。
2. 接著執行 `scaffold.py`，為這些題目產生 stub、README 與測資，並開成 `scaffold/week-N` 的 PR（已存在的檔案不會被覆蓋）。stub 帶有 `TODO(scaffold)` 標記，CI 會跳過它們。
