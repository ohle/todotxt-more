#!/usr/bin/env python3

import sys
import fileinput
from collections import defaultdict

if len(sys.argv) > 1 and sys.argv[1] == "--all":
    all = True
    del sys.argv[1]
else:
    all = False


counter = defaultdict(int)
for line in fileinput.input():
    line = line.strip()
    fields = line.split(' ')
    try:
        duration = int(fields[0])
    except:
        continue
    for field in fields:
        if field and field[0] in ('+','@'):
            counter[field] += duration
    if all:
        counter[" ".join(fields[1:])] += duration

for key, value in sorted(counter.items(),key=lambda x: -1 * int(x[1])):
    print(value, key)
