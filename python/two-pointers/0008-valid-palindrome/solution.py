def solve(s: str) -> bool:
    # ideas 透過左指標，右指標同時移動判斷是否為回文同時需要排除掉非字母與數字的項目
    lp, rp = 0, len(s) - 1
    while lp < rp:
        # 判斷 lp 是否為非字母數字
        if not (s[lp].isascii() and s[lp].isalnum()):
            lp += 1
            continue

        # 判斷 rp 是否為非字母數字
        if not (s[rp].isascii() and s[rp].isalnum()):
            rp -= 1
            continue

        # 判斷兩個字元轉大寫後是否相等
        if s[lp].upper() != s[rp].upper():
            return False

        lp += 1
        rp -= 1

    return True
