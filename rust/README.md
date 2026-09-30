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

## 驗證機制：用 trait 做型別轉換

測資是 JSON，解答卻用 `Vec<i64>`、`String` 這類原生型別。Go 靠 reflection 自動轉換，Rust 沒有 reflection，所以 `run_rust.rs` 改用 **trait** 在編譯期完成轉換：

| trait | 作用 | 已支援的型別 |
|---|---|---|
| `FromValue` | JSON `Value` → 解答的參數型別 | `i64`、`f64`、`bool`、`String`、`Vec<T>`、`Option<T>` |
| `ToValue` | 解答的回傳值 → JSON `Value`，用來和 `expected` 比對 | 同上 |
| `Solvable` | 讓 driver 不必知道 `solve` 有幾個參數，就能依序取出 `input` 的值並呼叫 | 1～6 個參數的函式 |

流程：driver 解析測資 → 依 `input` 的 key 順序取出各個值 → 用 `FromValue` 轉成 `solve` 宣告的參數型別 → 呼叫 `solve` → 用 `ToValue` 把回傳值轉回 JSON → 與 `expected` 比對。

`Vec<T>` 和 `Option<T>` 是遞迴組合的：只要 `T` 有實作，`Vec<Vec<String>>`、`Option<Vec<i64>>` 都能直接使用，不必另外寫。

### 擴充新型別

要支援新的型別（例如 `ListNode`、`TreeNode`），只要在 `run_rust.rs` 為它實作 `FromValue` 和 `ToValue`，既有程式不需要改。

### 什麼是 trait？

trait 是 Rust 用來描述「某個型別具備哪些能力」的機制，類似 Java 的 `interface` 或 Go 的 `interface`。trait 只宣告方法的簽名，由各個型別自行實作：

```rust
trait Describe {
    fn describe(&self) -> String;
}

impl Describe for i64 {
    fn describe(&self) -> String { format!("整數 {}", self) }
}

impl Describe for bool {
    fn describe(&self) -> String { format!("布林 {}", self) }
}
```

函式可以用 **trait bound** 要求參數必須具備某種能力，編譯器會在編譯期檢查：

```rust
fn show<T: Describe>(x: T) {
    println!("{}", x.describe());
}

show(42_i64); // OK
show(true);   // OK
show("abc");  // 編譯錯誤：&str 沒有實作 Describe
```

和 Go、Java 的 interface 比較：

- **事後實作：** 可以替既有型別（包含標準庫的 `i64`、`Vec<T>`）補上自己定義的 trait，不必修改原本的型別。本專案就是這樣替 `i64` 實作 `FromValue`。
- **靜態分派：** 泛型搭配 trait bound 會在編譯期為每個具體型別產生專用程式碼，沒有執行期的查表成本。
- **泛型實作：** `impl<T: FromValue> FromValue for Vec<T>` 表示「只要元素型別有實作，`Vec` 就自動有實作」，這是上面遞迴組合的來源。
- **回傳型別導向：** 像 `FromValue::from_value(&v)` 這種呼叫，會由編譯器從 `solve` 宣告的參數型別推導該用哪個實作，所以 driver 不需要知道型別字串。
