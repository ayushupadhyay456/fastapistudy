"""
=============================================================================
DSA CHEAT SHEET & PYTHON IDIOMS / PITFALLS
=============================================================================
"""

from collections import Counter, defaultdict, deque
import bisect
import heapq

# =============================================================================
# 1. DICTIONARIES & COUNTING
# =============================================================================

# Problem: Manual membership checks ('if key not in d:') add unnecessary boilerplate.
# Solution: Use collections.defaultdict, dict.get(), or collections.Counter.

# Option A: defaultdict(type) auto-initializes missing keys
char_counts = defaultdict(int)  # Missing keys default to int() -> 0
for ch in "banana":
    char_counts[ch] += 1

# Option B: dict.get(key, fallback_default)
standard_dict = {}
for ch in "banana":
    standard_dict[ch] = standard_dict.get(ch, 0) + 1

# Option C: collections.Counter for fast one-liner counting
freq = Counter("banana")  # Counter({'a': 3, 'n': 2, 'b': 1})    


# =============================================================================
# 2. 2D MATRIX INITIALIZATION PITFALL
# =============================================================================

# PITFALL: Multiplying a list containing a list creates shallow copies.
# Every row points to the same memory reference!
bad_grid = [[0] * 3] * 3
bad_grid[0][0] = 1
# Result: [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  <-- All rows mutate!

# FIX: Use list comprehension to allocate separate list objects in memory.
rows, cols = 3, 3
correct_grid = [[0] * cols for _ in range(rows)]
correct_grid[0][0] = 1
# Result: [[1, 0, 0], [0, 0, 0], [0, 0, 0]]


# =============================================================================
# 3. LIST SLICING COPIES MEMORY (O(k) Time & Space)
# =============================================================================

arr = [1, 2, 3, 4, 5]
sub = arr[1:4]  # Allocates a new list in O(k) time and space.

# PITFALL IN RECURSION (e.g., Binary Search):
# Slicing the array (arr[:mid] / arr[mid+1:]) creates O(N) overhead per call,
# degrading an O(log N) algorithm to O(N).
# FIX: Pass boundary indices (left, right) instead of slicing the array.


# =============================================================================
# 4. QUEUES & BFS: list.pop(0) vs collections.deque
# =============================================================================

# PITFALL: Python lists are dynamic arrays.
#   - list.append(val) : O(1) amortized
#   - list.pop()       : O(1)
#   - list.pop(0)      : O(N) -> Shifts all remaining elements in memory!
#   - list.insert(0, x): O(N)

# FIX: Use collections.deque for O(1) queue operations in BFS.
queue = deque([1, 2, 3])
queue.append(4)  # O(1) push to back
first = queue.popleft()  # O(1) pop from front


# =============================================================================
# 5. HEAPS (PRIORITY QUEUES) via heapq
# =============================================================================

# Note: Python's heapq is MIN-HEAP ONLY.

# Min-Heap:
nums = [5, 1, 3]
heapq.heapify(nums)  # O(N) in-place transformation
smallest = heapq.heappop(nums)  # O(log N) -> Returns 1
heapq.heappush(nums, 2)  # O(log N)

# Max-Heap Workaround: Invert numbers by multiplying by -1.
nums = [5, 1, 3]
max_heap = [-x for x in nums]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap)  # Negate again to restore original value -> Returns 5


# =============================================================================
# 6. CUSTOM SORTING WITH key & lambda
# =============================================================================

# In-place sort: list.sort() | Returns new list: sorted(iterable)
# Tuples sort lexicographically (compares index 0, then index 1, etc.).

intervals = [[2, 6], [1, 3], [1, 2]]

# Example: Sort by start time ascending, then by end time descending
intervals.sort(key=lambda x: (x[0], -x[1]))
# Result: [[1, 3], [1, 2], [2, 6]]    


# =============================================================================
# 7. SCOPE IN RECURSION (nonlocal vs mutable containers)
# =============================================================================


def outer_function():
    max_val = float("-inf")
    result_list = []  # Lists are mutable, don't require nonlocal for mutations

    def dfs(current_val):
        nonlocal max_val  # Required to rebind an immutable variable from an enclosing scope
        max_val = max(max_val, current_val)
        result_list.append(current_val)  # .append() modifies in-place; no keyword needed

    dfs(10)
    return max_val, result_list


# =============================================================================
# 8. INFINITIES & EXTREME VALUES
# =============================================================================

# Avoid hardcoded magic numbers like 999999 or -100000.
pos_inf = float("inf")  # Greater than all numeric values
neg_inf = float("-inf")  # Smaller than all numeric values


# =============================================================================
# 9. BUILT-IN BINARY SEARCH: bisect
# =============================================================================

# Operates in O(log N) on sorted sequences.
sorted_arr = [10, 20, 20, 30, 40]

# bisect_left: Finds the first index where element could be inserted (>= x)
idx_left = bisect.bisect_left(sorted_arr, 20)  # Index 1

# bisect_right: Finds the rightmost insertion point (> x)
idx_right = bisect.bisect_right(sorted_arr, 20)  # Index 3

# insort_left / insort_right: Inserts the element in sorted order (O(N) shift)
bisect.insort_left(sorted_arr, 25)


# =============================================================================
# 10. STRING IMMUTABILITY & CONCATENATION
# =============================================================================

chars = ["a", "b", "c", "d"]

# PITFALL: Strings are immutable. In-place concatenation creates a new string
# object on every iteration, leading to O(N^2) runtime.
# bad_str = ""
# for ch in chars:
#     bad_str += ch

# FIX: Collect strings/characters in a list and join them in O(N).
good_str = "".join(chars)



