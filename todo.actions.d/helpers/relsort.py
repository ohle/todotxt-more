#!/usr/bin/env python3

import fileinput
import datetime
import re


TAG_DATE = re.compile(r'\d\d\d\d-\d\d-\d\d')

now = datetime.datetime.now()
today = datetime.datetime(now.year, now.month, now.day)

for line in fileinput.input():
    fields = line.strip().split(" ")
    haslinenum = fields[0].isdigit()
    if haslinenum:
        linenum = fields[0]
        i = 1
    else:
        i = 0
    if fields[i] in ("TODO:", "--"):
        continue
    sortkey = ""
    if len(fields) > i:
        #priority
        if fields[i] == "(A)":
            sortkey = "A"
            i += 1
        if fields[i] == "(B)":
            sortkey = "B"
            i += 1
        if fields[i] == "(C)":
            sortkey = "C"
            i += 1
        if fields[i] == "(D)":
            sortkey = "D"
            i += 1
    if len(fields) > i:
        if TAG_DATE.match(fields[i]):
            dt = datetime.datetime(int(fields[i][0:4]), int(fields[i][5:7]), int(fields[i][8:10]))
            days = int((today.timestamp() - dt.timestamp()) / (3600*24))
            fields[i] = "%04dd" % days
            if sortkey:
                sortkey += fields[i]
            else:
                sortkey = "Y" + fields[i]
    if not sortkey:
        sortkey = "Z"


    print(sortkey, " ".join(fields))
            

