#!/usr/bin/bash
# https://askubuntu.com/questions/980997/how-do-i-disable-the-touchpad-when-the-lid-is-twisted-or-closed
cat << EOF | sudo tee /etc/acpi/events/thinkpad-tablet-enabled
# /etc/acpi/events/thinkpad-tablet-enabled
# This is called when the lid is placed in tablet position on
# Lenovo ThinkPad Yoga 260 Tablet

event=video/tabletmode TBLT 0000008A 00000001 K
action=/usr/local/bin/tablet-mode.py
EOF

cat << EOF | sudo tee /etc/acpi/events/thinkpad-tablet-disabled
# /etc/acpi/events/thinkpad-tablet-disabled
# This is called when the lid is placed in tablet position on
# Lenovo ThinkPad Yoga 260 Tablet

event=video/tabletmode TBLT 0000008A 00000000 K
action=/usr/local/bin/laptop-mode.py
EOF

sudo ln -s /home/poleguy/flippy-data/bin/tablet-mode.py /usr/local/bin/tablet-mode.py

sudo ln -s /home/poleguy/flippy-data/bin/laptop-mode.py /usr/local/bin/laptop-mode.py

