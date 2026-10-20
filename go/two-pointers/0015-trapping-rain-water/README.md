# [0015] Trapping Rain Water

- 難度：hard　主題：`two-pointers`
- 題目連結：https://leetcode.com/problems/trapping-rain-water/

## 題目說明

給定 n 個非負整數代表一張高度圖，每個柱子寬度為 1。請計算下雨後這張圖最多能接住多少單位的雨水。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `height` | `int[]` |

回傳：`int`

## 限制

- n == height.length
- 1 <= n <= 2 * 10^4
- 0 <= height[i] <= 10^5

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"height": [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]}` | `6` |
| 2 | `{"height": [4, 2, 0, 3, 2, 5]}` | `9` |
| 3 | `{"height": [1]}` | `0` |
| 4 | `{"height": [3, 2, 1]}` | `0` |

完整測資見 `testcases/0015-trapping-rain-water.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
