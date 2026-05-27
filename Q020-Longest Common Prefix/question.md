# Longest Common Prefix

**Difficulty:** Easy  
**Topic Tags:** String · Trie

---

## Problem Description

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

---

## Examples

**Example 1:**
```
Input:  strs = ["flower","flow","flight"]
Output: "fl"
```

**Example 2:**
```
Input:  strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.
```

---

## Constraints

- `1 <= strs.length <= 200`
- `0 <= strs[i].length <= 200`
- `strs[i]` consists of only lowercase English letters (if non-empty)

---

## Solution

```python
# main.py
class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Horizontal scan (fold left) | O(S) | O(1) |
| Vertical scan (column by column) ✅ | O(S) | O(1) |
| Divide and conquer | O(S) | O(m · log n) |
| Binary search | O(S · log m) | O(1) |

Where `S` = total characters across all strings, `m` = length of shortest string, `n` = number of strings.
