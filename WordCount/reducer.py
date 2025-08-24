#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for raw in sys.stdin:
    line = raw.strip()
    if not line:
        continue
    try:
        word, count_str = line.split("\t", 1)
        count = int(count_str)
    except ValueError:
        # skip malformed line
        continue

    if current_word is None:
        current_word = word

    if word != current_word:
        # flush previous
        print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = 0

    current_count += count

# flush last key
if current_word is not None:
    print(f"{current_word}\t{current_count}")
