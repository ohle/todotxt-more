#!/usr/bin/env python3

import sys
import pytodotxt
import datetime

TODO_FILE = sys.argv[1]
changed = False
todo = pytodotxt.TodoTxt(TODO_FILE)
todo.parse()

TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
TOMORROW = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
TWODAYS = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

for task in todo.tasks:
    assert isinstance(task, pytodotxt.Task)
    if 'due' in task.attributes:
        field = task.attributes['due'][0]
        if field.startswith(TODAY):
            task.priority = "A"
            changed = True
        elif field.startswith(TOMORROW):
            task.priority = "B"
            changed = True
        elif field.startswith(TWODAYS):
            task.priority = "C"
            changed = True


if changed:
#pytodotxt stumbles over symlinks (overwriting them with a new file rather than following them), so we do it this way:
    todo.save(target="/tmp/todo.txt", safe=False)
    with open("/tmp/todo.txt","r",encoding="utf-8") as f_in:
        with open(TODO_FILE,"w+",encoding="utf-8") as f_out:
            f_out.write(f_in.read())
