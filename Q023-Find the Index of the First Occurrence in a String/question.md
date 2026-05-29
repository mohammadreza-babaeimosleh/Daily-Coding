# Find the Index of the First Occurrence in a String

**Difficulty:** Easy  
**Topic Tags:** Two Pointers · String · String Matching

---

## Problem Description

Given two strings `needle` and `haystack`, return the index of the **first occurrence** of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

---

## Examples

**Example 1:**
```
Input:  haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6. The first occurrence is at index 0.
```

**Example 2:**
```
Input:  haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode".
```

---

## Constraints

- `1 <= haystack.length, needle.length <= 10⁴`
- `haystack` and `needle` consist of only lowercase English letters

---

## Solution

```python
# main.py
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Sliding window (substring compare) ✅ | O(n · m) | O(1) |
| KMP algorithm | O(n + m) | O(m) |
| Rabin-Karp (rolling hash) | O(n + m) avg | O(1) |

Where `n = len(haystack)`, `m = len(needle)`.
