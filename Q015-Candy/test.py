"""
test.py — Benchmark & correctness tester for Candy
Runs 100 test cases against main.py's Solution.candy() and reports:
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

# ── Import solution ────────────────────────────────────────────────────────────────────────────
try:
    solution_module = importlib.import_module("main")
    Solution = solution_module.Solution
except ModuleNotFoundError:
    print("❌  Could not import 'main.py'. Make sure it exists in the same directory.")
    sys.exit(1)
except AttributeError:
    print("❌  'main.py' must define a class named 'Solution'.")
    sys.exit(1)


# ── Reference solution ─────────────────────────────────────────────────────────────────────────
def reference(ratings: list) -> int:
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"ratings": [1, 0, 2]},                        # expected 5
        {"ratings": [1, 2, 2]},                        # expected 4
        {"ratings": [1]},                              # single child
        {"ratings": [1, 1, 1, 1]},                     # all equal -> all get 1
        {"ratings": [1, 2, 3, 4, 5]},                  # strictly increasing
        {"ratings": [5, 4, 3, 2, 1]},                  # strictly decreasing
        {"ratings": [1, 3, 2, 2, 1]},                  # peak in middle
        {"ratings": [1, 2, 3, 2, 1]},                  # mountain
        {"ratings": list(range(20_000))},              # max size, strictly increasing
        {"ratings": list(range(20_000, 0, -1))},       # max size, strictly decreasing
    ]
    cases = []
    for f in fixed:
        cases.append({**f, "expected": reference(f["ratings"])})
    rng = random.Random(42)
    while len(cases) < count:
        n       = rng.randint(1, 20_000)
        ratings = [rng.randint(0, 20_000) for _ in range(n)]
        cases.append({"ratings": ratings, "expected": reference(ratings)})
    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Candy — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        ratings = copy.deepcopy(case["ratings"])
        start = time.perf_counter_ns()
        try:
            result = sol.candy(ratings)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "ratings_in": case["ratings"],
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue
        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "ratings_in": case["ratings"],
                              "got": result, "expected": case["expected"]})

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
            def fmt(v, limit=8):
                if isinstance(v, list) and len(v) > limit:
                    return str(v[:limit])[:-1] + f", ... +{len(v)-limit} more]"
                return str(v)
            print(f"  Test #{f['index']}")
            print(f"    ratings (in) : {fmt(f['ratings_in'])}")
            print(f"    Expected     : {f['expected']}")
            print(f"    Got          : {f['got']}")
            print()
    else:
        print("\n🎉  All tests passed!")
    print("=" * 60)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    run_tests(100)
