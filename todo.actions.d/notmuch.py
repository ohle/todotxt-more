#!/usr/bin/env python3

import sys
import argparse
import json
import datetime
from itertools import chain
import pytodotxt

parser = argparse.ArgumentParser(description="Notmuch syncer, reads 'notmuch search --format=json' output from stdin", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--todo','-t',type=str, help="todo.txt file", action='store', required=True)
parser.add_argument('--done','-d',type=str, help="done.txt file", action='store', required=True)
parser.add_argument('--tagmap','-m',type=str, help="notmuch tag to todo.txt tag map (json)", action='store', required=False)
parser.add_argument('--lowprio',type=str, help="notmuch tag used for low priority", action='store', required=False,default="lowpriority")
parser.add_argument('--highprio',type=str, help="notmuch tag used for high priority", action='store', required=False,default="priority")
args = parser.parse_args() #parsed arguments can be accessed as attributes

TODO_FILE = args.todo
DONE_FILE = args.done


tagmap = {}
if args.tagmap:
    with open(args.tagmap,'r',encoding="utf-8") as f:
        tagmap = json.load(f)

todo = pytodotxt.TodoTxt(TODO_FILE)
todo.parse()

done = pytodotxt.TodoTxt(DONE_FILE)
done.parse()

notmuch_found = set()

threads = json.load(sys.stdin)
threads = { thread['thread']: thread for thread in threads }

for task in chain(todo.tasks,done.tasks):
    if 'notmuch:' in task.attributes: #bug in pytodotxt, https is interpeted as part of the key rather than value
        thread_id = task.attributes['notmuch']
        notmuch_found.add(thread_id)
        if thread_id not in threads:
            print("No longer tagged todo/reply in notmuch, marking as completed: ", task)
            task.is_completed = True
    
for thread_id, thread in threads.items():
    if thread_id not in notmuch_found:
        created = datetime.datetime.fromtimestamp(thread['timestamp']).strftime("%Y-%m-%d")
        taskline = ""
        if args.highprio in thread['tags']:
            taskline = "(A) "
        elif args.lowprio not in thread['tags']:
            taskline = "(C) "
        taskline += f"{created} @mail"

        if 'reply' in thread['tags']:
            taskline += " #reply"
        taskline += " " + thread['subject'] 
        taskline += f" notmuch:{thread_id}"
        for tag in thread['tags']:
            if tag in tagmap:
                for xtag in tagmap[tag]:
                    taskline += f" {xtag}"
        task = pytodotxt.Task(taskline)
        print(task)


#pytodotxt stumbles over symlinks (overwriting them with a new file rather than following them), so we do it this way:
todo.save(target="/tmp/todo.txt", safe=False)
with open("/tmp/todo.txt","r",encoding="utf-8") as f_in:
    with open(TODO_FILE,"w+",encoding="utf-8") as f_out:
        f_out.write(f_in.read())

done.save(target="/tmp/done.txt", safe=False)
with open("/tmp/done.txt","r",encoding="utf-8") as f_in:
    with open(DONE_FILE ,"w+",encoding="utf-8") as f_out:
        f_out.write(f_in.read())

