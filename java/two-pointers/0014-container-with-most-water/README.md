# [0014] Container With Most Water

- 難度：medium　主題：`two-pointers`
- 題目連結：https://leetcode.com/problems/container-with-most-water/

## 題目說明

給定長度為 n 的整數陣列 height，第 i 條垂直線的兩個端點為 (i, 0) 與 (i, height[i])。請找出兩條線，使它們與 x 軸共同構成的容器能裝最多的水，並回傳最大水量。容器不可傾斜。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `height` | `int[]` |

回傳：`int`

## 限制

- n == height.length
- 2 <= n <= 10^5
- 0 <= height[i] <= 10^4

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"height": [1, 8, 6, 2, 5, 4, 8, 3, 7]}` | `49` |
| 2 | `{"height": [1, 1]}` | `1` |
| 3 | `{"height": [0, 0]}` | `0` |
| 4 | `{"height": [2, 3, 4, 5, 18, 17, 6]}` | `17` |

完整測資見 `testcases/0014-container-with-most-water.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
