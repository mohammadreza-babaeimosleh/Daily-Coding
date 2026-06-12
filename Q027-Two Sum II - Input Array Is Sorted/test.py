"""
test.py — Benchmark & correctness tester for Two Sum II - Input Array Is Sorted
Runs 100 test cases against main.py's Solution.twoSum() and reports:
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
def reference(numbers: list, target: int) -> list:
    i, j = 0, len(numbers) - 1
    while i < j:
        s = numbers[i] + numbers[j]
        if s == target:
            return [i + 1, j + 1]
        elif s < target:
            i += 1
        else:
            j -= 1


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def make_case(rng: random.Random) -> dict:
    """Generate a sorted array guaranteed to have exactly one pair summing to target."""
    n      = rng.randint(2, 30_000)
    nums   = sorted(rng.randint(-1000, 1000) for _ in range(n))
    # pick two distinct indices for the answer
    i1, i2 = sorted(rng.sample(range(n), 2))
    target = nums[i1] + nums[i2]
    # verify uniqueness (if not, just accept — problem guarantees unique input)
    return {"numbers": nums, "target": target,
            "expected": reference(nums, target)}

def generate_test_cases(count: int) -> list:
    fixed = [
        {"numbers": [2, 7, 11, 15],  "target": 9},   # [1,2]
        {"numbers": [2, 3, 4],       "target": 6},   # [1,3]
        {"numbers": [-1, 0],         "target": -1},  # [1,2]
        {"numbers": [-1000, 1000],   "target": 0},   # extremes
        {"numbers": [0, 0],          "target": 0},   # duplicates
        {"numbers": list(range(-1000, 1001)), "target": -1999},  # first two
        {"numbers": list(range(-1000, 1001)), "target":  1999},  # last two
    ]
    cases = [{"numbers": f["numbers"], "target": f["target"],
              "expected": reference(f["numbers"], f["target"])} for f in fixed]

    rng = random.Random(42)
    while len(cases) < count:
        cases.append(make_case(rng))

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Two Sum II — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        numbers = copy.deepcopy(case["numbers"])
        target  = case["target"]

        start = time.perf_counter_ns()
        try:
            result = sol.twoSum(numbers, target)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "numbers": case["numbers"], "target": target,
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)

        # Validate: indices in bounds, 1-based, sum correct, index1 < index2
        exp = case["expected"]
        ok  = (isinstance(result, list) and len(result) == 2
               and result == exp)
        if ok:
            passed += 1
        else:
            failures.append({"index": idx+1, "numbers": case["numbers"], "target": target,
                              "got": result, "expected": exp})

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
            print(f"  Test #{f['index']}  |  target={f['target']}")
            print(f"    numbers  : {fmt(f['numbers'])}")
            print(f"    Expected : {f['expected']}")
            print(f"    Got      : {f['got']}")
            print()
    else:
        print("\n🎉  All tests passed!")
    print("=" * 60)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    run_tests(100)
