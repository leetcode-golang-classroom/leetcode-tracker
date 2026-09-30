# Rust solutions

路徑格式：`<topic-slug>/<NNNN>-<problem-slug>/solution.rs`（每題一個資料夾，內含 `README.md` 題目說明）

例如第一批 Arrays & Hashing 的 Two Sum：`arrays-hashing/0003-two-sum/solution.rs`

## 解法檔規範

- 定義 `fn solve(<參數...>) -> <回傳值>`，直接用題目原本的型別，例如：
  ```rust
  fn solve(nums: Vec<i64>, target: i64) -> Vec<i64> { ... }
  ```
- 型別對應：`int`→`i64`、`float`→`f64`、`bool`→`bool`、`string`→`String`、`T[]`→`Vec<T>`。參數須是 owned 型別（`Vec<i64>`，不是 `&[i64]`）。
- Rust 沒有 reflection，`.github/scripts/run_rust.rs` 以 `FromValue` / `ToValue` trait 做 JSON 與型別的轉換，並透過 `Solvable` trait 依參數個數（1～6 個）呼叫 `solve`。
- 和 Go 一樣依**參數順序**對應，不是依名稱：`testcases` 裡 `input` 物件的 key 順序要與 `solve` 的參數順序一致。
- 不要寫 `fn main`，也不需要自己引入 `Value`。
- 之後要支援 `ListNode`、`TreeNode` 等型別，只需在 driver 為它們補上 `FromValue` / `ToValue`。
