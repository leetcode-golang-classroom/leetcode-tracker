fn solve(s: String) -> bool {
    let chars: Vec<char> = s.chars().collect();

    // 使用 lp, rp two pointer 同時檢查對應的字元是否相同來判斷是否是回文
    // 宣告 lp, rp 具有所有權 來改動
    // rp 指向最後一個字元的下一格，實際檢查的是 chars[rp - 1]，避免空字串時 usize underflow
    let (mut lp, mut rp) = (0, chars.len());

    while lp < rp {
        // 確認 lp 指到的字元是否是 a-z, A-Z, 0-9
        if !chars[lp].is_ascii_alphanumeric() {
            lp += 1;
            continue;
        }

        // 確認 rp - 1 指到的字元是否是 a-z, A-Z, 0-9
        if !chars[rp - 1].is_ascii_alphanumeric() {
            rp -= 1;
            continue;
        }

        // 確認兩個數值字串是否不相同
        if !chars[lp].eq_ignore_ascii_case(&chars[rp - 1]) {
            return false;
        }

        lp += 1;
        rp -= 1;
    }
    true
}
