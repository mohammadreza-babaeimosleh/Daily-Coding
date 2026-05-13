# H-Index

**Difficulty:** Medium  
**Topic Tags:** Array · Sorting · Counting Sort

---

## Problem Description

Given an array of integers `citations` where `citations[i]` is the number of citations a researcher received for their `ith` paper, return the researcher's **h-index**.

The h-index is defined as the maximum value of `h` such that the given researcher has published at least `h` papers that have each been cited **at least `h` times**.

---

## Examples

**Example 1:**

```
Input:  citations = [3,0,6,1,5]
Output: 3
Explanation: The researcher has 5 papers with 3, 0, 6, 1, 5 citations.
             There are 3 papers with at least 3 citations each, and the
             remaining two have no more than 3 citations — so h-index = 3.
```

**Example 2:**

```
Input:  citations = [1,3,1]
Output: 1
```

---

## Constraints

- `n == citations.length`
- `1 <= n <= 5000`
- `0 <= citations[i] <= 1000`

---

## Solution

```python
# main.py
class Solution:
    def hIndex(self, citations: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach                         | Time       | Space |
| -------------------------------- | ---------- | ----- |
| Sort descending + linear scan ✅ | O(n log n) | O(1)  |
| Counting sort (bucket)           | O(n)       | O(n)  |
