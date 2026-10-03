# [0008] Valid Palindrome

- 難度：easy　主題：`two-pointers`
- 題目連結：https://leetcode.com/problems/valid-palindrome/

## 題目說明

將字串中所有大寫字母轉為小寫，並移除所有非英數字元後，若正著讀與反著讀相同，則稱為回文。判斷給定字串 s 是否為回文。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `s` | `string` |

回傳：`bool`

## 限制

- 1 <= s.length <= 2 * 10^5
- s 只包含可列印的 ASCII 字元

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"s": "A man, a plan, a canal: Panama"}` | `true` |
| 2 | `{"s": "race a car"}` | `false` |
| 3 | `{"s": " "}` | `true` |

完整測資見 `testcases/0008-valid-palindrome.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
