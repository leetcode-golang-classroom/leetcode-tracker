# [0005] Top K Frequent Elements

- 難度：medium　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/top-k-frequent-elements/

## 題目說明

給定整數陣列 nums 與整數 k，回傳出現頻率最高的 k 個元素。
**本 repo 的輸出約定**：回傳值由小到大排序（且測資保證答案唯一）。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `nums` | `int[]` |
| `k` | `int` |

回傳：`int[]`

## 限制

- 1 <= nums.length <= 10^5
- k 介於 1 與不同元素個數之間

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"nums": [1, 1, 1, 2, 2, 3], "k": 2}` | `[1, 2]` |
| 2 | `{"nums": [1], "k": 1}` | `[1]` |
| 3 | `{"nums": [4, 4, 4, 5, 5, 6, 6, 6, 6], "k": 1}` | `[6]` |

完整測資見 `testcases/0005-top-k-frequent-elements.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
