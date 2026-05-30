"""
test.py — Benchmark & correctness tester for Text Justification
Runs 100 test cases against main.py's Solution.fullJustify() and reports:
  - Pass rate
  - Average / median / std-dev / min / max / p90 / p99 execution time
  - Any failing cases (up to 5 shown)
"""

import time
import copy
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
def reference(words: list, maxWidth: int) -> list:
    res, i, n = [], 0, len(words)
    while i < n:
        line_len, j = len(words[i]), i + 1
        while j < n and line_len + 1 + len(words[j]) <= maxWidth:
            line_len += 1 + len(words[j])
            j += 1
        line_words = words[i:j]
        num_words  = len(line_words)
        if j == n or num_words == 1:
            line = " ".join(line_words).ljust(maxWidth)
        else:
            total_spaces = maxWidth - sum(len(w) for w in line_words)
            gaps         = num_words - 1
            each, extra  = divmod(total_spaces, gaps)
            line = ""
            for k in range(gaps):
                line += line_words[k] + " " * each + (" " if k < extra else "")
            line += line_words[-1]
        res.append(line)
        i = j
    return res


# ── Validation helpers ───────────────────────────────────────────────────────────────────────
def validate(result: list, expected: list, maxWidth: int) -> str | None:
    """Returns an error message, or None if valid."""
    if not isinstance(result, list):
        return f"Expected list, got {type(result).__name__}"
    if len(result) != len(expected):
        return f"Wrong number of lines: expected {len(expected)}, got {len(result)}"
    for idx, (got_line, exp_line) in enumerate(zip(result, expected)):
        if len(got_line) != maxWidth:
            return f"Line {idx}: wrong length {len(got_line)}, expected {maxWidth}"
        if got_line != exp_line:
            return f"Line {idx}: expected {exp_line!r}, got {got_line!r}"
    return None


# ── Test-case generator ──────────────────────────────────────────────────────────────────────────────
def generate_test_cases(count: int) -> list:
    fixed = [
        {"words": ["This","is","an","example","of","text","justification."], "maxWidth": 16},
        {"words": ["What","must","be","acknowledgment","shall","be"],         "maxWidth": 16},
        {"words": ["Science","is","what","we","understand","well","enough",
                   "to","explain","to","a","computer.","Art","is",
                   "everything","else","we","do"],                            "maxWidth": 20},
        {"words": ["a"],                                                       "maxWidth": 1},
        {"words": ["a"],                                                       "maxWidth": 5},
        {"words": ["word"],                                                    "maxWidth": 4},  # exact fit
        {"words": ["a","b","c","d"],                                           "maxWidth": 1},  # each alone
        {"words": ["longword"] * 10,                                           "maxWidth": 20},
    ]
    cases = [{"words": f["words"], "maxWidth": f["maxWidth"],
              "expected": reference(f["words"], f["maxWidth"])} for f in fixed]

    rng = random.Random(42)
    CHARS = string.ascii_letters + string.punctuation.replace(" ", "")
    while len(cases) < count:
        maxWidth = rng.randint(1, 100)
        n_words  = rng.randint(1, 300)
        words    = []
        for _ in range(n_words):
            wlen = rng.randint(1, min(20, maxWidth))
            words.append("".join(rng.choices(CHARS, k=wlen)))
        cases.append({"words": words, "maxWidth": maxWidth,
                      "expected": reference(words, maxWidth)})

    return cases[:count]


# ── Runner ────────────────────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Text Justification — Test Suite")
    print("=" * 60)

    cases    = generate_test_cases(num_tests)
    sol      = Solution()
    passed   = 0
    failures = []
    times_ns = []

    for idx, case in enumerate(cases):
        words    = copy.deepcopy(case["words"])
        maxWidth = case["maxWidth"]

        start = time.perf_counter_ns()
        try:
            result = sol.fullJustify(words, maxWidth)
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            failures.append({"index": idx+1, "words": case["words"], "maxWidth": maxWidth,
                              "detail": f"EXCEPTION: {exc}"})
            times_ns.append(elapsed)
            continue

        times_ns.append(elapsed)
        err = validate(result, case["expected"], maxWidth)
        if err is None:
            passed += 1
        else:
            failures.append({"index": idx+1, "words": case["words"],
                              "maxWidth": maxWidth, "detail": err})

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
            words_prev = str(f["words"][:5])[:-1] + (", ...]" if len(f["words"]) > 5 else "]")
            print(f"  Test #{f['index']}  |  maxWidth={f['maxWidth']}")
            print(f"    words    : {words_prev}")
            print(f"    detail   : {f['detail']}")
            print()
    else:
        print("\n🎉  All tests passed!")
    print("=" * 60)
    if failures:
        sys.exit(1)

if __name__ == "__main__":
    run_tests(100)