"""
=============================================================================
DSA CHEAT SHEET (PART 2): ADVANCED PYTHON IDIOMS & LEETCODE PATTERNS
=============================================================================
"""

from functools import cache, cmp_to_key, lru_cache
import math
import sys

# =============================================================================
# 11. RECURSION DEPTH LIMIT & TLE IN DFS
# =============================================================================

# PITFALL: Python's default recursion limit is typically 1000.
# Deep DFS on large trees or graphs (e.g., N = 10^4 or 10^5) triggers RecursionError.
# FIX: Increase the limit before executing deep recursion.

sys.setrecursionlimit(200_000)


# =============================================================================
# 12. BUILT-IN MEMOIZATION: @cache AND @lru_cache (AUTOMATIC DP)
# =============================================================================

# Turns Top-Down DP into a simple recursive function without manual memo dicts.
# NOTE: Arguments must be HASHABLE (integers, strings, tuples; NOT lists or sets).


@cache  # Unlimited cache (Python 3.9+)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)


# For bounded memory, use lru_cache:
@lru_cache(maxsize=1024)
def knapsack(idx: int, capacity: int) -> int:
    # State transitions here...
    return 0


# =============================================================================
# 13. INTEGER DIVISION TRAPS (NEGATIVE NUMBERS)
# =============================================================================

# PITFALL: Python's `//` rounds toward NEGATIVE INFINITY (floor division),
# whereas C++/Java truncate toward zero.
# Example:
#   -3 // 2 == -2  (Python)
#   -3 /  2 == -1  (C++ / Java integer truncation)

# FIX: To truncate toward zero (like LeetCode problems often expect):
res_truncated = int(-3 / 2)  # -1

# Ceiling division (divide a by b, rounded up without floating-point math):
# Instead of math.ceil(a / b) which can lose precision for large ints:
a, b = 7, 3
ceil_div = (a + b - 1) // b  # 3


# =============================================================================
# 14. BITWISE OPERATIONS & TRICKS
# =============================================================================

x = 12  # Binary: 1100

# Clear the lowest set bit (O(number of set bits) counting):
# Used in Brian Kernighan's Algorithm:
count = 0
n = 12
while n:
    n &= n - 1  # Drops the lowest '1' bit
    count += 1  # count = 2

# Isolate the lowest set bit:
lowest_bit = x & -x  # Binary: 0100 (4)

# Check if a number is a power of two (and non-zero):
is_power_of_two = (x > 0) and (x & (x - 1) == 0)

# Fast set bit count:
bit_count = (12).bit_count()  # 2


# =============================================================================
# 15. CUSTOM COMPARATORS WITH cmp_to_key (e.g., "LARGEST NUMBER" PROBLEM)
# =============================================================================

# When elements cannot be sorted with a simple key lambda (depends on pairs).
# Return:
#   Negative value if a < b (a comes first)
#   Zero if a == b
#   Positive value if a > b (b comes first)


def compare_strings(a: str, b: str) -> int:
    # Example: Largest Number problem (compare concatenated results)
    if a + b > b + a:
        return -1  # a should come before b
    elif a + b < b + a:
        return 1  # b should come before a
    return 0


nums = ["3", "30", "34", "5", "9"]
sorted_nums = sorted(nums, key=cmp_to_key(compare_strings))
# Result: ['9', '5', '34', '3', '30']


# =============================================================================
# 16. UNPACKING & SWAPPING (O(1) WITHOUT TEMP VARIABLES)
# =============================================================================

# Swap variables safely in one cycle:
a, b = 5, 10
a, b = b, a

# Unpack head, tail, or rest of list:
head, *middle, tail = [1, 2, 3, 4, 5]
# head = 1, middle = [2, 3, 4], tail = 5


# =============================================================================
# 17. MATRIX TRANSPOSE & ROTATION WITH zip(*)
# =============================================================================

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

# Transpose matrix (rows become columns):
transposed = [list(col) for col in zip(*matrix)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# Rotate matrix 90 degrees clockwise:
# Rule: Reverse vertically, then transpose (or transpose and reverse each row):
rotated_90_cw = [list(row) for row in zip(*matrix[::-1])]
# [[7, 4, 1], [8, 5, 2], [9, 6, 3]]


# =============================================================================
# 18. SET OPERATIONS RUNTIME (INTERSECTION, UNION, DIFFERENCE)
# =============================================================================

s1 = {1, 2, 3, 4}
s2 = {3, 4, 5, 6}

# Set Lookups / Inserts / Deletes: O(1) average
# Pitfall: Set intersection `s1 & s2` is O(min(len(s1), len(s2))), NOT O(1).
intersection = s1 & s2  # {3, 4}
union = s1 | s2  # {1, 2, 3, 4, 5, 6}
difference = s1 - s2  # {1, 2}


# =============================================================================
# 19. gcd AND lcm (MATH MODULE)
# =============================================================================

# Avoid implementing Euclidean algorithm manually:
g = math.gcd(24, 36)  # 12
l = math.lcm(12, 18)  # 36
# Works with multiple arguments in modern Python:
multi_gcd = math.gcd(12, 24, 36, 48)  # 12


# =============================================================================
# 20. SHALLOW VS DEEP COPYING
# =============================================================================

import copy

original = [[1, 2], [3, 4]]

# Shallow copy: modifying sub-elements mutates the original!
shallow = original[:]  # or original.copy()
shallow[0][0] = 99
# original[0][0] is now 99!

# Deep copy: fully independent copy in memory:
independent = copy.deepcopy(original)
independent[0][0] = 42  # original remains unchanged