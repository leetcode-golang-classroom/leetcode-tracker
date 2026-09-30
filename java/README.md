# Java solutions

路徑格式：`<topic-slug>/<NNNN>-<problem-slug>/solution.java`（每題一個資料夾，內含 `README.md` 題目說明）

例如第一批 Arrays & Hashing 的 Two Sum：`arrays-hashing/0003-two-sum/solution.java`

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

## Lint 與格式

用 repo 根目錄的 `scripts/lint.sh`，不用額外安裝工具（需要 `java` 與 `uv`；google-java-format 的 jar 第一次執行時會自動下載到 `~/.cache/leetcode-tracker/`）。

```bash
scripts/lint.sh java/arrays-hashing/0003-two-sum/solution.java          # 只檢查，有問題就 FAIL
scripts/lint.sh --fix java/arrays-hashing/0003-two-sum/solution.java    # 自動補 import 並整理格式
scripts/lint.sh                                                         # 檢查相對 master 有變更的解答（含其他語言）
```

建議寫完解法後先跑一次 `--fix`，再跑 `scripts/verify.sh` 驗證。

檢查內容：

1. **缺少的 import**：`.github/scripts/java_imports.py` 會替常用 JDK 類別自動補 `import`，涵蓋 `java.util`（`List`、`Map`、`HashMap`、`Deque`、`PriorityQueue`、`Arrays`…）、`java.util.function` 與 `java.util.stream`。清單以外的類別要自己寫 import。
2. **格式**：google-java-format 的 `--aosp` 風格（4 格縮排），同時會排序 import、移除沒用到的 import。

注意：

- 還留有 `TODO(scaffold)` 標記的 stub 會被跳過。
- 沒有補 import 時編譯會失敗（`cannot find symbol`），`verify.sh` 也會 FAIL，所以 `--fix` 可以先救回來。
- PR 上的 `lint.yml` 會跑同一支腳本，lint 失敗不會改動 Project 的 Verified 欄位。
