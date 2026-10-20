# [0016] Best Time to Buy and Sell Stock

- 難度：easy　主題：`sliding-window`
- 題目連結：https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

## 題目說明

給定陣列 prices，其中 prices[i] 是某支股票第 i 天的價格。你只能選擇某一天買入、並在之後的另一天賣出，請回傳能獲得的最大利潤；若無法獲利則回傳 0。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `prices` | `int[]` |

回傳：`int`

## 限制

- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"prices": [7, 1, 5, 3, 6, 4]}` | `5` |
| 2 | `{"prices": [7, 6, 4, 3, 1]}` | `0` |
| 3 | `{"prices": [5]}` | `0` |
| 4 | `{"prices": [2, 4, 1]}` | `2` |

完整測資見 `testcases/0016-best-time-to-buy-and-sell-stock.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
