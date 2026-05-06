from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count_dict = {}
        for i in nums:
            count = count_dict.get(i, None)
            if not count:
                count_dict[i] = 1
            else: 
                count_dict[i] += 1

        max_count = max(count_dict, key=count_dict.get)

        return max_count
