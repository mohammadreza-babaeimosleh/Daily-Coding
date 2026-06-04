class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0
        j = 0

        len_s = len(s)
        len_t = len(t)

        if len_s == 0:
            return True
        if len_t == 0:
            return False

        while j <= len_t - 1:

            if s[i] == t[j]:
                i += 1
                j += 1
            else:
                j += 1

            if i == len_s :
                return True

        
        return False
