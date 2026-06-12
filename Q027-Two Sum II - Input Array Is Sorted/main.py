from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i, j = 0, len(numbers) - 1

        while i < j:
            total = numbers[i] + numbers[j]
            if total > target:
                j -= 1
            elif total < target:
                i += 1
            else:
                return [i + 1, j + 1]
