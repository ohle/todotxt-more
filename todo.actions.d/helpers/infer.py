#!/usr/bin/env python3
import sys
import json
#maps projects to tags/contexts/projects, these will be added in addition to the project (rather than replacing it)
#example: { "frog": ["@work","@huc","@clariah","+wp3t139"] }
INFER_FROM_PROJECT = {}

with open(sys.argv[1],'r',encoding='utf-8') as f:
    INFER_FROM_PROJECT = json.load(f)

taskline = " ".join(sys.argv[2:])

projects = [ x for x in taskline.split(" ") if x and x[0] == '+' ]
for project in projects:
    project = project[1:]
    if project in INFER_FROM_PROJECT:
        for tag in INFER_FROM_PROJECT[project]:
            if taskline.find(tag) == -1:
                taskline += f" {tag}"

print(taskline)
