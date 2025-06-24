#!/bin/bash
# add source notify.sh to ~/.bashrc

# uses:
# https://github.com/rcaloras/bash-preexec
# inspired by:
# https://github.com/dschep/ntfy/blob/master/ntfy/shell_integration/auto-ntfy-done.sh
# but doesn't screw up $HISTCONTROL


# This script is meant to be sourced in your terminal
# Usage: source notify.sh

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Source a file from within the same directory
source "$SCRIPT_DIR/bash-preexec.sh"

# Save the current terminal window ID only once per shell session
if [[ -z "$MY_TERM_WIN_ID" ]]; then
    MY_TERM_WIN_ID=$(xdotool getwindowfocus)
    #echo "set MY_TERM_WIN_ID"
fi

#preexec() { echo "just typed $1";}
precmd() { #echo "printing the prompt";

function notify_if_inactive() {
    local exit_status=$?
    local active_win_id
    active_win_id=$(xdotool getwindowfocus)
    #echo "notify_if_inactive"
    if [[ "$MY_TERM_WIN_ID" != "$active_win_id" ]]; then
        echo "command completed in background window"
        espeak "command complete"
    fi
    return $exit_status
}

notify_if_inactive

}

