#!/usr/bin/env python3
import asyncio
import time
#from evdev import InputDevice, categorize, ecodes
import evdev
import subprocess
# https://python-evdev.readthedocs.io/en/latest/tutorial.html

dev =evdev.InputDevice('/dev/input/by-id/usb-0c45_USB_Keyboard-event-kbd')
dev2 = evdev.InputDevice('/dev/input/by-id/usb-0c45_USB_Keyboard-event-if01')

# needed to do this in python to prevent glitch characters in terminal when using
# input-remapper-gtk

with dev.grab_context():
    # to stop calculator functionality.
    
    with dev2.grab_context():

        async def print_events(device):
            async for event in device.async_read_loop():
                #print(device.path, evdev.categorize(event), sep=': ')
                #print(event)

                if event.type == evdev.ecodes.EV_KEY:
                    key = evdev.categorize(event)
                    if key.keystate == key.key_down:
                        print(key.keycode)
                        if key.keycode == 'KEY_ESC':
                            print("Hello, world! ESC")
                            subprocess.Popen("/home/poleguy/.local/bin/hotkey-teams")
                        if key.keycode == 'KEY_CALC':
                            print("Hello, world!")
                            subprocess.Popen("/home/poleguy/.local/bin/hotkey-python3")
                        if key.keycode == 'KEY_TAB':
                            subprocess.Popen("/home/poleguy/.local/bin/hotkey-obs")
                            
                        if key.keycode == 'KEY_EQUAL':
                            subprocess.Popen("/home/poleguy/.local/bin/hotkey-vscode")
                            
                        if key.keycode == 'KEY_KPSLASH':
                            print("Hello, world!")
                            
                        if key.keycode == 'KEY_KPASTERISK':
                            print("Hello, world!")
                            
                        if key.keycode == 'KEY_BACKSPACE':
                            print("Hello, world!")
                            
                        if key.keycode == 'KEY_KP1':
                            print("Hello, world!1")
                            subprocess.Popen('/usr/local/bin/obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 scene switch "Scope"', shell=True)

                        if key.keycode == 'KEY_KP2':
                            print("Hello, world!2")
                            subprocess.Popen('/usr/local/bin/obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 scene switch "Share ViewSonic"', shell=True)

                        if key.keycode == 'KEY_KP3':
                            print("Hello, world!3")
                            subprocess.Popen('/usr/local/bin/obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 scene switch "Soldering"', shell=True)

                            
                        if key.keycode == 'KEY_KP4':
                            print("Hello, world!4")

                        if key.keycode == 'KEY_KP5':
                            print("Hello, world!5")
                            
                        if key.keycode == 'KEY_KP6':
                            print("Hello, world!6")
                            
                        if key.keycode == 'KEY_KP7':
                            print("Hello, world!7")
                            
                        if key.keycode == 'KEY_KP8':
                            print("Hello, world!8")
                            
                        if key.keycode == 'KEY_KP9':
                            print("Hello, world!9")
                            
                        if key.keycode == 'KEY_KP0':
                            print("Hello, world 0!")
                            subprocess.Popen('/usr/local/bin/obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 scene switch "Tele"', shell=True)
                            
                        if key.keycode == 'KEY_KPDOT':
                            print("Hello, world!")
                            subprocess.Popen('/usr/local/bin/obs-cli -p 7D4xNRVVAkE3sHhu -P 4455 -H 192.168.1.162 scene switch "Tele and Scope"', shell=True)

                            
                        if key.keycode == 'KEY_KPMINUS':
                            print("Hello, world!")
                            
                        if key.keycode == 'KEY_KPPLUS':
                            print("Hello, world!")
                            
                        if key.keycode == 'KEY_KPENTER':                            
                            subprocess.Popen('espeak "Merry Christmas, Damian"', shell=True)

        
        for device in dev, dev2:
            asyncio.ensure_future(print_events(device))
        
        loop = asyncio.get_event_loop()
        loop.run_forever()
