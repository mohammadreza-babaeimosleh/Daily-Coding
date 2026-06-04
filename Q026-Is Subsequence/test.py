"""
test.py — Benchmark & correctness tester for Is Subsequence
Runs 100 test cases against main.py's Solution.isSubsequence() and reports:
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
def reference(s: str, t: str) -> bool:
    it = iter(t)
    return all(c in it for c in s)


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def make_subsequence(t: str, rng: random.Random) -> str:
    """Extract a random subsequence from t."""
    if not t:
        return ""
    indices = sorted(rng.sample(range(len(t)), k=rng.randint(0, len(t))))
    return "".join(t[i] for i in indices)

def generate_test_cases(count: int) -> list:
    fixed = [
        {"s": "abc",  "t": "ahbgdc"},   # true
        {"s": "axc",  "t": "ahbgdc"},   # false
        {"s": "",     "t": "ahbgdc"},   # empty s -> true
        {"s": "abc",  "t": ""},         # empty t, non-empty s -> false
        {"s": "",     "t": ""},         # both empty -> true
        {"s": "a",    "t": "a"},        # exact match single char
        {"s": "b",    "t": "a"},        # single char miss
        {"s": "ace",  "t": "abcde"},    # true
        {"s": "aec",  "t": "abcde"},    # false (out of order)
        {"s": "z" * 100, "t": "z" * 10_000},  # max lengths, true
        {"s": "z" * 100, "t": "a" * 10_000},  # max lengths, false
    ]
    cases = [{"s": f["s"], "t": f["t"], "expected": reference(f["s"], f["t"])} for f in fixed]

    rng = random.Random(42)
    LOWER = string.ascii_lowercase
    while len(cases) < count:
        t_len = rng.randint(0, 10_000)
        t     = "".join(rng.choices(LOWER, k=t_len))
        if rng.random() < 0.5 and t:
            # guaranteed subsequence
            s = make_subsequence(t, rng)
            s = s[:100]
        else:
            s_len = rng.randint(0, 100)
            s     = "".join(rng.choices(LOWER, k=s_len))
        cases.append({"s": s, "t": t, "expected": reference(s, t)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Is Subsequence — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        s, t = case["s"], case["t"]
        start = time.perf_counter_ns()
        try:
            result = sol.isSubsequence(s, t)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "s": s, "t": t,
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue
        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "s": s, "t": t,
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
            print(f"  Test #{f['index']}")
            print(f"    s (in)     : {f['s']!r}")
            print(f"    t (in)     : {repr(f['t'][:50])}{'...' if len(f['t']) > 50 else ''}")
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
