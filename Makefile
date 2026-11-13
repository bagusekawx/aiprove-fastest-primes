CC ?= cc
CFLAGS ?= -O3

all: primes

primes: primes.c tables.h
	$(CC) $(CFLAGS) -o primes primes.c

baseline_sieve: baseline_sieve.c
	$(CC) $(CFLAGS) -o baseline_sieve baseline_sieve.c

# Regenerate the embedded tables (also re-verifies the reference sieve).
tables.h: gen_tables.py
	python3 gen_tables.py

check: primes
	python3 verify.py

clean:
	rm -f primes baseline_sieve

.PHONY: all check clean
