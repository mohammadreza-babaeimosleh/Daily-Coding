# Remove Duplicates from Sorted Array II

**Difficulty:** Medium  
**Topic Tags:** Array · Two Pointers

---

## Problem Description

Given an integer array `nums` sorted in non-decreasing order, remove some duplicates in-place such that each unique element appears **at most twice**. The relative order of the elements should be kept the same.

If there are `k` elements after removing the duplicates, then the first `k` elements of `nums` should hold the final result. It does not matter what you leave beyond the first `k` elements.

Return `k` after placing the final result in the first `k` slots of `nums`.

Do not allocate extra space for another array. You must do this by modifying the input array **in-place** with `O(1)` extra memory.

---

## Custom Judge

```
int[] nums = [...];         // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
```

If all assertions pass, then your solution will be accepted.

---

## Examples

**Example 1:**
```
Input:  nums = [1,1,1,2,2,3]
Output: 5, nums = [1,1,2,2,3,_]
Explanation: Your function should return k = 5, with the first five elements
             of nums being 1, 1, 2, 2 and 3 respectively.
```

**Example 2:**
```
Input:  nums = [0,0,1,1,1,1,2,3,3]
Output: 7, nums = [0,0,1,1,2,3,3,_,_]
Explanation: Your function should return k = 7, with the first seven elements
             of nums being 0, 0, 1, 1, 2, 3 and 3 respectively.
```

---

## Constraints

- `1 <= nums.length <= 3 * 10⁴`
- `-10⁴ <= nums[i] <= 10⁴`
- `nums` is sorted in non-decreasing order.

---

## Solution

```python
# main.py
class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Using a counter dict | O(n) | O(n) |
| Two pointers ✅ | O(n) | O(1) |

---

## Note

This is a generalisation of [LC 26 · Remove Duplicates from Sorted Array](../26-remove-duplicates-from-sorted-array/question.md). The key insight is comparing `nums[i]` against `nums[k-2]` instead of `nums[k-1]` — if they differ, the current element can safely be placed (it cannot be a third occurrence).
