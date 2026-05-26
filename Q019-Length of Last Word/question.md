# Length of Last Word

**Difficulty:** Easy  
**Topic Tags:** String

---

## Problem Description

Given a string `s` consisting of words and spaces, return the **length of the last word** in the string.

A word is a maximal substring consisting of non-space characters only.

---

## Examples

**Example 1:**
```
Input:  s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.
```

**Example 2:**
```
Input:  s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.
```

**Example 3:**
```
Input:  s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.
```

---

## Constraints

- `1 <= s.length <= 10⁴`
- `s` consists of only English letters and spaces `' '`
- There will be at least one word in `s`

---

## Solution

```python
# main.py
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Split and index last | O(n) | O(n) |
| Reverse scan (two pointers) ✅ | O(n) | O(1) |
