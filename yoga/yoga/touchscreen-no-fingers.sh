#! /usr/bin/bash
# maps touchscreen to laptop screen only
# disables finger usage
# https://github.com/poleguy/sweep/edit/master/xubuntu.md
# https://github.com/poleguy/classical

export DISPLAY=:0
export XAUTHORITY=/home/poleguy/.Xauthority

# https://www.reddit.com/r/i3wm/comments/h8i0nm/touchscreen_issues_when_using_second_monitor/
#date >> /tmp/log.txt

xrandr --query
#echo "query" >> /tmp/log.txt

# note these changed from eDP-1 to eDP1 at some point and this broke
# it later changed back and broke again
#xinput map-to-output 9 eDP1
#xinput map-to-output 9 eDP-1
xinput map-to-output "Wacom Pen and multitouch sensor Finger touch" eDP-1
xinput map-to-output "Wacom Pen and multitouch sensor Pen stylus" eDP-1
#echo "map 9" >> /tmp/log.txt
xinput map-to-output "Wacom Pen and multitouch sensor Pen eraser" eDP-1
#xinput map-to-output 10 eDP1
#xinput map-to-output 10 eDP-1
#echo "map 10" >> /tmp/log.txt

# https://askubuntu.com/questions/65951/how-to-disable-the-touchpad
xinput --disable "Wacom Pen and multitouch sensor Finger touch"



# added to ~/.profile
# better in /etc/X11/Xsession.d/50-touchscreen
# even better in /etc/udev/rules.d/50-touchscreen.rules

# https://askubuntu.com/questions/79195/where-do-i-have-to-paste-an-xinput-command-so-that-it-executes-it-when-gnome-i
