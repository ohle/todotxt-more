#!/usr/bin/env python3

import sys
import fileinput
from collections import defaultdict

counter = defaultdict(int)
for line in fileinput.input():
    line = line.strip()
    fields = line.split(' ')
    try:
        duration = int(fields[0])
    except:
        continue
    for field in fields:
        if field[0] in ('+','@'):
            counter[field] += duration

for key, value in counter.items():
    print(key, value)
