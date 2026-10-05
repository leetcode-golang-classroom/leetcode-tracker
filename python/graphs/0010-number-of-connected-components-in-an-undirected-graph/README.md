# [0010] Number of Connected Components in an Undirected Graph

- 難度：medium　主題：`graphs`
- 題目連結：https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

## 題目說明

給定 n 個節點（編號 0 到 n - 1）與一個陣列 edges，其中 edges[i] = [a, b] 表示節點 a 與 b 之間有一條無向邊。請回傳此圖中連通元件（connected components）的數量。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `n` | `int` |
| `edges` | `int[][]` |

回傳：`int`

## 限制

- 1 <= n <= 2000
- 1 <= edges.length <= 5000
- edges[i].length == 2
- 0 <= a, b < n
- a != b
- 不會有重複的邊

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"n": 5, "edges": [[0, 1], [1, 2], [3, 4]]}` | `2` |
| 2 | `{"n": 5, "edges": [[0, 1], [1, 2], [2, 3], [3, 4]]}` | `1` |
| 3 | `{"n": 4, "edges": []}` | `4` |
| 4 | `{"n": 1, "edges": []}` | `1` |

完整測資見 `testcases/0010-number-of-connected-components-in-an-undirected-graph.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
