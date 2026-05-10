# Rotate Array

**Difficulty:** Medium  
**Topic Tags:** Array · Math · Two Pointers

---

## Problem Description

Given an integer array `nums`, rotate the array to the right by `k` steps, where `k` is non-negative.

---

## Examples

**Example 1:**
```
Input:  nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
  rotate 1 step  to the right: [7,1,2,3,4,5,6]
  rotate 2 steps to the right: [6,7,1,2,3,4,5]
  rotate 3 steps to the right: [5,6,7,1,2,3,4]
```

**Example 2:**
```
Input:  nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation:
  rotate 1 step  to the right: [99,-1,-100,3]
  rotate 2 steps to the right: [3,99,-1,-100]
```

---

## Constraints

- `1 <= nums.length <= 10⁵`
- `-2³¹ <= nums[i] <= 2³¹ - 1`
- `0 <= k <= 10⁵`

---

## Follow Up

- Try to come up with as many solutions as you can. There are at least **three** different ways to solve this problem.
- Could you do it **in-place** with `O(1)` extra space?

**Hint for O(1) space:** Reverse the whole array, then reverse the first `k` elements, then reverse the rest.

---

## Solution

```python
# main.py
class Solution:
    def rotate(self, nums: list[int], k: int) -> None:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Brute force (rotate one step at a time) | O(n·k) | O(1) |
| Extra array / slice reassignment ✅ | O(n) | O(n) |
| Cyclic replacements | O(n) | O(1) |
| Triple reverse | O(n) | O(1) |
