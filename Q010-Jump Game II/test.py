"""
test.py — Benchmark & correctness tester for LeetCode 45 · Jump Game II
Runs 100 test cases against main.py's Solution.jump() and reports:
  - Pass rate
  - Average / median / std-dev / min / max / p90 / p99 execution time
  - Any failing cases (up to 5 shown)

Note: per the problem constraints, all inputs are guaranteed reachable.
      The test generator enforces this by construction.
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


# ── Reference solution (greedy boundary) ──────────────────────────────────────
def reference(nums: list) -> int:
    jumps = cur_end = cur_far = 0
    for i in range(len(nums) - 1):
        cur_far = max(cur_far, i + nums[i])
        if i == cur_end:
            jumps  += 1
            cur_end = cur_far
    return jumps


# ── Guaranteed-reachable array generator ──────────────────────────────────────
def make_reachable(n: int, rng: random.Random) -> list:
    """
    Build a length-n array that is always reachable by construction.
    Walk a path from 0 to n-1 assigning non-zero jumps, then randomise the rest.
    """
    nums = [0] * n
    i = 0
    while i < n - 1:
        jump = rng.randint(1, min(1000, n - 1 - i))
        nums[i] = max(nums[i], jump)
        i += rng.randint(1, jump)
    # fill remaining non-path cells with random values (reachability guaranteed)
    for k in range(n - 1):
        if nums[k] == 0:
            nums[k] = rng.randint(0, 1000)
    return nums


# ── Test-case generator ────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"nums": [2, 3, 1, 1, 4]},      # expected 2
        {"nums": [2, 3, 0, 1, 4]},      # expected 2
        {"nums": [0]},                   # single element → 0
        {"nums": [1, 0]},                # one jump → 1
        {"nums": [1, 1, 1, 1]},          # every step → 3
        {"nums": [1000, 1000]},          # one giant jump → 1
        {"nums": [3, 0, 0, 0]},          # big jump over zeros → 1
    ]

    cases = []
    for f in fixed:
        cases.append({**f, "expected": reference(f["nums"])})

    rng = random.Random(42)
    while len(cases) < count:
        n    = rng.randint(1, 10_000)
        nums = make_reachable(n, rng)
        cases.append({"nums": nums, "expected": reference(nums)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  LeetCode 45 · Jump Game II — Test Suite")
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
            result = sol.jump(nums)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({
                "index":   idx + 1,
                "nums_in": case["nums"],
                "got":     f"EXCEPTION: {exc}",
                "expected": case["expected"],
            })
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)

        if result == case["expected"]:
            passed += 1
        else:
            failures.append({
                "index":   idx + 1,
                "nums_in": case["nums"],
                "got":     result,
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
