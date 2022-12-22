#!/usr/bin/env python3

import sys
import os
import re
import pytodotxt
from github import Github



LABEL_MAP = {
    #from github -> to todo.txt
    "feature": "feat",
    "enhancement": "feat"
}

INFER_FROM_PROJECT = {
    "folia": ["@work","@huc","@clariah","+wp3t108"],
    "foliatools": ["@work","@huc","@clariah", "+wp3t108"],
    "foliautils": ["@work","@huc","@clariah","+wp3t108"],
    "flat": ["@work","@huc","@clariah","+wp3t062"],
    "clam": ["@work","@huc","@clariah","+wp3t142"],
    "frog": ["@work","@huc","@clariah","+wp3t139"],
    "deepfrog": ["@work","@huc","@clariah","+wp3t139"],
    "ucto": ["@work","@huc","@clariah","+wp3t139"],
    "lamachine": ["@work","@huc","@clariah","+wp3t098"],
    "codemetapy": ["@work","@huc","@clariah","+wp2tooldiscovery"],
    "codemetaharvester": ["@work","@huc","@clariah","+wp2tooldiscovery"],
    "codemetaserver": ["@work","@huc","@clariah","+wp2tooldiscovery"],
    "stam": ["@work","@huc","+clariah","+wp2annotation"],
}


TAG_RE = re.compile(r'(\s+|^)#([^\s]+)')

def infer_from_project(task: pytodotxt.Task):
    """Infer additional tags based on the project"""
    for project in task.projects:
        if project in INFER_FROM_PROJECT:
            for tag in INFER_FROM_PROJECT[project]:
                if str(task).find(tag) == -1:
                    task.append(tag)
    

def update_task_with_github_issue(task: pytodotxt.Task, issue):
    if issue.state == "open" and task.is_completed:
        #reopen locally
        task.is_completed = False
        print("Reopening: ", task, file=sys.stderr)
    elif issue.state != "open" and not task.is_completed:
        #close locally
        task.is_completed = True
        print("Closing: ", task, file=sys.stderr)

    updated = issue.updated_at.strftime("%Y-%m-%d")
    if 'updated' in task.attributes and task.attributes['updated'] != [updated]:
        task.remove_attribute('updated')
        task.add_attribute('updated', updated)
    elif 'updated' not in task.attributes:
        task.add_attribute('updated', updated)

    #sync labels
    foundlabels = set()
    tags = [ m.group(0).strip(' #') for m in task.parse_tags(TAG_RE) ]
    for label in issue.labels:
        label = fmtlabel(label.name)
        foundlabels.add(label)
        if label not in tags:
            task.append("#" + label)

    for label in tags:
        if label not in foundlabels: 
            task.remove_tag(label, TAG_RE)


def fmtlabel(label: str) -> str:
    label = fmt(label)
    if label in LABEL_MAP:
        return LABEL_MAP[label]
    else:
        return label

def fmt(s: str) -> str:
    """Formatter for projects/tags"""
    return "".join(c for c in s if c.isalnum()).lower()

todo = pytodotxt.TodoTxt(os.path.expanduser("~/todo.txt"))
todo.parse()

gh = Github(os.environ['GITHUB_TOKEN'])
ghuser = gh.get_user()

ghissues = {}
for issue in ghuser.get_user_issues():
    ghissues[issue.html_url] = issue

ghissues_found = set()
ghissues_notfound = set()

for task in todo.tasks:
    if 'issue:https' in task.attributes: #bug in pytodotxt, https is interpeted as part of the key rather than value
        for url in task.attributes['issue:https']:
            url = "https:" + url
            if url in ghissues:
                print("Matched issue ", url, file=sys.stderr)
                issue = ghissues[url]
                ghissues_found.add(url)
                update_task_with_github_issue(task, issue)
            else:
                print("Unable to match issue ", url, file=sys.stderr)
                ghissues_notfound.add(url)

for url, issue in ghissues.items():
    if url not in ghissues_found:
        taskline = ""
        if issue.state != "open":
            taskline += "x "
        taskline += f"+{fmt(issue.repository.name)}"
        for label in issue.labels:
            taskline += f" #{fmtlabel(label.name)}"
        created = issue.created_at.strftime("%Y-%m-%d")
        updated = issue.updated_at.strftime("%Y-%m-%d")
        taskline += f" {issue.title} issue:{issue.html_url} created:{created} updated:{updated}"
        task = pytodotxt.Task(taskline)
        infer_from_project(task)
        todo.add(task)
        print("Added: ", task, file=sys.stderr)

#pytodotxt stumbles over symlinks (overwriting them with a new file rather than following them), so we do it this way:
todo.save(target="/tmp/todo.txt", safe=False)
with open("/tmp/todo.txt","r",encoding="utf-8") as f_in:
    with open(os.path.expanduser("~/todo.txt") ,"w+",encoding="utf-8") as f_out:
        f_out.write(f_in.read())



