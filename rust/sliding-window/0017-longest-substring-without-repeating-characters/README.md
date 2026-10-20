# [0017] Longest Substring Without Repeating Characters

- 難度：medium　主題：`sliding-window`
- 題目連結：https://leetcode.com/problems/longest-substring-without-repeating-characters/

## 題目說明

給定字串 s，請找出不含重複字元的最長子字串，並回傳其長度。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `s` | `string` |

回傳：`int`

## 限制

- 0 <= s.length <= 5 * 10^4
- s 由英文字母、數字、符號與空白組成

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"s": "abcabcbb"}` | `3` |
| 2 | `{"s": "bbbbb"}` | `1` |
| 3 | `{"s": "pwwkew"}` | `3` |
| 4 | `{"s": ""}` | `0` |

完整測資見 `testcases/0017-longest-substring-without-repeating-characters.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
