# Reverse Words in a String

**Difficulty:** Medium  
**Topic Tags:** Two Pointers · String

---

## Problem Description

Given an input string `s`, reverse the order of the **words**.

A word is defined as a sequence of non-space characters. Words in `s` will be separated by at least one space.

Return a string of the words in reverse order concatenated by a **single space**. The returned string should have no leading or trailing spaces, and multiple spaces between words must be reduced to one.

---

## Examples

**Example 1:**
```
Input:  s = "the sky is blue"
Output: "blue is sky the"
```

**Example 2:**
```
Input:  s = "  hello world  "
Output: "world hello"
Explanation: Strip leading/trailing spaces.
```

**Example 3:**
```
Input:  s = "a good   example"
Output: "example good a"
Explanation: Reduce multiple spaces to a single space.
```

---

## Constraints

- `1 <= s.length <= 10⁴`
- `s` contains English letters (upper and lower case), digits, and spaces `' '`
- There is at least one word in `s`

---

## Follow Up

> If the string data type is mutable in your language, can you solve it **in-place** with `O(1)` extra space?

---

## Solution

```python
# main.py
class Solution:
    def reverseWords(self, s: str) -> str:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| `split()[::-1]` (Pythonic) ✅ | O(n) | O(n) |
| Manual reverse scan (two pointers) ✅ | O(n) | O(n) |
| In-place (reverse all, reverse each word) | O(n) | O(1)¹ |

¹ Only possible in languages with mutable strings (e.g. C++, Java char arrays). Python strings are immutable.
