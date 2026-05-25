# Roman to Integer

**Difficulty:** Easy  
**Topic Tags:** Hash Table · Math · String

---

## Problem Description

Roman numerals are represented by seven different symbols:

| Symbol | Value |
|--------|-------|
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

Roman numerals are usually written largest to smallest from left to right. However, subtraction is used in six special cases:

- `I` before `V` (5) or `X` (10) → 4 or 9
- `X` before `L` (50) or `C` (100) → 40 or 90
- `C` before `D` (500) or `M` (1000) → 400 or 900

Given a roman numeral string `s`, convert it to an integer.

---

## Examples

**Example 1:**
```
Input:  s = "III"
Output: 3
```

**Example 2:**
```
Input:  s = "LVIII"
Output: 58
Explanation: L = 50, V = 5, III = 3.
```

**Example 3:**
```
Input:  s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90, IV = 4.
```

---

## Constraints

- `1 <= s.length <= 15`
- `s` contains only `'I'`, `'V'`, `'X'`, `'L'`, `'C'`, `'D'`, `'M'`
- `s` is a valid roman numeral in the range `[1, 3999]`

---

## Solution

```python
# main.py
class Solution:
    def romanToInt(self, s: str) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Scan left-to-right with lookahead | O(n) | O(1) |
| Scan right-to-left tracking previous ✅ | O(n) | O(1) |

**Key insight:** Scanning right-to-left, if the current symbol's value is less than the previously seen value, it must be a subtraction case — so subtract it instead of adding.
