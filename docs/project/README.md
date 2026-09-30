# 專案結構：Topic、Issue 與設定

## Topic 分類（沿用 NeetCode 架構）

`arrays-hashing`、`two-pointers`、`sliding-window`、`stack`、`binary-search`、
`linked-list`、`trees`、`tries`、`heap-priority-queue`、`backtracking`、
`graphs`、`advanced-graphs`、`dp-1d`、`dp-2d`、`greedy`、`intervals`、
`math-geometry`、`bit-manipulation`

## Issue 結構

- **Parent issue（題目）**：語言無關，標題格式 `[0001] Two Sum`，標籤 `topic:*`、`difficulty:*`、`type:problem`。
- **Sub-issue（解法）**：每語言一個，標題格式 `[0001][python] Two Sum`，標籤 `lang:*`、`type:solution`，用 GitHub 原生 Sub-issues 掛在 parent 下。內文附有 README、解法檔路徑與作題流程的連結。
- 語言選項（`lang:*` 標籤、Project 的 Language 欄位、`LANGUAGES` 環境變數共用同一組值）：`python`、`javascript-typescript`、`go`、`rust`、`java`、`other`。

## 需要你確認／填入的設定

- 這個 repo 要 push 到哪個 GitHub repo（例如 `Egg-Village-Python-Workshop/leetcode-tracker`）。
- org Project 的編號（`GH_PROJECT_NUMBER`），需要先在 GitHub 上手動建立好這個 Project 並加上八個自訂欄位（Topic / Difficulty / Handle-Status / Language / Order / Verified / Runtime (ms) / Memory (KB)，Iteration 欄位另外在 Project UI 設定週期）。GitHub 內建的 `Status` 欄位名稱系統保留（無法改名／刪除），所以自訂的刷題狀態欄位要叫 `Handle-Status`，不要跟內建的 `Status` 搞混。
- 本機需要 `gh` CLI（並 `gh auth refresh -s project` 取得 project 權限）與 `uv`，才能跑這些腳本。
- 啟用 `seed-weekly.yml` 排程：`WEEK1_START_DATE` 定在哪一天、`PROJECT_PAT` secret 要不要現在就建（見 [排程與 seed](../seeding/README.md)）。

Project 需依計畫設定 5 個 View：Topic Roadmap、語言 Kanban（每語言一個）、難度總覽、Hierarchy view、This Week。
