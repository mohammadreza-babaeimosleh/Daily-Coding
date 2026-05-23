# Gas Station

**Difficulty:** Medium  
**Topic Tags:** Array · Greedy

---

## Problem Description

There are `n` gas stations along a circular route, where the amount of gas at the `ith` station is `gas[i]`.

You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `ith` station to its next `(i + 1)th` station. You begin the journey with an **empty tank** at one of the gas stations.

Given two integer arrays `gas` and `cost`, return the **starting gas station's index** if you can travel around the circuit once in the clockwise direction, otherwise return `-1`. If a solution exists, it is **guaranteed to be unique**.

---

## Examples

**Example 1:**
```
Input:  gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3
Explanation:
  Start at station 3, fill up 4 units. Tank = 4
  Travel to station 4. Tank = 4 - 1 + 5 = 8
  Travel to station 0. Tank = 8 - 2 + 1 = 7
  Travel to station 1. Tank = 7 - 3 + 2 = 6
  Travel to station 2. Tank = 6 - 4 + 3 = 5
  Travel to station 3. Cost is 5. Tank = 0. Circuit complete.
```

**Example 2:**
```
Input:  gas = [2,3,4], cost = [3,4,3]
Output: -1
Explanation: No starting station allows completing the full circuit.
```

---

## Constraints

- `n == gas.length == cost.length`
- `1 <= n <= 10⁵`
- `0 <= gas[i], cost[i] <= 10⁴`
- The answer is guaranteed to be unique.

---

## Solution

```python
# main.py
class Solution:
    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Brute force (try every start) | O(n²) | O(1) |
| Greedy (single pass) ✅ | O(n) | O(1) |

**Key insight:** If the total gas is less than total cost, no solution exists. Otherwise, a solution is guaranteed. Track a running tank balance — whenever it goes negative, the current start and every station up to `i` are all invalid starts, so reset to `i + 1`.
