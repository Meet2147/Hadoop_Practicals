#!/usr/bin/env python3
import sys
import re

WORD_RE = re.compile(r"[A-Za-z0-9']+")

for raw in sys.stdin:
    line = raw.strip().lower()
    if not line:
        continue
    for word in WORD_RE.findall(line):
        # emit "word\t1"
        print(f"{word}\t1")
