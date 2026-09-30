# Scripts

## 管理腳本（皆用 `uv run`，依賴以 PEP 723 inline metadata 宣告）

| 腳本 | 用途 |
|---|---|
| `gh_project_lib.py` | 共用的 `gh` CLI / Projects v2 helper（issue、欄位、留言） |
| `bootstrap_labels.sh` | 建立 topic / difficulty / lang / type 標籤 |
| `add_problem.py` | 自動算出下一個 id/order，附加一筆新題目到 `problems.yaml` |
| `seed_problems.py` | 讀 `problems.yaml`，批次建立 parent + sub-issue 並設定 Project 欄位 |
| `scaffold.py` | 依 `problems.yaml` 產生 stub、每題 README 與共用測資（不覆蓋既有檔案） |
| `record_result.py` | 執行任一語言的 runner，把結果寫回 Project 欄位 + issue 留言 |

## 驗證 runner

每個 runner 吃 `<solution> <testcases.json>`，最後一行印 JSON：
`{"status": "passed"|"failed", "runtime_ms": <float>, "memory_kb": <float>, "details": "..."}`。

| 語言 | Runner | 解法檔案要求 |
|---|---|---|
| Python | `run_python.py`（`uv run`） | `def solve(...)`，以關鍵字參數呼叫，參數名對到 input 的 key |
| JavaScript | `run_javascript.mjs`（`node`） | CommonJS，`solve(input)` 收整個 input 物件（解法自行解構），`module.exports = { solve }`（`.ts` 需自行 transpile 成 `.js`） |
| Go | `run_go.go` + `run_go.sh` | `package main`，`func Solve(<原生型別參數>) <回傳值>`，不含 `func main`；依 input key 的順序對應參數順序 |
| Rust | `run_rust.rs` + `run_rust.sh` | `fn solve(nums: Vec<i64>, ...) -> ...`（driver 以 `FromValue`/`ToValue` trait 轉換，依參數順序對應） |
| Java | `Runner.java` + `run_java.sh` | 非 public 的 `class Solution`，`static <ret> solve(<原生型別參數>)`，以參數名對應 input 的 key |
| Other | — | 尚未提供；寫一個輸出格式相同的 runner 即可接上 `record_result.py` |

Go/Rust/Java 是靜態語言，無法像 Python/JS 動態載入任意函式，所以用固定簽名慣例：runner 負責計時、量記憶體、比對結果，解法照簽名寫即可。
- Go：`run_go.sh` 把 driver 與解法複製到同一個暫存目錄再 `go run`（`go run` 要求檔案在同一層）。
- Rust：`include!` 在編譯期把解法拼進 driver，以 `rustc` 直接編譯（沒有 Cargo/serde，JSON 手刻）。
- Java：`javac -parameters` 把 driver 與解法（複製並改名為 `Solution.java`）一起編譯，JSON 手刻。

Runtime / Memory 的量測方式各語言不同（Python `tracemalloc` 峰值、JS V8 heap delta、Go `TotalAlloc` delta、Rust `VmHWM`、Java heap 用量 delta），彼此**不是同單位可比**，但同一語言、同一題目跨次比較是有意義的。
