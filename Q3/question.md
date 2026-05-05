# Remove Duplicates from Sorted Array

**Difficulty:** Easy  
**Topic Tags:** Array · Two Pointers

---

## Problem Description

Given an integer array `nums` sorted in non-decreasing order, remove the duplicates [in-place](https://en.wikipedia.org/wiki/In-place_algorithm) such that each unique element appears only once. The relative order of the elements should be kept the same.

Consider the number of unique elements in `nums` to be `k`. After removing duplicates, return `k`.

The first `k` elements of `nums` should contain the unique numbers in sorted order. The remaining elements beyond index `k - 1` can be ignored.

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
Input:  nums = [1,1,2]
Output: 2, nums = [1,2,_]
Explanation: Your function should return k = 2, with the first two elements
             of nums being 1 and 2 respectively.
```

**Example 2:**
```
Input:  nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
Explanation: Your function should return k = 5, with the first five elements
             of nums being 0, 1, 2, 3, and 4 respectively.
```

---

## Constraints

- `1 <= nums.length <= 3 * 10⁴`
- `-100 <= nums[i] <= 100`
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
| Using a set | O(n log n) | O(n) |
| Two pointers ✅ | O(n) | O(1) |
