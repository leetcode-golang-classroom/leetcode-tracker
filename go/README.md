# Go solutions

檔名格式：`<topic-slug>/<NNNN>-<problem-slug>.go`

例如第一批 Arrays & Hashing 的 Two Sum：`arrays-hashing/0003-two-sum.go`

## 解法檔規範

- `package main`，不要寫 `func main`（會跟 `.github/scripts/run_go.go` 的 driver 衝突）。
- 匯出 `func Solve(<參數...>) <回傳值>`，直接用題目原本的型別即可，例如：
  ```go
  func Solve(nums []int, target int) []int { ... }
  ```
- driver 用 reflection 依「`testcases.json` 裡 `input` 物件的 key 順序」對應「`Solve` 的參數順序」逐一解出型別並呼叫，**不是**依 key 名稱比對（Go 編譯後不會保留參數名稱）。所以寫 testcase 時 `input` 的 key 順序要跟 `Solve` 的參數順序一致。
- 只支援單一回傳值。
