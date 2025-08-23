#!/usr/bin/env python3
import sys
from collections import defaultdict

current_key = None
Avals = defaultdict(float)
Bvals = defaultdict(float)

def flush(key, A, B):
    if not key:
        return
    total = 0.0
    for j, a in A.items():
        if j in B:
            total += a * B[j]
    if total != 0.0:
        i, k = key
        print(f"{i} {k} {total}")

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    key_str, payload = line.split('\t', 1)
    i, k = map(int, key_str.split(','))
    src, j_str, v_str = payload.split(',', 2)
    j, v = int(j_str), float(v_str)

    if current_key != (i, k):
        flush(current_key, Avals, Bvals)
        current_key = (i, k)
        Avals.clear(); Bvals.clear()

    if src == 'A':
        Avals[j] += v
    else:
        Bvals[j] += v

flush(current_key, Avals, Bvals)
