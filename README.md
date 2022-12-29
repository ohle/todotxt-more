# todo.txt-more

This is a set of complementary extensions for todo.txt .

* `format` - Better coloured output, supports both ANSI colours as well as pango.
* `edit` - Invokes editor to edit todo.txt. 
* `show` - Show a single task based on item number
* `priup` - Priority up
* `pridown` - Priority down (up to C)
* `rofi` - Control todo.txt interactively via rofi (a menu program)
* `fzf` - Control todo.txt interactively via fzf (a terminal based fuzzy finder)
* `issue` - View and sync issues (sync with Github)
* `timetrack` - Track time on projects and contexts, and produce summary reports 
* `notmuch` - Sync with notmuch mail based on tags like 'todo' and/or 'reply' 

## Installation

Run ``make install`` to copy everything to your `~/.todo.actions.d` directory.

You will need the following dependencies to use all the extra functionality this extension set offers:

* Python 3.7 or above (the extensions are written in bash but some call additional python scripts)
* [pygithub](https://github.com/pygithub/pygithub) (Arch: `python-github`, Alpine: `py3-github3`), for `issue`
* [pytodotxt](https://vonshednob.cc/pytodotxt/) (from pypi), for `issue` and `notmuch`
* [fzf](https://github.com/junegunn/fzf) (Arch: `fzf`, Alpine: `fzf`), for `fzf`
* [rofi](https://github.com/davatorium/rofi) (Arch: `rofi` or AUR `rofi-lbonn-wayland` , Alpine: `rofi` or `rofi-wayland`), for `rofi`
* [notmuch](https://notmuchmail.org/) (Arch: `notmuch`, Alpine: `notmuch`), for `notmuch`

## Usage

Once installed, see `todo.sh help` for usage information.






