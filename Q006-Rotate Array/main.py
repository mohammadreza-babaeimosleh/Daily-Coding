from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:

        length = len(nums)
        k = k % length

        anchor = length - k
        first = nums[anchor:]
        second = nums[:anchor]

        nums[:k] = first
        nums[k:] = second
