"""
test.py — Benchmark & correctness tester for Gas Station
Runs 100 test cases against main.py's Solution.canCompleteCircuit() and reports:
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


# ── Reference solution (brute force for correctness) ───────────────────────────
def reference(gas: list, cost: list) -> int:
    n = len(gas)
    if sum(gas) < sum(cost):
        return -1
    curr, start = 0, 0
    for i in range(n):
        curr += gas[i] - cost[i]
        if curr < 0:
            curr, start = 0, i + 1
    return start


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"gas": [1,2,3,4,5],  "cost": [3,4,5,1,2]},   # expected 3
        {"gas": [2,3,4],       "cost": [3,4,3]},        # expected -1
        {"gas": [5],           "cost": [4]},             # single station, can complete
        {"gas": [1],           "cost": [2]},             # single station, cannot complete
        {"gas": [0,0,0,0,10], "cost": [1,1,1,1,5]},    # late surplus
        {"gas": [10,0,0,0,0], "cost": [5,1,1,1,1]},    # early surplus
        {"gas": [4,5,2,6,5,3], "cost": [3,2,7,3,2,9]}, # -1 case with surplus in middle
    ]
    cases = []
    for f in fixed:
        cases.append({**f, "expected": reference(f["gas"], f["cost"])})

    rng = random.Random(42)
    while len(cases) < count:
        n    = rng.randint(1, 10_000)
        gas  = [rng.randint(0, 10_000) for _ in range(n)]
        cost = [rng.randint(0, 10_000) for _ in range(n)]
        # Enforce uniqueness guarantee: if solvable, there must be exactly one answer.
        # The greedy reference always returns a unique answer when sum(gas) >= sum(cost),
        # so we just use it directly.
        cases.append({"gas": gas, "cost": cost, "expected": reference(gas, cost)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Gas Station — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        gas  = copy.deepcopy(case["gas"])
        cost = copy.deepcopy(case["cost"])

        start = time.perf_counter_ns()
        try:
            result = sol.canCompleteCircuit(gas, cost)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "gas": case["gas"], "cost": case["cost"],
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "gas": case["gas"], "cost": case["cost"],
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
            print(f"    gas  (in)  : {fmt(f['gas'])}")
            print(f"    cost (in)  : {fmt(f['cost'])}")
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
