# Integer to Roman

**Difficulty:** Medium  
**Topic Tags:** Hash Table · Math · String

---

## Problem Description

Seven different symbols represent Roman numerals with the following values:

| Symbol | Value |
|--------|-------|
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

Roman numerals are formed by appending conversions of decimal place values from highest to lowest:

- If the value does **not** start with 4 or 9, select the maximal symbol that fits, append it, subtract its value, and repeat.
- If the value starts with **4 or 9**, use the subtractive form: `IV`, `IX`, `XL`, `XC`, `CD`, `CM`.
- Powers of 10 (`I`, `X`, `C`, `M`) can appear consecutively **at most 3 times**. `V`, `L`, `D` can never repeat.

Given an integer `num`, convert it to a Roman numeral.

---

## Examples

**Example 1:**
```
Input:  num = 3749
Output: "MMMDCCXLIX"
Explanation:
  3000 = MMM  (M × 3)
   700 = DCC  (D + C × 2)
    40 = XL   (10 less than 50)
     9 = IX   (1 less than 10)
```

**Example 2:**
```
Input:  num = 58
Output: "LVIII"
Explanation: 50 = L, 8 = VIII
```

**Example 3:**
```
Input:  num = 1994
Output: "MCMXCIV"
Explanation: M + CM + XC + IV
```

---

## Constraints

- `1 <= num <= 3999`

---

## Solution

```python
# main.py
class Solution:
    def intToRoman(self, num: int) -> str:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Greedy (value-symbol table) ✅ | O(1) | O(1) |

**Key insight:** Pre-build a table of all 13 value/symbol pairs including the 6 subtractive forms, then greedily peel off the largest fitting value repeatedly. Since the input is bounded to [1, 3999] and the table is fixed size, the algorithm runs in constant time.
