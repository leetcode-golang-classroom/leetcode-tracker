# [0002] Valid Anagram

- 難度：easy　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/valid-anagram/

## 題目說明

給定兩個字串 s 與 t，若 t 是 s 的重新排列（每個字元出現次數相同）則回傳 true，否則回傳 false。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `s` | `string` |
| `t` | `string` |

回傳：`bool`

## 限制

- 1 <= s.length, t.length <= 5 * 10^4
- s 與 t 只包含小寫英文字母

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"s": "anagram", "t": "nagaram"}` | `true` |
| 2 | `{"s": "rat", "t": "car"}` | `false` |

完整測資見 `testcases/0002-valid-anagram.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
