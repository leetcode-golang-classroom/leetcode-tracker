# [0001] Contains Duplicate

- 難度：easy　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/contains-duplicate/

## 題目說明

給定整數陣列 nums，若有任何數值出現至少兩次則回傳 true，否則回傳 false。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `nums` | `int[]` |

回傳：`bool`

## 限制

- 1 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"nums": [1, 2, 3, 1]}` | `true` |
| 2 | `{"nums": [1, 2, 3, 4]}` | `false` |
| 3 | `{"nums": [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]}` | `true` |

完整測資見 `testcases/0001-contains-duplicate.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
