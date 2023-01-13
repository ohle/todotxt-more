#!/usr/bin/env python3

import sys
import argparse
from itertools import chain
import datetime
import pytodotxt
from ics import Calendar, Event, Todo

parser = argparse.ArgumentParser(description="iCalendar importer/syncer. Reads ics data from stdin", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--todo','-t',type=str, help="todo.txt file", action='store', required=True)
parser.add_argument('--done','-d',type=str, help="done.txt file", action='store', required=True)
args = parser.parse_args() #parsed arguments can be accessed as attributes


TODO_FILE = args.todo
DONE_FILE = args.done

todo = pytodotxt.TodoTxt(TODO_FILE)
todo.parse()

done = pytodotxt.TodoTxt(DONE_FILE)
done.parse()

found = set()
for task in chain(todo.tasks,done.tasks):
    if 'ics' in task.attributes:
        found.add(task.attributes['ics'][0])

changed = False
errcode = 1
cal = Calendar(sys.stdin.read())
for event in chain(cal.events, cal.todos):
    if event.uid and event.uid in found:
        print(f"Skipping existing UID {event.uid}")
        errcode = 2
        continue

    taskline = ""
    if isinstance(event, Event) and event.all_day:
        begin = event.begin.format("YYYY-MM-DD")
        taskline += f"@calendar due:{begin}"
    elif event.begin:
        begin = event.begin.format("YYYY-MM-DDTHH:mm:ss")
        taskline += f"@calendar due:{begin}"
    elif isinstance(event, Todo) and event.dtstamp:
        created = event.begin.format("YYYY-MM-DD")
        taskline += f"{created} "

    if event.name:
        taskline += " " + event.name
    else:
        print("Event has no summary, skipping", file=sys.stderr)
        continue
    if event.location:
        taskline += f" location:{event.location}"
    if event.url:
        taskline += f" url:{event.url}"
    if isinstance(event, Event) and event.end:
        end = event.end.format("YYYY-MM-DDTHH:mm:ss")
        taskline += f" end:{end}"
    if isinstance(event, Event) and event.categories:
        for category in event.categories:
            taskline += f" #{category}"
    if event.uid:
        taskline += f" ics:{event.uid}"
    if event.description:
        taskline += " :: " + event.description.replace("\n"," ")
    taskline = taskline.strip()
    task = pytodotxt.Task(taskline)
    todo.add(task)
    changed = True
    print("Added: ", taskline, file=sys.stderr)

#pytodotxt stumbles over symlinks (overwriting them with a new file rather than following them), so we do it this way:
if changed:
    todo.save(target="/tmp/todo.txt", safe=False)
    with open("/tmp/todo.txt","r",encoding="utf-8") as f_in:
        with open(TODO_FILE,"w+",encoding="utf-8") as f_out:
            f_out.write(f_in.read())
    sys.exit(0)
else:
    sys.exit(errcode)
