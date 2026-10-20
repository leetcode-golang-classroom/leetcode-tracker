# [0012] Two Sum II - Input Array Is Sorted

- 難度：medium　主題：`two-pointers`
- 題目連結：https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

## 題目說明

給定一個已依非遞減順序排序、索引從 1 開始的整數陣列 numbers，找出兩個相加等於 target 的數字，並回傳它們的索引 [index1, index2]（1 <= index1 < index2）。保證恰有一組解，且不可重複使用同一個元素，解法只能使用常數額外空間。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `numbers` | `int[]` |
| `target` | `int` |

回傳：`int[]`

## 限制

- 2 <= numbers.length <= 3 * 10^4
- -1000 <= numbers[i] <= 1000
- numbers 以非遞減順序排序
- -1000 <= target <= 1000
- 保證恰有一組解

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"numbers": [2, 7, 11, 15], "target": 9}` | `[1, 2]` |
| 2 | `{"numbers": [2, 3, 4], "target": 6}` | `[1, 3]` |
| 3 | `{"numbers": [-1, 0], "target": -1}` | `[1, 2]` |
| 4 | `{"numbers": [1, 2, 3, 4, 4, 9, 56, 90], "target": 8}` | `[4, 5]` |

完整測資見 `testcases/0012-two-sum-ii-input-array-is-sorted.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
