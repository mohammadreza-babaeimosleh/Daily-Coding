# Valid Palindrome

**Difficulty:** Easy  
**Topic Tags:** Two Pointers · String

---

## Problem Description

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

---

## Examples

**Example 1:**
```
Input:  s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

**Example 2:**
```
Input:  s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
```

**Example 3:**
```
Input:  s = " "
Output: true
Explanation: After removing non-alphanumeric characters the string is empty,
             and an empty string is a palindrome.
```

---

## Constraints

- `1 <= s.length <= 2 * 10⁵`
- `s` consists only of printable ASCII characters

---

## Solution

```python
# main.py
class Solution:
    def isPalindrome(self, s: str) -> bool:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Filter then reverse-compare | O(n) | O(n) |
| Two pointers (in-place skip) ✅ | O(n) | O(1) |

**Key insight:** Use two pointers converging inward, skipping non-alphanumeric characters on both sides. Compare lowercase versions of the valid characters. No extra string allocation needed.
