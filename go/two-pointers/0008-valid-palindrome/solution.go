package main

func Solve(s string) bool {
	// ideas: 透過兩個 pointer 各自排除調非 alphaNumber 的字元
	// 然後轉換成大寫來避免來作字元比較
	lp, rp := 0, len(s)-1
	for lp < rp {
		// lp 不是字母或數字
		if !isAlphaNumber(s[lp]) {
			lp++
			continue
		}

		// rp 不是字母或是數字
		if !isAlphaNumber(s[rp]) {
			rp--
			continue
		}

		// 比較轉換成大寫的字元
		if toUpper(s[rp]) != toUpper(s[lp]) {
			return false
		}
		lp++
		rp--
	}
	return true
}

// isAlphaNumber: 判斷字元是 a-z, A-Z, 0-9
func isAlphaNumber(c byte) bool {
	return (c >= 'a' && c <= 'z') ||
		(c >= 'A' && c <= 'Z') ||
		(c >= '0' && c <= '9')
}

func toUpper(c byte) byte {
	alphaDist := byte('a') - byte('A')
	if c >= 'a' {
		return c - alphaDist
	}
	return c
}
