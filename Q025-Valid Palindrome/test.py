"""
test.py — Benchmark & correctness tester for Valid Palindrome
Runs 100 test cases against main.py's Solution.isPalindrome() and reports:
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
def reference(s: str) -> bool:
    filtered = [c.lower() for c in s if c.isalnum()]
    return filtered == filtered[::-1]


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def make_palindrome_str(rng, max_len=200_000):
    """Build a string whose alphanumeric chars form a palindrome."""
    half_len = rng.randint(0, min(50_000, max_len // 2))
    alphanum = string.ascii_letters + string.digits
    noise    = string.punctuation + " "
    half     = [rng.choice(alphanum) for _ in range(half_len)]
    middle   = [rng.choice(alphanum)] if rng.random() < 0.5 else []
    core     = half + middle + half[::-1]
    # sprinkle noise characters randomly
    result = []
    for ch in core:
        result.append(ch)
        if rng.random() < 0.3:
            result.append(rng.choice(noise))
    return "".join(result)[:max_len]

def generate_test_cases(count: int) -> list:
    fixed = [
        {"s": "A man, a plan, a canal: Panama"},  # true
        {"s": "race a car"},                       # false
        {"s": " "},                                # true (empty after filter)
        {"s": "a"},                                # true
        {"s": "ab"},                               # false
        {"s": "0P"},                               # false (digit vs letter)
        {"s": "A" * 200_000},                      # max length, all same
        {"s": "Ab" * 100_000},                     # max length, not palindrome
        {"s": ".,"},                               # true (no alphanums)
        {"s": "No lemon, no melon"},               # true
    ]
    cases = [{"s": f["s"], "expected": reference(f["s"])} for f in fixed]

    rng = random.Random(42)
    PRINTABLE = string.printable.strip("\t\n\r\x0b\x0c")
    while len(cases) < count:
        if rng.random() < 0.5:
            # generate a true palindrome
            s = make_palindrome_str(rng)
        else:
            # generate a random string (likely not a palindrome)
            n = rng.randint(1, 200_000)
            s = "".join(rng.choices(PRINTABLE, k=n))
        cases.append({"s": s, "expected": reference(s)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Valid Palindrome — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        s = case["s"]
        start = time.perf_counter_ns()
        try:
            result = sol.isPalindrome(s)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "s": s,
                              "got": f"EXCEPTION: {exc}", "expected": case["expected"]})
            times_ns.append(elapsed)
            continue
        times_ns.append(elapsed)
        if result == case["expected"]:
            passed += 1
        else:
            failures.append({"index": idx+1, "s": s,
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
            preview = repr(f["s"][:60]) + ("..." if len(f["s"]) > 60 else "")
            print(f"  Test #{f['index']}")
            print(f"    s (in)     : {preview}")
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
