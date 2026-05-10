# Jump Game

**Difficulty:** Medium  
**Topic Tags:** Array · Dynamic Programming · Greedy

---

## Problem Description

You are given an integer array `nums`. You are initially positioned at the **first index**, and each element in the array represents your **maximum jump length** at that position.

Return `true` if you can reach the last index, or `false` otherwise.

---

## Examples

**Example 1:**

```
Input:  nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
```

**Example 2:**

```
Input:  nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum
             jump length is 0, which makes it impossible to reach the last index.
```

---

## Constraints

- `1 <= nums.length <= 10⁴`
- `0 <= nums[i] <= 10⁵`

---

## Solution

```python
# main.py
class Solution:
    def canJump(self, nums: list[int]) -> bool:
        ...
```

---

## Complexity Analysis

| Approach                              | Time  | Space |
| ------------------------------------- | ----- | ----- |
| Backtracking (brute force)            | O(2ⁿ) | O(n)  |
| Dynamic programming (top-down)        | O(n²) | O(n)  |
| Dynamic programming (bottom-up)       | O(n²) | O(n)  |
| Greedy (track max reachable index) ✅ | O(n)  | O(1)  |
