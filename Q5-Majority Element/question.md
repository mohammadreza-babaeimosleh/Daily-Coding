# Majority Element

**Difficulty:** Easy  
**Topic Tags:** Array · Hash Table · Divide and Conquer · Sorting · Counting

---

## Problem Description

Given an array `nums` of size `n`, return the majority element.

The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element **always exists** in the array.

---

## Examples

**Example 1:**
```
Input:  nums = [3,2,3]
Output: 3
```

**Example 2:**
```
Input:  nums = [2,2,1,1,1,2,2]
Output: 2
```

---

## Constraints

- `n == nums.length`
- `1 <= n <= 5 * 10⁴`
- `-10⁹ <= nums[i] <= 10⁹`
- The majority element always exists in the array.

---

## Follow Up

> Could you solve the problem in linear time and in `O(1)` space?

**Hint:** Look into the **Boyer-Moore Voting Algorithm** — maintain a candidate and a counter. When the counter hits 0, switch candidates. The majority element always survives.

---

## Solution

```python
# main.py
class Solution:
    def majorityElement(self, nums: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Sorting | O(n log n) | O(1) |
| Hash map ✅ | O(n) | O(n) |
| Boyer-Moore Voting | O(n) | O(1) |
