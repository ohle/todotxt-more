# todo.txt-more

Forked from https://git.sr.ht/~proycon/todotxt-more

## Introduction

This is a set of complementary extensions for todo.txt .

* `more` -  Main entry point, shortcut invoking various underlying plugins. By default displays a list with better sorting (`relsort`) and colour highlighting (`format`)
* `edit` - Invokes editor to edit todo.txt. 
* `show` - Show a single task based on item number
* `priup` - Priority up
* `pridown` - Priority down (down to C, depriotitised after)
* `rofi` - Control todo.txt interactively via rofi (a menu program)
* `fzf` - Control todo.txt interactively via fzf (a terminal based fuzzy finder)
* `issue` - View and sync issues (sync with Github)
* `timetrack` - Track time on projects and contexts, and produce summary reports 
* `notmuch` - Sync with notmuch mail based on tags like 'todo' and/or 'reply' 
* `cal` - Import iCalendar/vCalendar (ics) files
* `autoprio` - Automatically assign priorities (mostly based on due dates) 
 
The following are usually not called directly:

* `format` - Better coloured output, supports ANSI colours, pango, and html
* `relsort` -  Better sorting with relative dates
* `actionmenu` - The menu used in the fzf and rofi interfaces. 

## Installation

Run ``make install`` to copy everything to your `~/.todo.actions.d` directory.

You will need the following dependencies to use all the extra functionality this extension offers:

