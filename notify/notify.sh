#!/bin/bash

# This script is meant to be sourced in your terminal
# Usage: source notify.sh

# Save the current terminal's window ID
MY_WIN_ID=$(xdotool getwindowfocus)

# Hook to run after each command
function notify_if_inactive() {
    local EXIT_STATUS=$?
    local CURRENT_WIN_ID
    CURRENT_WIN_ID=$(xdotool getwindowfocus)

    if [[ "$MY_WIN_ID" != "$CURRENT_WIN_ID" ]]; then
        espeak "Command completed in background terminal"
    fi
}

# Install the hook
trap notify_if_inactive DEBUG
