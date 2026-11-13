/* Baseline for comparison only: plain odd-only Eratosthenes sieve up to N. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1)
        return 1;
    if (n < 2) {
        puts("0");
        return 0;
    }
    long size = (n + 1) / 2; /* odds only: index i -> number 2i+1 */
    unsigned char *s = malloc((size_t)size);
    if (!s)
        return 1;
    memset(s, 1, (size_t)size);
    s[0] = 0; /* 1 */
    for (long p = 3; p * p <= n; p += 2) {
        if (s[p / 2]) {
            long step = p;
            for (long m = p * p; m <= n; m += 2 * step)
                s[m / 2] = 0;
        }
    }
    long count = 1; /* prime 2 */
    for (long i = 1; i < size; i++)
        count += s[i];
    printf("%ld\n", count);
    free(s);
    return 0;
}
