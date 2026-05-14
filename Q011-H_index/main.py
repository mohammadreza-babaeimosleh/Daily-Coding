from typing import List

class Solution:
    def hIndex(self, citations: List[int]) -> int:
        citations.sort(reverse=True)

        h = 0
        for i, cite in enumerate(citations, start=1):
            if cite >= i:
                h = i
            else:
                break

        return h
