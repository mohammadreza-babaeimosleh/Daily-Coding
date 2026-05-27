"""
test.py — Benchmark & correctness tester for Zigzag Conversion
Runs 100 test cases against main.py's Solution.convert() and reports:
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
def reference(s: str, numRows: int) -> str:
    if numRows == 1 or numRows >= len(s):
        return s
    rows = [""] * numRows
    row, direction = 0, 1
    for ch in s:
        rows[row] += ch
        if row == 0:
            direction = 1
        elif row == numRows - 1:
            direction = -1
        row += direction
    return "".join(rows)


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
VALID_CHARS = string.ascii_letters + ",."

def rand_s(rng, min_len=1, max_len=1000):
    n = rng.randint(min_len, max_len)
    return "".join(rng.choices(VALID_CHARS, k=n))

def generate_test_cases(count: int) -> list:
    fixed = [
        {"s": "PAYPALISHIRING", "numRows": 3},   # "PAHNAPLSIIGYIR"
        {"s": "PAYPALISHIRING", "numRows": 4},   # "PINALSIGYAHRPI"
        {"s": "A",              "numRows": 1},   # "A"
        {"s": "AB",             "numRows": 1},   # numRows=1, return as-is
        {"s": "AB",             "numRows": 2},   # two rows
        {"s": "ABCDE",          "numRows": 5},   # numRows == len(s)
        {"s": "ABCDE",          "numRows": 10},  # numRows > len(s)
        {"s": "A",              "numRows": 1000},# single char, many rows
        {"s": "a,b.c",          "numRows": 2},   # commas and dots
        {"s": "A" * 1000,       "numRows": 500}, # max stress
    ]
    cases = [{"s": f["s"], "numRows": f["numRows"],
              "expected": reference(f["s"], f["numRows"])} for f in fixed]

    rng = random.Random(42)
    while len(cases) < count:
        s       = rand_s(rng)
        numRows = rng.randint(1, 1000)
        cases.append({"s": s, "numRows": numRows, "expected": reference(s, numRows)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Zigzag Conversion — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        s, numRows = case["s"], case["numRows"]
        start = time.perf_counter_ns()
        try:
            result = sol.convert(s, numRows)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "s": s, "numRows": numRows,
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue
        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "s": s, "numRows": numRows,
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
            preview = repr(f["s"][:40]) + ("..." if len(f["s"]) > 40 else "")
            print(f"  Test #{f['index']}  |  numRows={f['numRows']}")
            print(f"    s (in)     : {preview}")
            print(f"    Expected   : {repr(f['expected'][:40])}")
            print(f"    Got        : {repr(str(f['got'])[:40])}")
            print()
    else:
        print("\n🎉  All tests passed!")
    print("=" * 60)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    run_tests(100)
