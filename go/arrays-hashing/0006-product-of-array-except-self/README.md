# [0006] Product of Array Except Self

- 難度：medium　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/product-of-array-except-self/

## 題目說明

給定整數陣列 nums，回傳陣列 answer，其中 answer[i] 等於 nums 中除了 nums[i] 以外所有元素的乘積。要求 O(n) 時間且不使用除法。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `nums` | `int[]` |

回傳：`int[]`

## 限制

- 2 <= nums.length <= 10^5
- -30 <= nums[i] <= 30，任何前綴／後綴乘積都能放進 32 位元整數

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"nums": [1, 2, 3, 4]}` | `[24, 12, 8, 6]` |
| 2 | `{"nums": [-1, 1, 0, -3, 3]}` | `[0, 0, 9, 0, 0]` |

完整測資見 `testcases/0006-product-of-array-except-self.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
