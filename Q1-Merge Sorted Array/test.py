"""
test.py — Benchmark & correctness tester for LeetCode 88 · Merge Sorted Array
Runs 100 test cases against main.py's Solution.merge() and reports:
  - Pass rate
  - Average / min / max / std-dev execution time
  - Any failing cases (up to 5 shown)
"""

import time
import copy
import random
import statistics
import importlib
import sys

# ── Import solution ────────────────────────────────────────────────────────────
try:
    solution_module = importlib.import_module("main")
    Solution = solution_module.Solution
except ModuleNotFoundError:
    print("❌  Could not import 'main.py'. Make sure it exists in the same directory.")
    sys.exit(1)
except AttributeError:
    print("❌  'main.py' must define a class named 'Solution'.")
    sys.exit(1)


# ── Reference (brute-force) solution ─────────────────────────────────────────
def reference_merge(nums1: list, m: int, nums2: list, n: int) -> list:
    """Returns the expected merged list without modifying inputs."""
    result = sorted(nums1[:m] + nums2[:n])
    return result


# ── Test-case generator ────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list[dict]:
    """
    Generates `count` randomised test cases plus the 3 canonical LeetCode examples.
    Each case is a dict with keys: nums1, m, nums2, n, expected.
    """
    fixed = [
        {"nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [2, 5, 6],  "n": 3},
        {"nums1": [1],                 "m": 1, "nums2": [],          "n": 0},
        {"nums1": [0],                 "m": 0, "nums2": [1],         "n": 1},
    ]

    cases = []
    for f in fixed:
        f["expected"] = reference_merge(f["nums1"], f["m"], f["nums2"], f["n"])
        cases.append(f)

    rng = random.Random(42)
    while len(cases) < count:
        m = rng.randint(0, 100)
        n = rng.randint(0, 100)
        if m + n == 0:
            n = 1                             # constraint: 1 <= m+n <= 200

        a = sorted(rng.randint(-10**9, 10**9) for _ in range(m))
        b = sorted(rng.randint(-10**9, 10**9) for _ in range(n))
        nums1 = a + [0] * n                   # pad with n zeros

        cases.append({
            "nums1":    nums1,
            "m":        m,
            "nums2":    b,
            "n":        n,
            "expected": reference_merge(nums1, m, b, n),
        })

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  LeetCode 88 · Merge Sorted Array — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()

    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        # Deep-copy so the solution gets a fresh nums1 every time
        nums1 = copy.deepcopy(case["nums1"])
        nums2 = copy.deepcopy(case["nums2"])
        m, n  = case["m"], case["n"]

        start = time.perf_counter_ns()
        try:
            sol.merge(nums1, m, nums2, n)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({
                "index":    idx + 1,
                "m":        m, "n": n,
                "nums1_in": case["nums1"],
                "nums2_in": case["nums2"],
                "got":      f"EXCEPTION: {exc}",
                "expected": case["expected"],
            })
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)
        actual = nums1[:m + n]

        if actual == case["expected"]:
            passed += 1
        else:
            failures.append({
                "index":    idx + 1,
                "m":        m, "n": n,
                "nums1_in": case["nums1"],
                "nums2_in": case["nums2"],
                "got":      actual,
                "expected": case["expected"],
            })

    # ── Statistics ────────────────────────────────────────────────────────────
    avg_us  = statistics.mean(times_ns)   / 1_000
    min_us  = min(times_ns)               / 1_000
    max_us  = max(times_ns)               / 1_000
    std_us  = statistics.stdev(times_ns)  / 1_000 if len(times_ns) > 1 else 0.0
    med_us  = statistics.median(times_ns) / 1_000

    # Percentiles
    sorted_ns = sorted(times_ns)
    p90_us = sorted_ns[int(0.90 * len(sorted_ns))] / 1_000
    p99_us = sorted_ns[int(0.99 * len(sorted_ns))] / 1_000

    fail_count = len(failures)
    pass_rate  = passed / num_tests * 100

    print(f"\n📊  Results ({num_tests} tests)")
    print(f"  ✅  Passed  : {passed}/{num_tests}  ({pass_rate:.1f}%)")
    print(f"  ❌  Failed  : {fail_count}")

    print(f"\n⏱️   Execution Time (per call)")
    print(f"  Average : {avg_us:>10.3f} µs")
    print(f"  Median  : {med_us:>10.3f} µs")
    print(f"  Std Dev : {std_us:>10.3f} µs")
    print(f"  Min     : {min_us:>10.3f} µs")
    print(f"  Max     : {max_us:>10.3f} µs")
    print(f"  p90     : {p90_us:>10.3f} µs")
    print(f"  p99     : {p99_us:>10.3f} µs")

    # ── Failure details ───────────────────────────────────────────────────────
    if failures:
        print(f"\n🔍  Failure Details (showing up to 5 of {fail_count})")
        print("-" * 60)
        for f in failures[:5]:
            print(f"  Test #{f['index']}  |  m={f['m']}, n={f['n']}")
            # Truncate long arrays for readability
            def fmt(arr, limit=8):
                if isinstance(arr, list) and len(arr) > limit:
                    return str(arr[:limit])[:-1] + f", ... +{len(arr)-limit} more]"
                return str(arr)
            print(f"    nums1 (in) : {fmt(f['nums1_in'])}")
            print(f"    nums2 (in) : {fmt(f['nums2_in'])}")
            print(f"    Expected   : {fmt(f['expected'])}")
            print(f"    Got        : {fmt(f['got'])}")
            print()
    else:
        print("\n🎉  All tests passed!")

    print("=" * 60)

    # Exit with non-zero code if any tests failed (useful for CI)
    if failures:
        sys.exit(1)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_tests(100)
