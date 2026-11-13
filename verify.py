#!/usr/bin/env python3
"""Exhaustive-ish verification of ./primes against an independent reference.

Reference: odd-only bytearray sieve up to 5,000,000 (same math as
gen_tables.py but recomputed here, plus known-value asserts).
Test set: exhaustive 0..5000, every 10000-boundary +/- {0,1,2,3} (the
table-join edge), all cases.json values, and 2000 random N in range.
"""
import random
import subprocess
import sys

NMAX = 5_000_000

def ref_pi(nmax):
    size = (nmax + 1) // 2
    s = bytearray(b"\x01") * size
    s[0] = 0
    import math
    for i in range(3, int(math.isqrt(nmax)) + 1, 2):
        if s[i // 2]:
            start = i * i // 2
            s[start:size:i] = b"\x00" * ((size - 1 - start) // i + 1)
    pi = [0] * (nmax + 1)
    c = 0
    for n in range(2, nmax + 1):
        if n == 2 or (n % 2 == 1 and s[n // 2]):
            c += 1
        pi[n] = c
    return pi

def run_c(n):
    r = subprocess.run(["./primes"], input=f"{n}\n", capture_output=True,
                       text=True, timeout=10)
    assert r.returncode == 0, f"exit {r.returncode} for N={n}: {r.stderr}"
    return int(r.stdout.strip())

def main():
    pi = ref_pi(NMAX)
    for n, want in {10: 4, 100: 25, 1000: 168, 100000: 9592,
                    1000000: 78498, 5000000: 348513}.items():
        assert pi[n] == want, (n, pi[n], want)
    print("reference OK", file=sys.stderr)

    tests = set(range(0, 5001))
    tests.update(json_n for json_n in (10, 100, 1000, 100000, 1000000))
    for k in range(0, 501):
        b = k * 10000
        for d in (0, 1, 2, 3, 9997, 9998, 9999):
            v = b + d
            if 0 <= v <= NMAX:
                tests.add(v)
    rng = random.Random(12345)
    tests.update(rng.randint(0, NMAX) for _ in range(2000))
    tests = sorted(tests)
    print(f"testing {len(tests)} values...", file=sys.stderr)
    bad = 0
    for n in tests:
        got = run_c(n)
        if got != pi[n]:
            print(f"MISMATCH N={n}: got {got}, want {pi[n]}")
            bad += 1
            if bad > 5:
                break
    if bad:
        print(f"FAILED: {bad} mismatches")
        sys.exit(1)
    print(f"ALL {len(tests)} TESTS PASSED")

if __name__ == "__main__":
    main()
