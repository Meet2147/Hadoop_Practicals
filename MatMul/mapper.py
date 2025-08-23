#!/usr/bin/env python3
import os, sys

# Matrix dimensions passed via environment variables
MAX_I = int(os.environ["MAX_I"])  # Rows of A
MAX_K = int(os.environ["MAX_K"])  # Cols of B

for raw in sys.stdin:
    line = raw.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split(',')
    if len(parts) != 4:
        continue

    name, r, c, v = parts
    r, c, v = int(r), int(c), float(v)

    if name.upper() == 'A':
        for k_idx in range(MAX_K):
            print(f"{r},{k_idx}\tA,{c},{v}")
    elif name.upper() == 'B':
        for i_idx in range(MAX_I):
            print(f"{i_idx},{c}\tB,{r},{v}")
