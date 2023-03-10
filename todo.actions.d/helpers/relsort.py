#!/usr/bin/env python3

import fileinput
import datetime
import re
import sys


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
    if '#timetracking' in fields:
        sortkey = '!'
    elif len(fields) > i:
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
        hasdue = [ j for j,x in enumerate(fields[0:]) if x.startswith("due:") ]
        if hasdue:
            #due dates take precedence over creation dates
            i_orig = i
            i = hasdue[0] 

            year = int(fields[i][4:8])
            month = int(fields[i][9:11])
            day = int(fields[i][12:14])
            if len(fields[i]) > 14:
                hour = int(fields[i][15:17])
                try:
                    min = int(fields[i][18:20])
                except:
                    min = 0
                try:
                    sec = int(fields[i][21:23])
                except:
                    sec = 0
                try:
                    dt = datetime.datetime(year, month, day, hour,min,sec)
                except ValueError:
                    print(fields, file=sys.stderr)
                    print(year,month,day,hour,min,sec, file=sys.stderr)
                    raise
            else:
                dt = datetime.datetime(year, month, day)
            days = int((dt.timestamp() - today.timestamp()) / (3600*24))
            if days >= 0:
                v = "%04dd+" % days
                fields.insert(i_orig,v)
            else:
                v = "%04dd" % abs(days)
                fields[i] = "over" + fields[i] #overdue!
                fields.insert(i_orig,v)
            if sortkey:
                sortkey += v
            else:
                sortkey = "Y" + v
        elif TAG_DATE.match(fields[i]):
            #creation date
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
            

