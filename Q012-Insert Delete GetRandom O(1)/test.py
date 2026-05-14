"""
test.py — Benchmark & correctness tester for LeetCode 380 · Insert Delete GetRandom O(1)
Runs 100 operation-sequence test cases against main.py's RandomizedSet and reports:
  - Pass rate
  - Average / median / std-dev / min / max / p90 / p99 execution time per sequence
  - Any failing cases (up to 5 shown)
"""

import time
import random
import statistics
import importlib
import sys

# ── Import solution ────────────────────────────────────────────────────────────
try:
    solution_module = importlib.import_module("main")
    RandomizedSet = solution_module.RandomizedSet
except ModuleNotFoundError:
    print("❌  Could not import 'main.py'. Make sure it exists in the same directory.")
    sys.exit(1)
except AttributeError:
    print("❌  'main.py' must define a class named 'RandomizedSet'.")
    sys.exit(1)


# ── Reference implementation ───────────────────────────────────────────────────
class ReferenceSet:
    def __init__(self):        self._s = set()
    def insert(self, v):       added = v not in self._s; self._s.add(v); return added
    def remove(self, v):       present = v in self._s; self._s.discard(v); return present
    def contains(self, v):     return v in self._s
    def elements(self):        return list(self._s)


# ── Sequence generator ────────────────────────────────────────────────────────
def generate_sequences(count: int, rng: random.Random) -> list:
    """Each sequence is a list of (op, arg) tuples. op ∈ insert/remove/getRandom."""

    fixed = [
        [("insert", 1), ("remove", 2), ("insert", 2),
         ("getRandom", None), ("remove", 1), ("insert", 2), ("getRandom", None)],
        [("insert", 0), ("getRandom", None), ("remove", 0), ("insert", -1), ("getRandom", None)],
        [("insert", i) for i in range(50)] + [("getRandom", None)] * 10 +
        [("remove", i) for i in range(50)] + [("insert", 99), ("getRandom", None)],
    ]

    sequences = list(fixed)

    while len(sequences) < count:
        n_ops = rng.randint(10, 2000)
        ref   = ReferenceSet()
        seq   = []
        for _ in range(n_ops):
            op = rng.choice(["insert", "insert", "remove", "getRandom"])
            if op == "insert":
                val = rng.randint(-(2**31), 2**31 - 1)
                seq.append(("insert", val))
                ref.insert(val)
            elif op == "remove":
                if ref.elements():
                    val = rng.choice(ref.elements()) if rng.random() < 0.5 else rng.randint(-(2**31), 2**31 - 1)
                else:
                    val = rng.randint(-(2**31), 2**31 - 1)
                seq.append(("remove", val))
                ref.remove(val)
            else:  # getRandom — only add if set is non-empty
                if ref.elements():
                    seq.append(("getRandom", None))
        sequences.append(seq)

    return sequences[:count]


# ── Runner ────────────────────────────────────────────────────────────────────
def run_tests(num_tests: int = 100) -> None:
    print("=" * 60)
    print("  Insert Delete GetRandom O(1) — Test Suite")
    print("=" * 60)

    rng       = random.Random(42)
    sequences = generate_sequences(num_tests, rng)

    passed   = 0
    failures = []
    times_ns = []

    for idx, seq in enumerate(sequences):
        rs  = RandomizedSet()
        ref = ReferenceSet()
        ok  = True
        fail_detail = None

        start = time.perf_counter_ns()
        try:
            for op, arg in seq:
                if op == "insert":
                    got      = rs.insert(arg)
                    expected = ref.insert(arg)
                    if got != expected:
                        ok = False
                        fail_detail = f"insert({arg}): expected {expected}, got {got}"
                        break
                elif op == "remove":
                    got      = rs.remove(arg)
                    expected = ref.remove(arg)
                    if got != expected:
                        ok = False
                        fail_detail = f"remove({arg}): expected {expected}, got {got}"
                        break
                else:  # getRandom
                    val = rs.getRandom()
                    if val not in ref.elements():
                        ok = False
                        fail_detail = f"getRandom() returned {val}, not in set {sorted(ref.elements())[:8]}"
                        break
            elapsed = time.perf_counter_ns() - start
        except Exception as exc:
            elapsed = time.perf_counter_ns() - start
            ok = False
            fail_detail = f"EXCEPTION: {exc}"

        times_ns.append(elapsed)

        if ok:
            passed += 1
        else:
            failures.append({"index": idx + 1, "detail": fail_detail,
                              "seq_len": len(seq)})

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

    print(f"\n📊  Results ({num_tests} operation-sequence tests)")
    print(f"  ✅  Passed  : {passed}/{num_tests}  ({pass_rate:.1f}%)")
    print(f"  ❌  Failed  : {fail_count}")

    print(f"\n⏱️   Execution Time (per sequence)")
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
            print(f"  Test #{f['index']}  |  sequence length: {f['seq_len']}")
            print(f"    {f['detail']}")
            print()
    else:
        print("\n🎉  All tests passed!")

    print("=" * 60)

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    run_tests(100)
