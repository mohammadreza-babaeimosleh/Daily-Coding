# Two Sum II - Input Array Is Sorted

**Difficulty:** Medium  
**Topic Tags:** Array · Two Pointers · Binary Search

---

## Problem Description

Given a **1-indexed** array of integers `numbers` sorted in non-decreasing order, find two numbers such that they add up to a specific `target`. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return `[index1, index2]` — the 1-based indices of the two numbers. There is exactly one solution and you may not use the same element twice. Your solution must use only **constant extra space**.

---

## Examples

**Example 1:**
```
Input:  numbers = [2,7,11,15], target = 9
Output: [1,2]
Explanation: 2 + 7 = 9. index1 = 1, index2 = 2.
```

**Example 2:**
```
Input:  numbers = [2,3,4], target = 6
Output: [1,3]
Explanation: 2 + 4 = 6. index1 = 1, index2 = 3.
```

**Example 3:**
```
Input:  numbers = [-1,0], target = -1
Output: [1,2]
Explanation: -1 + 0 = -1. index1 = 1, index2 = 2.
```

---

## Constraints

- `2 <= numbers.length <= 3 * 10⁴`
- `-1000 <= numbers[i] <= 1000`
- `numbers` is sorted in non-decreasing order
- `-1000 <= target <= 1000`
- Exactly one solution exists

---

## Solution

```python
# main.py
class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Hash map | O(n) | O(n) |
| Binary search (per element) | O(n log n) | O(1) |
| Two pointers ✅ | O(n) | O(1) |

**Key insight:** With a sorted array, use two pointers from both ends. If the sum is too large shrink from the right; if too small grow from the left. Guaranteed to find the unique solution in a single pass.
