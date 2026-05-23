from typing import List

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # If total gas < total cost, no solution exists
        if sum(gas) < sum(cost):
            return -1

        curr_gas = 0
        start = 0

        for i in range(len(gas)):
            curr_gas += gas[i] - cost[i]
            # If tank goes negative, current start is invalid
            # Reset and try next station as new start
            if curr_gas < 0:
                curr_gas = 0
                start = i + 1

        return start
