#!/usr/bin/env python3

import sys
import argparse
from itertools import chain
import datetime
import pytodotxt
from ics import Calendar, Event, Todo

parser = argparse.ArgumentParser(description="iCalendar exporter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--todo','-t',type=str, help="todo.txt file", action='store', required=True)
parser.add_argument('itemno', nargs='+')
args = parser.parse_args() #parsed arguments can be accessed as attributes

args.itemno = [ int(x) for x in args.itemno ]


TODO_FILE = args.todo

todo = pytodotxt.TodoTxt(TODO_FILE)
todo.parse()



cal = Calendar(creator="todo.txt-more")
for task in todo.tasks:
    assert( isinstance(task, pytodotxt.Task) )
    itemno = task.linenr + 1
    if itemno in args.itemno:
        if 'due' in task.attributes and '@calendar' in task.contexts:
            duedate: str = task.attributes['due'][0]
            e = Event()
        else:
            duedate = None
            e = Todo()
        e.name = task.bare_description()
        if 'end' in task.attributes:
            e.end = task.attributes['end'][0]
        else:
            e.end = duedate
        if duedate and len(duedate) > 10:
            e.begin = duedate
        elif duedate and isinstance(e, Event):
            e.begin = duedate + " 00:00:00"
            e.make_all_day()
        if isinstance(e, Event):
            cal.events.add(e)
        elif isinstance(e, Todo):
            cal.todos.add(e)

print(cal.serialize())