* [todo.txt-cli](https://github.com/todotxt/todo.txt-cli) - The base todo.txt CLI interface, this provides `todo.sh`. (AUR: `todotxt`, Alpine: `todo.txt-cli`, Debian: `todotxt-cli`, Homebrew: `todo.txt`)
* Python 3.7 or above (the extensions are written in bash but some call additional python scripts)
* [pygithub](https://github.com/pygithub/pygithub) (Arch: `python-github`, Alpine: `py3-github3`, pypi: `pygithub`)
* [pytodotxt](https://vonshednob.cc/pytodotxt/) (pypi: `pytodotxt`)
* [fzf](https://github.com/junegunn/fzf) (Arch/Alpine/Debian/Homebrew: `fzf`)
* [rofi](https://github.com/davatorium/rofi) (Arch/Debian/Alpino: `rofi`, alterantive AUR `rofi-lbonn-wayland` , Alpine: `rofi-wayland`)
* [notmuch](https://notmuchmail.org/) (Arch/Alpine/Debian/Homebrew: `notmuch`)

You can run `make pythondeps` to install the python dependencies locally (uses ``pip install --user``).

## Usage & Workflow

This extension set assumes you make use of priorities A, B and C only (and D as a special category). I use them as follows in a kind of kanban-style:

* *(A)* for tasks to do on today
* *(B)* for tasks to do later this week
* *(C)* for tasks after this week (limited)
* *(D)* for tasks that are temporarily blocked/waiting on hold
* Tasks without a priority are the backlog 

At any time, there should only be a limited number of items carrying a priority, and it should be easy to increase/decrease priority of a task via either `priup`/`pridown`, or interactively using the `rofi` or `fzf` interfaces.

To display your tasks non-interactively, we recommend you use `todo.sh more` (short for `todo.sh more list`) rather than the traditional `todo.sh list`; `todo.sh more` redefines several built-in commands. A quick recommended way to use this from your shell is to set an alias `t="todo.sh more"`, you can then do `t list` (or just `t` as a shortcut),`t add`,`t done` etc... All the regular commands as well as the extensions should be available.

Todo.txt-more will invoke the `format` and `relsort` extensions to do better colour highlighting and better relative sorting. You can pass any actions you also pass to `todo.sh`. Here is an example:

![todo.sh more list](doc/morelist.png)


You can note the following in this example:

* todo.txt-more adds hashtags (starting with #) and will colour them differently (`todo.sh format`), context (`@`) and projects (`+`) will also get a distinctive colour.
* tasks with priority will always be shown before any items without priority (`todo.sh relsort`)
* tasks with a creation date will be shown using their relative date in days (e.g. 6d) , and sorted accordingly.
    * though not shown in this example, tasks with a due date (`due:` attribute) will be shown using their relative date in days (e.g. 6d+), and sorted accordingly, this takes precedence over creation date.
* you see tasks synced from the GitHub (issue) and from my mail (notmuch), more about this later...


Between the `more` and `lists` actions, you can inject the format you want for the output and the colouring.

* `ansi` - ANSI escape sequences, good for terminals, this is the default
* `pango` - Pango markup, good when used with GUI applications like rofi, dmenu with pango patch, [wayout](https://git.sr.ht/~proycon/wayout)
* `html` - HTML, good for exporting to the web
* `markdown` - Markdown syntax 
* `slack` - Slack's butchered version of markdown syntax, good for pasting into Slack.

You might, however, prefer a more interactive view that allows you to do fuzzy search and makes the tasks directly actionable.
If you run `todo.sh fzf list @work`, you'd the see same view as the static one, but interactively using fzf:

![todo.sh more list](doc/fzf.png)

Or run `todo.sh rofi list @work`, for the same thing in rofi, which opens a graphical menu. This is great to tie to a keybinding in your (tiling?) window manager: 

![todo.sh rofi list](doc/rofi.png)

Note that your rofi may look different depending on the theme you are using.

The rofi method binds some shortcuts keys for quick actions like prioritisation and editing. Moreover, you can directly add new entries with rofi by just typing the full task entry in the search field and pressing enter. For existing items, once you select an item in either rofi or fzf, you're presented with an action menu (`todo.sh actionmenu`)

![action menu](doc/actionmenu.png)

## Notifications

You can enable feedback via your notification daemon (via `notify-send`) by setting environment variable `TODOTXT_NOTIFY=1`. If set, you will get feedback notifications on various actions.

### Issue syncing

If you use Github extensively, its issue tracker is likely an important source of information for your todo tasks. However, it's cumbersome to have issues separate from your todo.txt and effectively have two systems you need to check. The `issue` extension should solve this problem. Its job is to sync issues (including pull requests) from github with your todo.txt. It will sync *all issues assigned to you*. 

The sync works as follows:

* All tasks that are issues are marked with `issue:` and the *full path* to the issue.
* A sync is done by calling `todo.sh issue sync`, in order for this to work you need to have the environment variable `$GITHUB_TOKEN` set to a Github API token.
* Any github issue that is *assigned to you* and not yet in `todo.txt` or `done.txt` will be added (without prioritisation)
* The Github repository name is translated to a project name (e.g `proycon/codemeta-harvester` becomes `+codemetaharvester`, punctuation etc is stripped and all is lowercased) and will be shown at the beginning of the task line.
* The `todo.txt` contains just the issue title, its labels, project, not the body or comments. The rofi and fzf extensions offer an easy way to inspect an issue in the browser.
* If you close a task that is also a github issue via the action menu in rofi/fzf or via `task.sh issue done`, an API call will go out to GitHub to close the issue.
* Projects may also translate to further projects or contexts, you can customize this in a JSON file and pass the JSON filename in environment variable `$TODO_ISSUE_INFERMAP`. Example:

```json
{
    "codemetapy": ["@work","@huc","@clariah","+wp2tooldiscovery"],
    "codemetaharvester": ["@work","@huc","@clariah","+wp2tooldiscovery"],
    "codemetaserver": ["@work","@huc","@clariah","+wp2tooldiscovery"],
}
```

These will all be appended to the end.

* Github labels will be added as hashtags immediately after the project name.
You can optionally translate these through another map defined in a JSON file and filename in `$TODO_ISSUE_LABELMAP`. Example:

```json
{
    "feature": "feat",
    "enhancement": "feat"
}
```

* Tasks will have a creation date corresponding to the creation data of the issue.
* An extra `updated:`  attribute is added with the last updated time. This is updated on sync.

There are a few limitations to be aware of:

* The task description/issue subject is synced from github to task.txt only once, editing it in either has no effect on the other.
* When Github labels change, they will be synced back to todo.txt (but will appear at the end when they're new). You can't sync hashtags to github labels the other way round.
* When an issue is closed and reopened, it won't be detected in the sync

### Mail syncing

Another common source of todo tasks is email. I often receive mails that require some kind of follow-up action, or that I simply have to reply to. I am using [notmuch](https://notmuchmail.org) as a means to add tags to my mail and make it quickly searchable. I use a *reply* tag for mail I still have to reply to, and *todo* for mail that requires another follow-up actions. Of course, I want both in my `todo.txt` so I have everything in one place again. 


The `todo.txt notmuch` extension syncs with your notmuch database. It runs a query (defined in environment variable `$TODOTXT_NOTMUCH_SEARCH`, which defaults to `tag:todo or tag:reply` fitting my own use-case) and adds all threads it finds to `todo.txt`. It is a one-way sync. Synced mails receive the context `@mail` and the notmuch tag translates to a hashtag. Any further mappings between notmuch tags and todo.txt can be configured in a JSON file, filename stored in `$TODOTXT_NOTMUCH_MAP`. Example:

```json
{
    "work": ["@work"],
    "personal": ["@hobby"],
    "sxmo": ["+sxmo", "@hobby"],
    "folia": ["+folia","@huc","@work"]
}
```

Results when listing may look as follows:

```
$ todo.sh more list @mail
221 (C) 7d @mail #reply Frog voor MacOS notmuch:00000000000268a8 +frog @huc @work
225 (C) 13d @mail #reply [PATCH sxmo-utils] Drop busybox aliases notmuch:000000000001a40a +sxmo @hobby
```

Referenced notmuch threads can be viewed in your mail client (configured via `$TODOXT_NOTMUCH_MAILCMD`, set to neomutt by default):

```
$ todo.sh notmuch view 225
```

You can also mark a task as done via the notmuch extension, which will take care of removing the notmuch tags for you as well (configured via `$TODOTXT_NOTMUCH_UNTAG`).

```
$ todo.sh notmuch done 225
```

Of course all this is also available via the action menu offered by the rofi/fzf interfaces.

### Time tracking

Employers often require you to track your working hours, especially if you are working on a variety of distinct projects. Keeping track of this manually is a waste of time. If you have your `todo.txt` workflow in place, we can simply take advantage of this for tracking time as well. This is done using `todo.txt timetrack` and it can be invoked interactively via the action menu as presented by fzf or rofi. When you say *start task* a simply eentry of the full task line, prepended with the current date and time, is registered to a file `timetrack.txt` that lives alongside your `todo.txt` and `done.txt`. Only one task can be tracked at any given time (people suck at multitasking anyway, so better not pretend you can do it). When you start a new task the previous one ends. There is also `todo.sh timetrack stop` to stop tracking, which will simply register an *idle* entry in `timetrack.txt`. I recommend to automatically trigger this action when your screensaver/screenlock kicks in so you don't have to worry about it. The tracking will also be stopped automatically if you mark the currently tracked task as done via `todo.sh more done` or fzf/rofi.

To see the task you are currently working on, run `todo.sh timetrack current`. This may be worth adding to whatever bar (waybar/polybar/dwm's bar/etc) you use so you can see it at all times.

```
$ todo.sh timetrack current -d                  
1h13m +todotxtmore implement timetrack summary options @hobby
```

The `timetrack.txt` log can be visualised with `todo.sh timetrack log`, it optionally takes a start date and an end date (non-inclusive) as parameters (YYYY-MM-DD). Add the `-d` option if you want to have relative time (durations), use `-s` instead if you want it in raw seconds, these are also available for `timetrack current` as shown above.

Using `todo.sh timetrack daysummary` you can get a summary of total time spent, per day, on specific contexts or projects. It aggregates for each day all projects (``+``) and contexts (`@`) mentioned in the log.

Example output:

```
$ todo.sh timetrack daysummary 2022-12-29
2022-12-29 Thu 8h52m @hobby
2022-12-29 Thu 4h8m +todotxtmore
2022-12-29 Thu 14m @generic
2022-12-29 Thu 14m @entertainment
```

Be aware that the contexts and projects used in aggregation are not mutually exclusive. You can use any combination you want.

Similarly, there is a `weeksummary` and `monthsummary` that aggregates per week/month. You may add the `-all` parameter to see individual tasks again (rather than just contexts and projects).

### Calendar

There is a fair degree of overlap between todo lists and calendars, even though they are distinct perspectives on your time planning. Todo.txt traditionally caters towards todo lists  and not calendars, due dates are not in the initial design but can be easily using a `due` attribute, as many other implementations also do. Todo.txt-more follows this convention and takes `due` dates into account when sorting (`relsort`) and highlighting.

This opens up the road to expressing calendar items in `todo.txt`. The `cal` extension allows importing iCalendar (ics) format via `todo.sh cal import`. 

Similarly, you can export todo items to iCalendar format using `todo.sh cal export`.

The `cal` extension also has some specific visualisations via `todo.sh cal list`:

![todo.sh cal list](doc/callist.png)

Add the ``--headers`` parameter for a more verbose view grouped per day.

![todo.sh cal list --headers](doc/callistheaders.png)

The latter is also what you get if you just run `todo.sh cal` without further arguments.

### Further usage

Once installed, see `todo.sh help` for complete usage information:

```
  Add-on Actions:
  Action menu:
    actionmenu
      Shows or processing items for the action menu, not meant to be used directly
    actionmenu [action] [itemno] [-d]
      Run the action on the item number. Add -d (at the end) to act on done.txt

  Auto prioritisation:
    autoprio
      automatically assign priorities where possible

  calendar support:
    cal import [filename]
      imports an ics file. Takes care not to import duplicates. filename may also be - for stdin
    cal export [itemno] ..
      export the specified item numbers to ics (to stdout)
    cal list [[--headers|-H]
      list all calendar items, add --headers to output headers (ansi colours only)
    cal
      shortcut for cal list --headers

  Edit:
    edit [[itemno]]
      Edit the specified item in the default editor
    edit
      Open todo.txt in the editor

  Format/recolor output:
    format [ansi|pango|html|markdown|slack] [ACTIONS]
      run command and recolor using ansi, pango, html, markdown, or slack's markdown variant
    format [ansi|pango|html|markdown|slack] stdin
      reads from standard input

  Fuzzy search:
    fzf [ACTIONS]
      pass list actions through fzf and make them actionable

  Handle linked issues:
    issue [[-d]] [itemno]
      view the issue referenced in the item (if any). Add -d to search in done tasks
    issue sync
      sync issues from remote
    issue close|done [itemno] ...
      close the reference issue (and mark the item as a whole as done)

  Shortcut redefining various default actions:
    more [[ansi|pango|html|markdown]] list|ls|listall|listcon|listpri|listproj
      Shortcut to show the list with relative dates, sorting and better colour h8ighlighting (can be used with any list action)
    more done [itemno]
      Marks an item number as done, takes care of closing the issue or untagging the mail as well
    more view [itemno] [[-d]]
      View related data (issue/mail). Set the -d parameter to search in done.txt
    more sync
      Run sync on extensions that are syncable

  Handle linked mails:
    notmuch sync
      sync notmuch mails by query: tag:todo or tag:reply
    notmuch done [itemno]
      mark the task and the corresponding mail as done (-todo -reply -inbox)
    notmuch view [-d] [itemno]
      view the referenced thread in your mail client. Add -d to search in done tasks

  Priority changing:
    pridown [itemno]
      Decreases the priority of the item number, deprioritize after C

  Priority changing:
    priup [itemno]
      Increase the priority of the item number, unprioritized becomes C

  Show task by item number:
    relsort [actions]
      Convert completion dates into relative time (=days) compared to now and sort accordingly

  Fuzzy search:
    rofi [ACTIONS]
      pass actions through rofi and make them actionable

  Show task by item number:
    show [[-d]] [itemno]
      show the task on the specified line. Add -d to search in done tasks

  Timetrack output:
    timetrack start [itemno|item]
      Start tracking item (stops tracking previous one)
    timetrack stop
      Stop tracking
    timetrack current [-t]
      Show currently tracked task and the time it was started
      -t - hide the time
      -d - show relative time
      -s - show relative time in seconds
    timetrack log [[options]] [[fromdatetime]] [[todatetime]]
      Shows the timetrack log for the given time period
      (Datetime is in Y-m-d H:M:S format, time component may be omitted)
      Options:
      -d - show relative time deltas
      -s - show relative time deltas in seconds
      Note: todatetime is non-inclusive
    timetrack summary [[options]] [[fromdatetime]] [[todatetime]]
      Shows a time spent summary, over the specified period
      (Datetime is in Y-m-d H:M:S format, time component may be omitted)
      Options:
      -a|--all - show all tasks, not only aggregates
      Note: todatetime is non-inclusive
    timetrack daysummary [[options]] [[fromdatetime]] [[days]]
      Shows a time spent summary, aggregated per day, over the specified period
      (Datetime is in Y-m-d H:M:S format, time component may be omitted)
      Note: days is the number of days, inclusive
    timetrack weeksummary [[options]] [[fromdatetime]] [[weeks]]
      Shows a time spent summary, aggregated per week, over the specified period
      (fromdatetime is in Y-m-d format and should be a monday that starts the week)
      Note: weeks is the number of weeks, inclusive
    timetrack monthsummary [[options]] [year...]
      Shows a time spent summary, aggregated per month, over the specified years

```

## Contribute

If you want to contribute, you can send patches to my [public inbox](mailto:~proycon/public-inbox@lists.sr.ht). Read about [the git e-mail workflow](https://git-send-email.io/) if you are not yet familiar with it.

The code is currently in a fairly early stage of development and needs further testing and cleanup.
