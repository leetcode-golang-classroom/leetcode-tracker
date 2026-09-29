# Java solutions

檔名格式：`<topic-slug>/<NNNN>-<problem-slug>.java`

例如第一批 Arrays & Hashing 的 Two Sum：`arrays-hashing/0003-two-sum.java`

## 解法檔規範

- package-private 的 `class Solution`（不用 `public`，因為檔名不會跟 class 名一致）。
- 宣告 `static <回傳型別> solve(<參數...>)`，直接用題目原本的型別即可，例如：
  ```java
  class Solution {
      static int[] solve(int[] nums, int target) { ... }
  }
  ```
  支援 `int`/`long`/`double`/`boolean`/`String`/其對應的陣列（`int[]`、`String[]`…）、以及 `List<T>`（如 `List<Integer>`）。
- driver（`Runner.java`）用 reflection，依「參數名稱」把 `testcases.json` 的 `input` 物件對應到 `solve` 的參數（`run_java.sh` 編譯時會加 `-parameters` 保留參數名稱），**跟 Go 不同，這裡不用管 key 順序**，只要 `input` 的 key 名稱跟參數名稱一致就好。
