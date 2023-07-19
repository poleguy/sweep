#!/usr/bin/env python3
# stop obs virtual camera if machine is idle for more than t time
# this allows the screen to go blank
# restart obs virtual camera when machine becomes active
#
# needs:
# https://github.com/pschmitt/obs-cli
# pip install obs-cli
import time
import subprocess
import shlex

# set idle time (seconds)
t = 60*20
#t = 3 # short for testing

poll_period = 2.0
idle_periodic_reset = 30  # when do we expect obs to periodically reset the idle count?
idle_periodic_reset_low = idle_periodic_reset - 0.5 # tolerance for inaccuracy of when reset occurs
idle_periodic_reset_high = idle_periodic_reset + 0.5 # tolerance for inaccuracy of when reset occurs

idle_last = 0

# set commands

#on_idle = "obs-cli virtualcam stop --password 7D4xNRVVAkE3sHhu --port 4455 --host 192.168.1.162"
#on_active = "obs --startvirtualcam"
#on_active = "obs-cli virtualcam start --password 7D4xNRVVAkE3sHhu --port 4455 --host 192.168.1.162"
on_active = "obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 virtualcam start"
on_idle = "obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 virtualcam stop"


def set_state(cmd):
    subprocess.Popen(shlex.split(cmd))
    
def get_idle():
    return int(subprocess.check_output("xprintidle").decode("utf-8").strip())/1000



def get_idle_corrected():
    # get idle time, but ignoring any resets that occur at a 30 second period
    # because these are due to obs interrupting the idle to force the screen active
    global idle_last
#    global idle_total
    global time_start
    time_end  = time.monotonic()
    
    idle = int(subprocess.check_output("xprintidle").decode("utf-8").strip())/1000
    if idle > idle_last:
        # still idle
        pass
    elif idle_last + poll_period - idle > idle_periodic_reset_low and idle_last + poll_period - idle < idle_periodic_reset_high:
        # ignore periodic reset near 30 seconds due to obs
        pass
    else:
        # idle time went down, but not near the expected periodic reset due to obs.
        # so this is reported as a true idle reset
        time_start = time.monotonic() + idle
    idle_last = idle
    print(f'idle {idle}, idle_corrected {time_end - time_start:0.3f}')
    # return the time elapsed since we saw a non-periodic reset of the idle count
    return time_end - time_start

idle1 = 0
time_start = time.monotonic() + get_idle()

while True:
    time.sleep(poll_period)
    idle2 = get_idle_corrected()
    #idle2 = get_idle()
        
    # if idle time exceeds (passes) the limit, run one command
    if all([idle2 >= t, idle1 < t]):
        set_state(on_idle)
    # if idle time switches to below (passes) the limit, run another command
    elif all([idle2 <= t, idle1 > t]):
        set_state(on_active)
    if idle1 > idle2:
        print(f'reset at {idle1:0.3f}')
    #print(idle1, idle2)
    idle1 = idle2

