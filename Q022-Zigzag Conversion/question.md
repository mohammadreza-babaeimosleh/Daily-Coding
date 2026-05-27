# Zigzag Conversion

**Difficulty:** Medium  
**Topic Tags:** String

---

## Problem Description

The string `"PAYPALISHIRING"` is written in a zigzag pattern on a given number of rows like this:

```
P   A   H   N
A P L S I I G
Y   I   R
```

And then read line by line: `"PAHNAPLSIIGYIR"`

Write the code that will take a string and make this conversion given a number of rows.

---

## Examples

**Example 1:**
```
Input:  s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
```

**Example 2:**
```
Input:  s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:
  P     I    N
  A   L S  I G
  Y A   H R
  P     I
```

**Example 3:**
```
Input:  s = "A", numRows = 1
Output: "A"
```

---

## Constraints

- `1 <= s.length <= 1000`
- `s` consists of English letters (lower-case and upper-case), `','` and `'.'`
- `1 <= numRows <= 1000`

---

## Solution

```python
# main.py
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Simulate row-by-row with direction flag ✅ | O(n) | O(n) |
| Math (direct index computation) | O(n) | O(n) |

**Key insight:** Simulate the zigzag traversal by bouncing a row pointer between `0` and `numRows - 1`, flipping direction at the boundaries. Concatenate all row strings at the end.
