# [0003] Two Sum

- 難度：easy　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/two-sum/

## 題目說明

給定整數陣列 nums 與整數 target，回傳兩個相加等於 target 的元素的索引 [i, j]（i < j）。保證恰有一組解，且同一個元素不可重複使用。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `nums` | `int[]` |
| `target` | `int` |

回傳：`int[]`

## 限制

- 2 <= nums.length <= 10^4
- -10^9 <= nums[i], target <= 10^9

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"nums": [2, 7, 11, 15], "target": 9}` | `[0, 1]` |
| 2 | `{"nums": [3, 2, 4], "target": 6}` | `[1, 2]` |
| 3 | `{"nums": [3, 3], "target": 6}` | `[0, 1]` |

完整測資見 `testcases/0003-two-sum.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
