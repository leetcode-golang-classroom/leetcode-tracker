# 驗證與效能紀錄

除了「有沒有解」之外，還要追蹤「解法對不對、跑多快、吃多少記憶體」。這靠三個 Project 欄位（只設在 sub-issue 上）加上 runner 與 CI。

| 欄位 | 類型 | 說明 |
|---|---|---|
| Verified | Single select | `Unverified` / `Passed` / `Failed`，最新一次驗證結果 |
| Runtime (ms) | Number | 最新一次驗證的執行時間 |
| Memory (KB) | Number | 最新一次驗證的峰值記憶體用量 |

Project 欄位只會存「最新一次」的值，所以每次驗證同時會在該 sub-issue 留一則留言（timestamp、status、runtime、memory、details），留言串就是這題這個語言的歷史紀錄。

## 測試案例

路徑 `testcases/<NNNN>-<problem-slug>.json`，各語言共用同一份：

```json
[{"input": {"<參數名>": <值>, ...}, "expected": <預期輸出>}, ...]
```

- 檔名的 `<NNNN>-<problem-slug>` 要跟解法所在資料夾同名，CI 與 `verify.sh` 就是用資料夾名稱反查測資。
- `input` 的 key 要對上參數名（Python、Java）；Go 則是依 key 的順序對應參數順序。
- 測資由 `scaffold.py` 從 `problems.yaml` 的 `examples` 產生。`expected` 請抄自題目頁附的範例，不要用自己的解法反推，否則驗證就失去意義。
- runner 以完全相等比較，答案順序不唯一的題目要在題目說明裡約定排序（見該題 README）。

Runner 的呼叫慣例與各語言的解法簽名見 [`.github/scripts/README.md`](../../.github/scripts/README.md)。

## 本機驗證

```bash
scripts/verify.sh                                              # 驗證相對 master 有變更的解答
scripts/verify.sh go/arrays-hashing/0003-two-sum/solution.go   # 指定檔案
scripts/lint.sh [--fix]                                        # lint / format（Python、JS、Go）
```

`verify.sh` 使用與 CI 相同的 runner，但不寫回 Project；缺少 toolchain、沒有測資、`other/`、以及仍含 `TODO(scaffold)` 的 stub 都會 SKIP，有 FAIL 則 exit 1。

單跑一個 runner：

```bash
uv run .github/scripts/run_python.py python/arrays-hashing/0003-two-sum/solution.py testcases/0003-two-sum.json
```

## CI

- **`verify-solutions.yml`**：PR 到 `master` 且改動了 `python/**`、`javascript/**`、`go/**`、`rust/**`、`java/**`、`other/**` 時，找出變更的 `solution.*`、依資料夾名稱找測資、跑對應 runner，再呼叫 `record_result.py` 寫回 Verified / Runtime / Memory 並留言。也可在 Actions 頁用 `workflow_dispatch` 指定 `solution_path` 重跑單一檔案。平常只要開 PR，不需要手動跑 `record_result.py`。
- **`lint.yml`**：PR 上跑 `scripts/lint.sh`，獨立於驗證，lint 失敗不會改動 Verified。

所需設定與 `seed-weekly.yml` 共用：`PROJECT_PAT` secret、`GH_PROJECT_OWNER` / `GH_PROJECT_NUMBER` repo variables。
