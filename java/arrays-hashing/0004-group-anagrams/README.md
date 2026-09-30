# [0004] Group Anagrams

- 難度：medium　主題：`arrays-hashing`
- 題目連結：https://leetcode.com/problems/group-anagrams/

## 題目說明

給定字串陣列 strs，把彼此是 anagram 的字串分成同一組。
**本 repo 的輸出約定**（runner 以完全相等比較）：每組內的字串依字典序排序，各組再依「組內第一個字串」的字典序排序。

## 函式簽名

| 參數 | 型別 |
| --- | --- |
| `strs` | `string[]` |

回傳：`string[][]`

## 限制

- 1 <= strs.length <= 10^4
- 0 <= strs[i].length <= 100，只包含小寫英文字母

## 範例測資

| # | input | expected |
| --- | --- | --- |
| 1 | `{"strs": ["eat", "tea", "tan", "ate", "nat", "bat"]}` | `[["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]` |
| 2 | `{"strs": [""]}` | `[[""]]` |
| 3 | `{"strs": ["a"]}` | `[["a"]]` |

完整測資見 `testcases/0004-group-anagrams.json`（各語言 runner 共用，`input` 的 key 順序須與參數順序一致）。
