# Candy

**Difficulty:** Hard  
**Topic Tags:** Array · Greedy · Two Pass

---

## Problem Description

There are `n` children standing in a line. Each child is assigned a rating value given in the integer array `ratings`.

You are giving candies to these children subjected to the following requirements:

- Each child must have **at least one candy**.
- Children with a **higher rating** than their neighbors get **more candies** than those neighbors.

Return the **minimum number of candies** you need to distribute.

---

## Examples

**Example 1:**
```
Input:  ratings = [1,0,2]
Output: 5
Explanation: Allocate 2, 1, 2 candies to children 1, 2, 3 respectively.
```

**Example 2:**
```
Input:  ratings = [1,2,2]
Output: 4
Explanation: Allocate 1, 2, 1 candies respectively.
             The third child gets 1 because equal ratings don't require more candies.
```

---

## Constraints

- `n == ratings.length`
- `1 <= n <= 2 * 10⁴`
- `0 <= ratings[i] <= 2 * 10⁴`

---

## Solution

```python
# main.py
class Solution:
    def candy(self, ratings: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach | Time | Space |
|---|---|---|
| Brute force (repeat until stable) | O(n²) | O(n) |
| Two-pass greedy (L→R then R←L) ✅ | O(n) | O(n) |
| Single-pass (slope counting) | O(n) | O(1) |

**Key insight:** A single left-to-right pass enforces the left-neighbour constraint. A second right-to-left pass enforces the right-neighbour constraint by taking the max of the two passes at each position.
