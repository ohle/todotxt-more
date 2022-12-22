#!/bin/bash

#install this in the .todo.actions.d folder of your todo.txt CLI install.

action=$1
shift

[ "$action" = "usage" ] && {
  echo "  Recently comlpeted tasks:"
  echo "    show [linenr]"
  echo "      show the task on the specified line."
  echo "    showdone [linenr]"
  echo "      show the completed task on the specified line."
  echo ""
  exit
}

[ "$action" = "show" ] && {
    while [ "$#" -gt 0 ] ; do
        item=$1
        sed -n "${item}p" "$TODO_FILE" 
    done
}

[ "$action" = "showdone" ] && {
    while [ "$#" -gt 0 ] ; do
        item=$1
        sed -n "${item}p" "$DONE_FILE" 
    done
}
