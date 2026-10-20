# [0011] Longest Consecutive Sequence

- 難度：medium　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/longest-consecutive-sequence/

## 題目說明

給定一個未排序的整數陣列 nums，回傳最長連續元素序列的長度。請設計時間複雜度為 O(n) 的演算法。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `nums` | `int[]` |

回傳：`int`

## 限制

- 0 <= nums.length <= 10^5
- -10^9 <= nums[i] <= 10^9

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"nums": [100, 4, 200, 1, 3, 2]}` | `4` |
| 2 | `{"nums": [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]}` | `9` |
| 3 | `{"nums": [1, 0, 1, 2]}` | `3` |
| 4 | `{"nums": []}` | `0` |
| 5 | `{"nums": [5]}` | `1` |

完整測資見 `testcases/0011-longest-consecutive-sequence.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
