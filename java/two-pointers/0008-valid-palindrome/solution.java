class Solution {
    static boolean solve(String s) {
        // idea: 透過 lp, rp 逐步檢查是否有相對應的字元來驗證回文
        int lp = 0, rp = s.length() - 1;
        while (lp < rp) {
            if (!isAlphaNum(s.charAt(lp))) {
                lp++;
                continue;
            }
            if (!isAlphaNum(s.charAt(rp))) {
                rp--;
                continue;
            }

            if (Character.toUpperCase(s.charAt(lp)) != Character.toUpperCase(s.charAt(rp))) {
                return false;
            }
            lp++;
            rp--;
        }
        return true;
    }

    static boolean isAlphaNum(char ch) {
        return (ch >= 'a' && ch <= 'z') || (ch >= 'A' && ch <= 'Z') || (ch >= '0' && ch <= '9');
    }
}
