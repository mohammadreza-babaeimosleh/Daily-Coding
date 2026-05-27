"""
test.py — Benchmark & correctness tester for Longest Common Prefix
Runs 100 test cases against main.py's Solution.longestCommonPrefix() and reports:
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
def reference(strs: list) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"strs": ["flower", "flow", "flight"]},          # "fl"
        {"strs": ["dog", "racecar", "car"]},             # ""
        {"strs": ["a"]},                                 # single string
        {"strs": ["ab", "a"]},                           # prefix is shorter string
        {"strs": ["", "b"]},                             # empty string in list
        {"strs": ["abc", "abc", "abc"]},                 # all identical
        {"strs": ["abc", "abcd", "ab"]},                 # "ab"
        {"strs": ["a"] * 200},                           # max count, all same
        {"strs": ["a" * 200] * 200},                     # max count, max length, all same
        {"strs": ["a" * 200, "a" * 199 + "b"]},         # differ only at last char
        {"strs": ["ab", ""]},                            # one empty string
    ]
    cases = [{"strs": f["strs"], "expected": reference(f["strs"])} for f in fixed]

    rng = random.Random(42)
    while len(cases) < count:
        n      = rng.randint(1, 200)
        # sometimes share a common prefix, sometimes not
        if rng.random() < 0.5:
            prefix_len = rng.randint(0, 10)
            prefix     = "".join(rng.choices(string.ascii_lowercase, k=prefix_len))
            strs = [prefix + "".join(rng.choices(string.ascii_lowercase,
                    k=rng.randint(0, 200 - prefix_len))) for _ in range(n)]
        else:
            strs = ["".join(rng.choices(string.ascii_lowercase,
                    k=rng.randint(0, 200))) for _ in range(n)]
        cases.append({"strs": strs, "expected": reference(strs)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Longest Common Prefix — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        strs = list(case["strs"])   # shallow copy sufficient (strings are immutable)
        start = time.perf_counter_ns()
        try:
            result = sol.longestCommonPrefix(strs)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "strs": case["strs"],
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue
        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "strs": case["strs"],
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
            def fmt_strs(strs, limit=4):
                preview = [repr(s[:30]) + ("..." if len(s) > 30 else "") for s in strs[:limit]]
                suffix  = f", ... +{len(strs)-limit} more" if len(strs) > limit else ""
                return "[" + ", ".join(preview) + suffix + "]"
            print(f"  Test #{f['index']}")
            print(f"    strs (in)  : {fmt_strs(f['strs'])}")
            print(f"    Expected   : {f['expected']!r}")
            print(f"    Got        : {f['got']!r}")
            print()
    else:
        print("\n🎉  All tests passed!")
    print("=" * 60)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    run_tests(100)
