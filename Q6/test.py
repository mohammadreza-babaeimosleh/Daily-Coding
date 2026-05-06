"""
test.py — Benchmark & correctness tester for LeetCode 189 · Rotate Array
Runs 100 test cases against main.py's Solution.rotate() and reports:
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
def reference(nums: list, k: int) -> list:
    n = len(nums)
    k = k % n
    return nums[-k:] + nums[:-k] if k else nums[:]


# ── Test-case generator ────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"nums": [1, 2, 3, 4, 5, 6, 7], "k": 3},
        {"nums": [-1, -100, 3, 99],      "k": 2},
        {"nums": [1],                    "k": 0},
        {"nums": [1, 2],                 "k": 1},
        {"nums": [1, 2, 3],              "k": 3},   # k == n, no-op
        {"nums": [1, 2, 3],              "k": 6},   # k multiple of n
        {"nums": [1, 2, 3, 4, 5],        "k": 100}, # k >> n
    ]

    cases = []
    for f in fixed:
        cases.append({**f, "expected": reference(f["nums"], f["k"])})

    rng = random.Random(42)
    while len(cases) < count:
        n    = rng.randint(1, 100_000)
        nums = [rng.randint(-(2**31), 2**31 - 1) for _ in range(n)]
        k    = rng.randint(0, 100_000)
        cases.append({"nums": nums, "k": k, "expected": reference(nums, k)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  LeetCode 189 · Rotate Array — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()

    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        nums = copy.deepcopy(case["nums"])
        k    = case["k"]

        start = time.perf_counter_ns()
        try:
            sol.rotate(nums, k)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({
                "index":    idx + 1,
                "nums_in":  case["nums"],
                "k":        k,
                "got":      f"EXCEPTION: {exc}",
                "expected": case["expected"],
            })
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)

        if nums == case["expected"]:
            passed += 1
        else:
            failures.append({
                "index":    idx + 1,
                "nums_in":  case["nums"],
                "k":        k,
                "got":      nums,
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
            def fmt(v, limit=8):
                if isinstance(v, list) and len(v) > limit:
                    return str(v[:limit])[:-1] + f", ... +{len(v)-limit} more]"
                return str(v)
            print(f"  Test #{f['index']}  |  k={f['k']}")
            print(f"    nums (in)  : {fmt(f['nums_in'])}")
            print(f"    Expected   : {fmt(f['expected'])}")
            print(f"    Got        : {fmt(f['got'])}")
            print()
    else:
        print("\n🎉  All tests passed!")

    print("=" * 60)

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    run_tests(100)
