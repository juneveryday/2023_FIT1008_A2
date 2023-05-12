from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")

def binary_search(l: list[T], item: T, key = lambda x:x, is_insert : bool = False) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.

    :return: The index at which either:
        * This item is located, or
        * Where this item would be inserted to preserve the ordering.

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    return _binary_search_aux(l, item, 0, len(l), key, is_insert = is_insert)

def _binary_search_aux(l: list[T], item: T, lo: int, hi: int , key = lambda x:x, is_insert : bool = False) -> int:
    """
    Auxilliary method used by binary search.
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    if lo == hi:
        if is_insert == True:
            return lo
        else:
            raise KeyError("Item" ,item, "does not exist")
    mid = (hi + lo) // 2
    if key(l[mid]) > key(item):
        # Item would be before mid
        return _binary_search_aux(l, item, lo, mid, key, is_insert)
    elif key(l[mid]) < key(item):
        # Item would be after mid
        return _binary_search_aux(l, item, mid+1, hi, key, is_insert)
    elif key(l[mid]) == key(item):
        return mid
    raise ValueError(f"Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.")

"""
Changes made:
- added parameters - key (lambda function) and is_insert (boolean)
- raised KeyError
"""