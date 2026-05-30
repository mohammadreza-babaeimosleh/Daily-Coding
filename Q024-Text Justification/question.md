# Text Justification

**Difficulty:** Hard  
**Topic Tags:** Array · String · Simulation

---

## Problem Description

Given an array of strings `words` and a width `maxWidth`, format the text such that each line has **exactly `maxWidth` characters** and is fully (left and right) justified.

Pack words greedily — as many as possible per line. Distribute extra spaces as evenly as possible between words. If spaces do not divide evenly, the **left gaps get more spaces** than the right ones.

The **last line** must be **left-justified** with no extra spaces between words (only trailing spaces to pad to `maxWidth`). A line containing a **single word** is also left-justified.

---

## Examples

**Example 1:**
```
Input:  words = ["This","is","an","example","of","text","justification."], maxWidth = 16
Output:
  "This    is    an"
  "example  of text"
  "justification.  "
```

**Example 2:**
```
Input:  words = ["What","must","be","acknowledgment","shall","be"], maxWidth = 16
Output:
  "What   must   be"
  "acknowledgment  "
  "shall be        "
```

**Example 3:**
```
Input:  words = ["Science","is","what","we","understand","well","enough","to",
                 "explain","to","a","computer.","Art","is","everything","else","we","do"],
        maxWidth = 20
Output:
  "Science  is  what we"
  "understand      well"
  "enough to explain to"
  "a  computer.  Art is"
  "everything  else  we"
  "do                  "
```

---

## Constraints

- `1 <= words.length <= 300`
- `1 <= words[i].length <= 20`
- `words[i]` consists of only English letters and symbols
- `1 <= maxWidth <= 100`
- `words[i].length <= maxWidth`

---

## Solution

```python
# main.py
class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Greedy line packing + space distribution ✅ | O(n · maxWidth) | O(n · maxWidth) |

**Key insight:** Use two passes per line — first pack words greedily, then distribute spaces. For non-last lines with multiple words, use `divmod(total_spaces, gaps)` to get even spacing and track which left gaps get the extra space.
