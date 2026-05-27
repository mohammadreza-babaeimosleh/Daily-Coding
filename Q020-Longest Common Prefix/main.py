from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        min_length = len(min(strs, key=len))
        count = len(strs)
        if min_length == 0:
            return ''

        if count == 1:
            return strs[0]

        for i in range(min_length):
            letter = strs[0][i]
            for j in range(count):
                if strs[j][i] != letter:
                    return strs[0][:i]

        return strs[0][:i + 1]
