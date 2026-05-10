# Best Time to Buy and Sell Stock II

**Difficulty:** Medium  
**Topic Tags:** Array · Dynamic Programming · Greedy

---

## Problem Description

You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `ith` day.

On each day, you may decide to buy and/or sell the stock. You can only hold **at most one share** of the stock at any time. However, you can sell and buy the stock multiple times on the same day, ensuring you never hold more than one share.

Find and return the **maximum profit** you can achieve.

---

## Examples

**Example 1:**

```
Input:  prices = [7,1,5,3,6,4]
Output: 7
Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 4.
             Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 3.
             Total profit = 4 + 3 = 7.
```

**Example 2:**

```
Input:  prices = [1,2,3,4,5]
Output: 4
Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 4.
             Total profit = 4.
```

**Example 3:**

```
Input:  prices = [7,6,4,3,1]
Output: 0
Explanation: No profitable transaction exists. Max profit = 0.
```

---

## Constraints

- `1 <= prices.length <= 3 * 10⁴`
- `0 <= prices[i] <= 10⁴`

---

## Solution

```python
# main.py
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        ...
```

---

## Complexity Analysis

| Approach                                 | Time | Space |
| ---------------------------------------- | ---- | ----- |
| Peak-valley (find each local min/max) ✅ | O(n) | O(1)  |
| Greedy (sum all positive differences)    | O(n) | O(1)  |
| Dynamic programming                      | O(n) | O(1)  |

---

## Note

This is a follow-up to [LC 121 · Best Time to Buy and Sell Stock](../121-best-time-to-buy-and-sell-stock/question.md). The key difference is that unlimited transactions are allowed here. The greedy insight: summing every consecutive upward step `max(0, prices[i+1] - prices[i])` gives the same result as finding every peak-valley pair.
