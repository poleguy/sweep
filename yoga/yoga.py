#!/usr/bin/env python3
# https://github.com/tagadvance/toggle-tablet-mode/blob/master/toggle-tablet-mode.py

# https://stackoverflow.com/questions/46169404/acpi-event-not-triggering-associated-action
# use sudo /etc/init.d/acpid reload
# and
# tail -f /var/log/syslog
# to reload and debug

import os
import re

def main() -> None:
    toggle()

def toggle():
    for id in all_ids():
        toggle_device(id)

def all_ids():
    # get all laptop control devices
    device_ids = [get_keyboard(), get_touchpad(), get_trackpoint()]
    return device_ids

def get_keyboard(device: str = 'AT Translated Set 2 keyboard'):
    meta = run('xinput --list | grep "%s"' % device)
    m = re.search('id=(\d+)', meta)
    return m.group(1)

def get_touchpad(device: str = 'Touchpad'):
    meta = run('xinput --list | grep -i "%s"' % device)
    m = re.search('id=(\d+)', meta)
    return m.group(1)

def get_trackpoint(device: str = 'TrackPoint'):
    meta = run('xinput --list | grep -i "%s"' % device)
    m = re.search('id=(\d+)', meta)
    return m.group(1)

def toggle_device(device: str) -> None:
    state = is_enabled(device)
    new_state = state ^ 1
    set_state(device, new_state)

def laptop() -> None:
    # sets yoga to laptop mode
    laptop_map_to_output()    
    for id in all_ids():
        print(f"laptop {id}")
#        with open('/tmp/log.txt','a') as f:
#            print(f"laptop {id}", file=f)
        enable(id)

def tablet() -> None:
    # sets yoga to laptop mode
    tablet_map_to_output()
    for id in all_ids():
        print(f"tablet {id}")
#        with open('/tmp/log.txt','a') as f:
#            print(f"tablet {id}", file=f)
        disable(id)

def set_state(device: str, new_state: int):
    run('xinput set-prop "%s" "Device Enabled" "%d"' % (device, new_state))

def enable(device: str):
    new_state = 1
    set_state(device, new_state)

def disable(device: str):
    new_state = 0
    set_state(device, new_state)

def is_enabled(device: str) -> int:
    meta = run('xinput list-props "%s" | grep "Device Enabled"' % device)
    m = re.search(':\s*(\d+)', meta)
    value = m.group(1)
    return int(value)

def run(command: str) -> str:
    return os.popen(command).read()


def tablet_map_to_output():
    # see touchscreen.sh
    run('bash /home/poleguy/flippy-data/bin/yoga/touchscreen-no-fingers.sh')

def laptop_map_to_output():
    # see touchscreen.sh
    run('bash /home/poleguy/flippy-data/bin/yoga/touchscreen.sh')


if __name__ == '__main__':
    print("call tablet-mode.py or laptop-mode.py")
    print("to install"
          """
# https://askubuntu.com/questions/980997/how-do-i-disable-the-touchpad-when-the-lid-is-twisted-or-closed
cat << EOF | sudo tee /etc/acpi/events/thinkpad-tablet-enabled
# /etc/acpi/events/thinkpad-tablet-enabled
# This is called when the lid is placed in tablet position on
# Lenovo ThinkPad Yoga 260 Tablet

event=video/tabletmode TBLT 0000008A 00000001 K
action=/usr/local/bin/tablet-mode
EOF
cat << EOF | sudo tee /etc/acpi/events/thinkpad-tablet-disabled
# /etc/acpi/events/thinkpad-tablet-disabled
# This is called when the lid is placed in tablet position on
# Lenovo ThinkPad Yoga 260 Tablet

event=video/tabletmode TBLT 0000008A 00000000 K
action=/usr/local/bin/laptop-mode
EOF

          """
"sudo ln -s /home/poleguy/flippy-data/bin/tablet-mode.py /usr/local/bin/tablet-mode.py"
"sudo ln -s /home/poleguy/flippy-data/bin/laptop-mode.py /usr/local/bin/laptop-mode.py"
"sudo ln -s /home/poleguy/flippy-data/bin/tablet-mode /usr/local/bin/tablet-mode"
"sudo ln -s /home/poleguy/flippy-data/bin/laptop-mode /usr/local/bin/laptop-mode"
          )

