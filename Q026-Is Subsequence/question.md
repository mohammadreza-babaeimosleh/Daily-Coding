# Is Subsequence

**Difficulty:** Easy  
**Topic Tags:** Two Pointers · String · Dynamic Programming

---

## Problem Description

Given two strings `s` and `t`, return `true` if `s` is a subsequence of `t`, or `false` otherwise.

A subsequence is formed from the original string by deleting some (or no) characters without disturbing the relative order of the remaining characters.

---

## Examples

**Example 1:**
```
Input:  s = "abc", t = "ahbgdc"
Output: true
```

**Example 2:**
```
Input:  s = "axc", t = "ahbgdc"
Output: false
```

---

## Constraints

- `0 <= s.length <= 100`
- `0 <= t.length <= 10⁴`
- `s` and `t` consist only of lowercase English letters

---

## Follow Up

> Suppose there are lots of incoming `s` values (`s1, s2, ..., sk` where `k >= 10⁹`), and you want to check each one against the same `t`. How would you change your code?

**Hint:** Precompute for each position in `t` and each character, the next occurrence index. Then each query runs in O(|s|) with O(|t| · 26) preprocessing.

---

## Solution

```python
# main.py
class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Two pointers ✅ | O(n) | O(1) |
| Binary search (for follow-up) | O(\|s\| · log \|t\|) | O(\|t\| · 26) |
