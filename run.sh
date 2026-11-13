#!/bin/sh
# Run command for the AIProve fastest-primes entry.
# Usage: echo 5000000 | ./run.sh   -> 348513
# Prefers the prebuilt x86-64 binary (built from primes.c with gcc -O3);
# rebuilds from source on any other architecture or if the binary is missing.
set -e
cd "$(dirname "$0")"
if [ -x ./primes ] && [ "$(uname -m)" = "x86_64" ]; then
    exec ./primes
fi
BIN="${TMPDIR:-/tmp}/aiprove-primes-$$"
cc -O3 -o "$BIN" primes.c
exec "$BIN"
