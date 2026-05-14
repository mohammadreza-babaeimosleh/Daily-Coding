"""
test.py — Benchmark & correctness tester for LeetCode 27 · Remove Element
Runs 100 test cases against main.py's Solution.removeElement() and reports:
  - Pass rate
  - Average / min / max / std-dev / median / p90 / p99 execution time
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
def reference(nums: list, val: int):
    """Returns (k, sorted first-k elements) without modifying input."""
    kept = [x for x in nums if x != val]
    return len(kept), sorted(kept)


# ── Test-case generator ────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list[dict]:
    fixed = [
        {"nums": [3, 2, 2, 3],          "val": 3},
        {"nums": [0, 1, 2, 2, 3, 0, 4, 2], "val": 2},
        {"nums": [],                     "val": 0},
        {"nums": [1],                    "val": 1},
        {"nums": [1],                    "val": 2},
    ]

    cases = []
    for f in fixed:
        k, expected_sorted = reference(f["nums"], f["val"])
        cases.append({**f, "expected_k": k, "expected_sorted": expected_sorted})

    rng = random.Random(42)
    while len(cases) < count:
        length = rng.randint(0, 100)
        nums = [rng.randint(0, 50) for _ in range(length)]
        val  = rng.randint(0, 100)
        k, expected_sorted = reference(nums, val)
        cases.append({"nums": nums, "val": val,
                      "expected_k": k, "expected_sorted": expected_sorted})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  LeetCode 27 · Remove Element — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()

    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        nums = copy.deepcopy(case["nums"])
        val  = case["val"]

        start = time.perf_counter_ns()
        try:
            k = sol.removeElement(nums, val)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({
                "index":    idx + 1,
                "nums_in":  case["nums"],
                "val":      val,
                "got":      f"EXCEPTION: {exc}",
                "expected": f"k={case['expected_k']}, sorted={case['expected_sorted']}",
            })
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)

        # Validate: k must match, and first k elements sorted must match
        actual_sorted = sorted(nums[:k])
        if k == case["expected_k"] and actual_sorted == case["expected_sorted"]:
            passed += 1
        else:
            failures.append({
                "index":    idx + 1,
                "nums_in":  case["nums"],
                "val":      val,
                "got":      f"k={k}, sorted first-k={actual_sorted}",
                "expected": f"k={case['expected_k']}, sorted={case['expected_sorted']}",
            })

    # ── Statistics ─────────────────────────────────────────────────────────────
    avg_us = statistics.mean(times_ns)    / 1_000
    min_us = min(times_ns)                / 1_000
    max_us = max(times_ns)                / 1_000
    std_us = statistics.stdev(times_ns)   / 1_000 if len(times_ns) > 1 else 0.0
    med_us = statistics.median(times_ns)  / 1_000

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
            print(f"  Test #{f['index']}  |  val={f['val']}")
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
