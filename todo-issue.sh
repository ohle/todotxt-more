#!/bin/bash

#install this in the .todo.actions.d folder of your todo.txt CLI install.

action=$1
shift

[ -z "$OPEN_ISSUE_URL" ] && OPEN_ISSUE_URL=xdg-open

[ "$action" = "usage" ] && {
  echo "  Handle linked issues:"
  echo "    issue [itemno]"
  echo "      view the issue (if any)"
  echo "    doneissue [itemno]"
  echo "      view the closed issue (if any)"
  echo ""
  exit
}

[ "$action" = "issue" ] && {
    item=$1
    url=$(sed -n "${item}p" "$TODO_FILE" | grep -P "issue:http[^[:blank:]]+")
    $OPEN_ISSUE_URL "$url"
}

[ "$action" = "doneissue" ] && {
    item=$1
    url=$(sed -n "${item}p" "$DONE_FILE" | grep -P "issue:http[^[:blank:]]+")
    $OPEN_ISSUE_URL "$url"
}
