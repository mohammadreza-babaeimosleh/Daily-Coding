# Trapping Rain Water

**Difficulty:** Hard  
**Topic Tags:** Array · Two Pointers · Dynamic Programming · Stack · Monotonic Stack

---

## Problem Description

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

---

## Examples

**Example 1:**
```
Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The elevation map traps 6 units of rain water.
```

**Example 2:**
```
Input:  height = [4,2,0,3,2,5]
Output: 9
```

---

## Constraints

- `n == height.length`
- `1 <= n <= 2 * 10⁴`
- `0 <= height[i] <= 10⁵`

---

## Solution

```python
# main.py
class Solution:
    def trap(self, height: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Brute force (for each bar scan left/right max) | O(n²) | O(1) |
| Precompute left/right max arrays | O(n) | O(n) |
| Monotonic stack | O(n) | O(n) |
| Two pointers ✅ | O(n) | O(1) |

**Key insight:** Use two pointers converging inward. The side with the smaller height is the limiting factor — water at that position is determined entirely by the max seen so far on that side, regardless of what's on the other side.
