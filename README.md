# leetcode-tracker

NeetCode 風格的多語言刷題追蹤 repo，搭配 GitHub Projects v2 看板使用。

## 文件

| 文件 | 內容 |
|---|---|
| [作題流程](docs/WORKFLOW.md) | 從 issue 到驗證通過的完整步驟 |
| [專案結構](docs/project/README.md) | Topic 分類、Issue 結構、需要填入的設定 |
| [題目建立與排程](docs/seeding/README.md) | `problems.yaml`、seed、每週排程、scaffold |
| [驗證與效能紀錄](docs/verification/README.md) | 欄位、測資格式、本機驗證、CI |
| [Scripts 與 runner](.github/scripts/README.md) | 各腳本用途、各語言解法簽名、量測方式 |

## 目錄結構

```
leetcode-tracker/
├── python/<topic-slug>/<NNNN>-<problem-slug>/solution.py     # 每題一個資料夾，另含 README.md
├── javascript/<topic-slug>/<NNNN>-<problem-slug>/solution.js (or .ts)
├── go/<topic-slug>/<NNNN>-<problem-slug>/solution.go
├── rust/<topic-slug>/<NNNN>-<problem-slug>/solution.rs
├── java/<topic-slug>/<NNNN>-<problem-slug>/solution.java
├── other/<lang>/<topic-slug>/<NNNN>-<problem-slug>/solution.*
├── problems.yaml                     # 題目主清單（source of truth，人工維護）
├── testcases/<NNNN>-<problem-slug>.json  # 每題的測試案例（input/expected），驗證腳本共用
├── scripts/
│   ├── verify.sh                     # 本機驗證（同 CI runner，不寫回 Project）
│   └── lint.sh                       # 本機 lint / format
├── docs/                             # 作題流程與各主題文件
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── problem.yml               # 手動補開單一題目（主幹 issue）
    │   └── solution.yml              # 手動補開單一語言解法（子 issue）
    ├── workflows/
    │   ├── add-to-project.yml        # 新 issue 自動加入 org Project
    │   ├── seed-weekly.yml           # 排程：每週自動建出輪到的題目，並開 scaffold PR
    │   ├── verify-solutions.yml      # PR 到 master 時，自動驗證並寫回 Project + 留言
    │   └── lint.yml                  # PR 上跑 lint / format 檢查
    └── scripts/
        ├── gh_project_lib.py         # 共用的 gh CLI / Projects v2 helper（issue、欄位、留言）
        ├── bootstrap_labels.sh       # 建立 topic / difficulty / lang / type 標籤
        ├── add_problem.py            # 自動算出下一個 id/order，附加一筆新題目到 problems.yaml
        ├── seed_problems.py          # 讀 problems.yaml，批次建立 parent + sub-issue 並設定 Project 欄位
        ├── scaffold.py               # 產生 stub / 每題 README / 共用測資
        ├── record_result.py          # 執行任一語言的 runner，把結果寫回 Project 欄位 + issue 留言
        │                              （上述 .py 都用 uv 跑，依賴以 PEP 723 inline script metadata 宣告）
        ├── run_python.py             # Python 驗證 runner（uv run）
        ├── run_javascript.mjs        # JavaScript/TypeScript 驗證 runner（node）
        ├── run_go.go + run_go.sh     # Go 驗證 runner：go run 需同目錄，run_go.sh 先把檔案暫存過去再跑
        ├── run_rust.rs + run_rust.sh # Rust 驗證 runner：rustc 直接編譯（無 Cargo/serde），無外部依賴
        └── Runner.java + run_java.sh # Java 驗證 runner：javac/java 編譯執行，JSON 手刻無外部依賴
```
