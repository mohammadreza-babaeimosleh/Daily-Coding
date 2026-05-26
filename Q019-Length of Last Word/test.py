"""
test.py — Benchmark & correctness tester for Length of Last Word
Runs 100 test cases against main.py's Solution.lengthOfLastWord() and reports:
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
def reference(s: str) -> int:
    return len(s.split()[-1])


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def rand_word(rng, min_len=1, max_len=20):
    length = rng.randint(min_len, max_len)
    return "".join(rng.choices(string.ascii_letters, k=length))

def generate_test_cases(count: int) -> list:
    fixed = [
        {"s": "Hello World"},
        {"s": "   fly me   to   the moon  "},
        {"s": "luffy is still joyboy"},
        {"s": "a"},
        {"s": "   a"},
        {"s": "a   "},
        {"s": "   a   "},
        {"s": "word"},
        {"s": "first last"},
        {"s": "a " * 5000 + "end"},         # long string, last word at end
        {"s": "end" + " " * 9997},          # long trailing spaces
    ]
    cases = [{"s": f["s"], "expected": reference(f["s"])} for f in fixed]

    rng = random.Random(42)
    while len(cases) < count:
        n_words  = rng.randint(1, 20)
        words    = [rand_word(rng) for _ in range(n_words)]
        # random leading/trailing/inter spaces
        sep      = lambda: " " * rng.randint(1, 5)
        s        = sep() * rng.randint(0, 3) + sep().join(words) + sep() * rng.randint(0, 3)
        cases.append({"s": s, "expected": reference(s)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Length of Last Word — Test Suite")
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
            result = sol.lengthOfLastWord(s)
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
