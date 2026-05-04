# Merge Sorted Array

**Difficulty:** Easy  
**Topic Tags:** Array · Two Pointers · Sorting

---

## Problem Description

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and two integers `m` and `n`, representing the number of elements in `nums1` and `nums2` respectively.

Merge `nums1` and `nums2` into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array `nums1`. To accommodate this, `nums1` has a length of `m + n`, where the first `m` elements denote the elements that should be merged, and the last `n` elements are set to `0` and should be ignored. `nums2` has a length of `n`.

---

## Examples

**Example 1:**
```
Input:  nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
Output: [1,2,2,3,5,6]
Explanation: The arrays we are merging are [1,2,3] and [2,5,6].
             The result of the merge is [1,2,2,3,5,6].
```

**Example 2:**
```
Input:  nums1 = [1], m = 1, nums2 = [], n = 0
Output: [1]
Explanation: The arrays we are merging are [1] and [].
             The result of the merge is [1].
```

**Example 3:**
```
Input:  nums1 = [0], m = 0, nums2 = [1], n = 1
Output: [1]
Explanation: The arrays we are merging are [] and [1].
             Note that because m = 0, there are no elements in nums1.
             The 0 is only there to ensure the merge result can fit in nums1.
```

---

## Constraints

- `nums1.length == m + n`
- `nums2.length == n`
- `0 <= m, n <= 200`
- `1 <= m + n <= 200`
- `-10⁹ <= nums1[i], nums2[j] <= 10⁹`

---

## Follow Up

> Can you come up with an algorithm that runs in **O(m + n)** time?

**Hint:** Try filling `nums1` from the **back** using two pointers — compare the largest unplaced elements of `nums1` and `nums2` and place the bigger one at the current tail position. This avoids any shifting and runs in a single pass.

---

## Solution

```python
# main.py
class Solution:
    def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Sort after concat | O((m+n) log(m+n)) | O(1) |
| Two pointers (front) | O(m+n) | O(m) |
| Two pointers (back) ✅ | O(m+n) | O(1) |
