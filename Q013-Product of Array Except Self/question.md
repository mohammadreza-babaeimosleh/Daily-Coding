# Insert Delete GetRandom O(1)

**Difficulty:** Medium  
**Topic Tags:** Array · Hash Table · Math · Design · Randomized

---

## Problem Description

Implement the `RandomizedSet` class:

- `RandomizedSet()` Initializes the `RandomizedSet` object.
- `bool insert(int val)` Inserts an item `val` into the set if not present. Returns `true` if the item was not present, `false` otherwise.
- `bool remove(int val)` Removes an item `val` from the set if present. Returns `true` if the item was present, `false` otherwise.
- `int getRandom()` Returns a random element from the current set of elements (it is guaranteed that at least one element exists when this method is called). Each element must have the **same probability** of being returned.

You must implement the functions of the class such that each function works in **average O(1) time complexity**.

---

## Example

```
Input:
["RandomizedSet", "insert", "remove", "insert", "getRandom", "remove", "insert", "getRandom"]
[[], [1], [2], [2], [], [1], [2], []]

Output:
[null, true, false, true, 2, true, false, 2]

Explanation:
RandomizedSet randomizedSet = new RandomizedSet();
randomizedSet.insert(1);     // Inserts 1. Returns true.
randomizedSet.remove(2);     // 2 not in set. Returns false.
randomizedSet.insert(2);     // Inserts 2. Returns true. Set = [1, 2].
randomizedSet.getRandom();   // Returns 1 or 2 randomly.
randomizedSet.remove(1);     // Removes 1. Returns true. Set = [2].
randomizedSet.insert(2);     // 2 already in set. Returns false.
randomizedSet.getRandom();   // Only element is 2. Returns 2.
```

---

## Constraints

- `-2³¹ <= val <= 2³¹ - 1`
- At most `2 * 10⁵` calls will be made to `insert`, `remove`, and `getRandom`.
- There will be at least one element in the data structure when `getRandom` is called.

---

## Solution

```python
# main.py
class RandomizedSet:
    def __init__(self): ...
    def insert(self, val: int) -> bool: ...
    def remove(self, val: int) -> bool: ...
    def getRandom(self) -> int: ...
```

---

## Complexity Analysis

| Operation | Time | Space |
|---|---|---|
| `insert` | O(1) avg | O(n) |
| `remove` | O(1) avg | O(n) |
| `getRandom` | O(1) | O(n) |

**Key insight:** combine a hash map (val → index) with a dynamic array. For O(1) removal, swap the target element with the last element before popping — then update the displaced element's index in the map.
