# [0009] Spiral Matrix

- 難度：medium　主題：`math-geometry`
- 題目連結：https://leetcode.com/problems/spiral-matrix/

## 題目說明

給定一個 m x n 的矩陣 matrix，請依照順時針螺旋的順序，回傳矩陣中的所有元素。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `matrix` | `int[][]` |

回傳：`int[]`

## 限制

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}` | `[1, 2, 3, 6, 9, 8, 7, 4, 5]` |
| 2 | `{"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]}` | `[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]` |
| 3 | `{"matrix": [[1]]}` | `[1]` |
| 4 | `{"matrix": [[1, 2, 3]]}` | `[1, 2, 3]` |
| 5 | `{"matrix": [[1], [2], [3]]}` | `[1, 2, 3]` |

完整測資見 `testcases/0009-spiral-matrix.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
