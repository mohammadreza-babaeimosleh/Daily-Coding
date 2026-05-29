"""
test.py — Benchmark & correctness tester for Find the Index of the First Occurrence in a String
Runs 100 test cases against main.py's Solution.strStr() and reports:
  - Pass rate
  - Average / median / std-dev / min / max / p90 / p99 execution time
  - Any failing cases (up to 5 shown)
"""

import time
import random
import string
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
def reference(haystack: str, needle: str) -> int:
    idx = haystack.find(needle)
    return idx


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"haystack": "sadbutsad",  "needle": "sad"},     # 0 (first of two)
        {"haystack": "leetcode",   "needle": "leeto"},   # -1
        {"haystack": "a",          "needle": "a"},       # 0, equal strings
        {"haystack": "a",          "needle": "b"},       # -1, single char miss
        {"haystack": "aaa",        "needle": "aaaa"},    # -1, needle longer
        {"haystack": "hello",      "needle": "ll"},      # 2
        {"haystack": "aaaaa",      "needle": "bba"},     # -1
        {"haystack": "mississippi","needle": "issip"},   # 4
        {"haystack": "a" * 10_000, "needle": "a" * 9_999 + "b"},  # near-miss, stress
        {"haystack": "a" * 9_999 + "b", "needle": "b"}, # match at very end
    ]
    cases = [{"haystack": f["haystack"], "needle": f["needle"],
              "expected": reference(f["haystack"], f["needle"])} for f in fixed]

    rng = random.Random(42)
    while len(cases) < count:
        h_len = rng.randint(1, 10_000)
        n_len = rng.randint(1, min(h_len, 10_000))
        haystack = "".join(rng.choices(string.ascii_lowercase, k=h_len))
        # 50% chance needle actually appears in haystack
        if rng.random() < 0.5:
            start  = rng.randint(0, h_len - n_len)
            needle = haystack[start:start + n_len]
        else:
            needle = "".join(rng.choices(string.ascii_lowercase, k=n_len))
        cases.append({"haystack": haystack, "needle": needle,
                      "expected": reference(haystack, needle)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Find the Index of the First Occurrence — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        haystack, needle = case["haystack"], case["needle"]
        start = time.perf_counter_ns()
        try:
            result = sol.strStr(haystack, needle)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "haystack": haystack, "needle": needle,
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue
        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "haystack": haystack, "needle": needle,
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
            h_prev = repr(f["haystack"][:40]) + ("..." if len(f["haystack"]) > 40 else "")
            print(f"  Test #{f['index']}")
            print(f"    haystack : {h_prev}")
            print(f"    needle   : {f['needle']!r}")
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
