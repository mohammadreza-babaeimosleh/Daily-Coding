class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        length_needle = len(needle)
        length_haystack = len(haystack)
        if length_haystack == length_needle:
            if haystack == needle:
                return 0
            else:
                return -1
        for i in range(length_haystack - length_needle + 1):
            if haystack[i: i+length_needle] == needle:
                return i
        
        return -1
