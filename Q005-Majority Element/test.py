"""
test.py — Benchmark & correctness tester for LeetCode 169 · Majority Element
Runs 100 test cases against main.py's Solution.majorityElement() and reports:
  - Pass rate
  - Average / median / std-dev / min / max / p90 / p99 execution time
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


# ── Reference solution ─────────────────────────────────────────────────────────
def reference(nums: list) -> int:
    return max(set(nums), key=nums.count)


# ── Test-case generator ────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"nums": [3, 2, 3]},
        {"nums": [2, 2, 1, 1, 1, 2, 2]},
        {"nums": [1]},
        {"nums": [1, 1]},
        {"nums": [-1, -1, 2]},
        {"nums": [10**9, 10**9, -10**9]},
    ]

    cases = []
    for f in fixed:
        cases.append({**f, "expected": reference(f["nums"])})

    rng = random.Random(42)
    while len(cases) < count:
        n        = rng.randint(1, 50_000)
        majority = rng.randint(-10**9, 10**9)
        # majority element must appear more than n//2 times
        majority_count = n // 2 + 1
        other_count    = n - majority_count
        others = [rng.randint(-10**9, 10**9) for _ in range(other_count)]
        nums   = [majority] * majority_count + others
        rng.shuffle(nums)
        cases.append({"nums": nums, "expected": majority})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  LeetCode 169 · Majority Element — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()

    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        nums = copy.deepcopy(case["nums"])

        start = time.perf_counter_ns()
        try:
            result = sol.majorityElement(nums)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({
                "index":    idx + 1,
                "nums_in":  case["nums"],
                "got":      f"EXCEPTION: {exc}",
                "expected": case["expected"],
            })
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)

        if result == case["expected"]:
            passed += 1
        else:
            failures.append({
                "index":    idx + 1,
                "nums_in":  case["nums"],
                "got":      result,
                "expected": case["expected"],
            })

    # ── Statistics ─────────────────────────────────────────────────────────────
    avg_us = statistics.mean(times_ns)   / 1_000
    min_us = min(times_ns)               / 1_000
    max_us = max(times_ns)               / 1_000
    std_us = statistics.stdev(times_ns)  / 1_000 if len(times_ns) > 1 else 0.0
    med_us = statistics.median(times_ns) / 1_000

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

    if failures:
        print(f"\n🔍  Failure Details (showing up to 5 of {fail_count})")
        print("-" * 60)
        for f in failures[:5]:
            def fmt(arr, limit=8):
                if isinstance(arr, list) and len(arr) > limit:
                    return str(arr[:limit])[:-1] + f", ... +{len(arr)-limit} more]"
                return str(arr)
            print(f"  Test #{f['index']}")
            print(f"    nums (in)  : {fmt(f['nums_in'])}")
            print(f"    Expected   : {f['expected']}")
            print(f"    Got        : {f['got']}")
            print()
    else:
        print("\n🎉  All tests passed!")

    print("=" * 60)

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    run_tests(100)
