import json
import os
import time
import signal
import socket
from threading import Thread
from zlib import compress
import sys
import tkinter 

from mss import mss

left = 0
top = 0

SERVER_WIDTH = 2560 
SERVER_HEIGHT = 1440
SERVER_OFFSET = 1280  # offset due to second screen to the left of main screen

SPEED_SCALE = 80

# teleprompter size (Low resolution, so you don't have to get too close to read.)
WIDTH = 1280
HEIGHT = 720


#!/usr/bin/env python

"""Get the current mouse position."""

import logging
import sys

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


lock_file_path = "script_lock.txt"


import time

def listen_for_messages():
    while True:
        try:
            with open("message.txt", "r") as file:
                message = file.readline().strip()
                if message:
                    print(f"Received message: {message}")
                    # Optionally, process the message here.
        except FileNotFoundError:
            pass
        time.sleep(1)  # Wait for new messages

#if __name__ == "__main__":
#    listen_for_messages()

import time

def send_message(message):
    with open("message.txt", "w") as file:
        file.write(message)

#if __name__ == "__main__":
#    message_to_send = "Hello from the second instance!"
#    send_message(message_to_send)
#    time.sleep(1)  # Give some time for the first instance to process the message (optional)
    

def is_script_already_running():
    return os.path.exists(lock_file_path)

def create_lock_file():
    with open(lock_file_path, "w") as lock_file:
        lock_file.write("Script is running.")

def remove_lock_file():
    os.remove(lock_file_path)

        
def get_mouse_position():
    global p
    """
    Get the current position of the mouse.

    Returns
    -------
    dict :
        With keys 'x' and 'y'
    """
    x, y = p.winfo_pointerxy()
    
    return x,y

def window_around_cursor(x,y):
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    #x,y = get_mouse_position()
    #print(x,y)
    if x < SERVER_OFFSET+WIDTH/2:
        left = SERVER_OFFSET
    elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
        left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
    else:
        left = x - WIDTH/2
    left = int(left)
    
    if y < HEIGHT/2:
        top = 0
    elif y > SERVER_HEIGHT - HEIGHT/2:
        top = SERVER_HEIGHT - HEIGHT
    else:
        top = y - HEIGHT/2
    top = int(top)

    rect = {'top': top, 'left': left, 'width': WIDTH, 'height':HEIGHT}
    return rect


def window_around_cursor_old():
    global left, top
    global last_x, last_y
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    DEAD_X = 630
    DEAD_Y = 350

    # TODO:add a way to modify this behavior to only act when a key is pressed.
    # possibly by having xfce4 keypress run a program that sends a message to trigger this 
    
    x,y = get_mouse_position()
    #print(last_x, last_y, x, y)

    if x < last_x + DEAD_X and x > last_x - DEAD_X:
        # in dead zone
        x = last_x
    else:
        #delta = int(((DEAD_X - abs(last_x - x))/DEAD_X)*SPEED_SCALE)
        delta = int(DEAD_X - abs(last_x - x)) # full jump
        if last_x - x > 0:
            delta = - delta
        x = last_x - delta
        #print(delta)
    x = min(x,SERVER_WIDTH+SERVER_OFFSET)
    x = max(x,0)
    
    if y < last_y + DEAD_Y and y > last_y - DEAD_Y:
        # in dead zone        
        y = last_y
    else:
        # in dead zone
        #delta = int(((last_y - y)/20)**2)
        #delta = int(((last_y - y)/DEAD_Y)*200)
        #delta = int(((DEAD_Y - abs(last_y - y))/DEAD_X)*SPEED_SCALE)
        delta = int(DEAD_Y - abs(last_y - y)) # full jump
        if last_y - y > 0:
            delta = - delta
        y = last_y - delta
        #print(delta)
    y = min(y,SERVER_HEIGHT)
    y = max(y,0)

    
        
    last_x = x
    last_y = y

#    print(x,y)
    #if left == SERVER_OFFSET:
#        if x < SERVER_OFFSET+WIDTH/2+DEAD_X:
#            left = SERVER_OFFSET
#        elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
#            left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
#        else:
#            left = x - WIDTH/2 - DEAD_X
#    else:
    if x < SERVER_OFFSET+WIDTH/2:
        left = SERVER_OFFSET
    elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
        left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
    else:
        left = x - WIDTH/2
    left = int(left)
    
    if y < HEIGHT/2:
        top = 0
    elif y > SERVER_HEIGHT - HEIGHT/2:
        top = SERVER_HEIGHT - HEIGHT
    else:
        top = y - HEIGHT/2
    top = int(top)

    rect = {'top': top, 'left': left, 'width': WIDTH, 'height':HEIGHT}
    return rect



#print(get_mouse_position())
def window_around_cursor4():
    global left, top
    global last_x, last_y
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    DEAD_X = 630
    DEAD_Y = 350


    # https://stackoverflow.com/questions/19861689/check-if-modifier-key-is-pressed-in-tkinter
    mods = {
        0x0001: 'Shift',
        0x0002: 'Caps Lock',
        0x0004: 'Control',
        0x0008: 'Left-hand Alt',
        0x0010: 'Num Lock',
        0x0080: 'Right-hand Alt',
        0x0100: 'Mouse button 1',
        0x0200: 'Mouse button 2',
        0x0400: 'Mouse button 3'
    }

    
    x,y = get_mouse_position()
    #print(last_x, last_y, x, y)

    if x < last_x + DEAD_X and x > last_x - DEAD_X:
        # in dead zone
        x = last_x
    else:
        #delta = int(((DEAD_X - abs(last_x - x))/DEAD_X)*SPEED_SCALE)
        delta = int(DEAD_X - abs(last_x - x)) # full jump
        if last_x - x > 0:
            delta = - delta
        x = last_x - delta
        #print(delta)
    x = min(x,SERVER_WIDTH+SERVER_OFFSET)
    x = max(x,0)
    
    if y < last_y + DEAD_Y and y > last_y - DEAD_Y:
        # in dead zone        
        y = last_y
    else:
        # in dead zone
        #delta = int(((last_y - y)/20)**2)
        #delta = int(((last_y - y)/DEAD_Y)*200)
        #delta = int(((DEAD_Y - abs(last_y - y))/DEAD_X)*SPEED_SCALE)
        delta = int(DEAD_Y - abs(last_y - y)) # full jump
        if last_y - y > 0:
            delta = - delta
        y = last_y - delta
        #print(delta)
    y = min(y,SERVER_HEIGHT)
    y = max(y,0)

    
        
    last_x = x
    last_y = y

#    print(x,y)
    #if left == SERVER_OFFSET:
#        if x < SERVER_OFFSET+WIDTH/2+DEAD_X:
#            left = SERVER_OFFSET
#        elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
#            left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
#        else:
#            left = x - WIDTH/2 - DEAD_X
#    else:
    if x < SERVER_OFFSET+WIDTH/2:
        left = SERVER_OFFSET
    elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
        left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
    else:
        left = x - WIDTH/2
    left = int(left)
    
    if y < HEIGHT/2:
        top = 0
    elif y > SERVER_HEIGHT - HEIGHT/2:
        top = SERVER_HEIGHT - HEIGHT
    else:
        top = y - HEIGHT/2
    top = int(top)

    rect = {'top': top, 'left': left, 'width': WIDTH, 'height':HEIGHT}
    return rect


def window_around_cursor1():
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    x,y = get_mouse_position()
    #print(x,y)
    if x < SERVER_OFFSET+WIDTH/2:
        left = SERVER_OFFSET
    elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
        left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
    else:
        left = x - WIDTH/2
    left = int(left)
    
    if y < HEIGHT/2:
        top = 0
    elif y > SERVER_HEIGHT - HEIGHT/2:
        top = SERVER_HEIGHT - HEIGHT
    else:
        top = y - HEIGHT/2
    top = int(top)

    rect = {'top': top, 'left': left, 'width': WIDTH, 'height':HEIGHT}
    return rect

def window_around_cursor2():
    global left, top
    global last_x, last_y
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    DEAD_X = 300
    DEAD_Y = 170

    
    
    x,y = get_mouse_position()
    #print(last_x, last_y, x, y)

    if x < last_x + DEAD_X and x > last_x - DEAD_X:
        # in dead zone
        x = last_x
    else:
        delta = int(((DEAD_X - abs(last_x - x))/DEAD_X)*SPEED_SCALE)
        if last_x - x > 0:
            delta = - delta
        x = last_x - delta
        #print(delta)
    x = min(x,SERVER_WIDTH+SERVER_OFFSET)
    x = max(x,0)
    
    if y < last_y + DEAD_Y and y > last_y - DEAD_Y:
        # in dead zone        
        y = last_y
    else:
        # in dead zone
        #delta = int(((last_y - y)/20)**2)
        #delta = int(((last_y - y)/DEAD_Y)*200)
        delta = int(((DEAD_Y - abs(last_y - y))/DEAD_X)*SPEED_SCALE)
        if last_y - y > 0:
            delta = - delta
        y = last_y - delta
        #print(delta)
    y = min(y,SERVER_HEIGHT)
    y = max(y,0)

    
        
    last_x = x
    last_y = y

#    print(x,y)
    #if left == SERVER_OFFSET:
#        if x < SERVER_OFFSET+WIDTH/2+DEAD_X:
#            left = SERVER_OFFSET
#        elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
#            left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
#        else:
#            left = x - WIDTH/2 - DEAD_X
#    else:
    if x < SERVER_OFFSET+WIDTH/2:
        left = SERVER_OFFSET
    elif x > SERVER_OFFSET + SERVER_WIDTH - WIDTH/2:
        left = SERVER_OFFSET + SERVER_WIDTH - WIDTH
    else:
        left = x - WIDTH/2
    left = int(left)
    
    if y < HEIGHT/2:
        top = 0
    elif y > SERVER_HEIGHT - HEIGHT/2:
        top = SERVER_HEIGHT - HEIGHT
    else:
        top = y - HEIGHT/2
    top = int(top)

    rect = {'top': top, 'left': left, 'width': WIDTH, 'height':HEIGHT}
    return rect

def retrieve_screenshot(conn):
    global server_running
    global last_x, last_y
    loop_running = True
    last_x, last_y = get_mouse_position()
    with mss(with_cursor=True) as sct:
        # The region to capture
        #rect = {'top': 0+HEIGHT, 'left': SERVER_OFFSET, 'width': WIDTH, 'height': HEIGHT}


        while server_running and loop_running:
            try:
                with open("message.txt", "r") as file:
                    message = file.readline().strip()
                    message = json.loads(message)
                    if message:
                        print(f"Received message: {message}")
                        # Optionally, process the message here.
                        x = int(message[0])
                        y = int(message[1])
            except FileNotFoundError:
                x = last_x
                y = last_y
        

            
            rect = window_around_cursor(x,y)
            #print(rect)
            try:
                #print('grab')
                # Capture the screen
                img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                pixels = compress(img.rgb, 6)
    
                # Send the size of the pixels length
                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                conn.send(bytes([size_len]))
    
                # Send the actual pixels length
                size_bytes = size.to_bytes(size_len, 'big')
                conn.send(size_bytes)
    
                # Send pixels
                conn.sendall(pixels)
            except BrokenPipeError as e:
                print(e)
                print("yucky yuck")
                #conn.close()
                loop_running = False

                #server_running = False
            except Exception as e:
                raise e
                print(e)
                #print("yucky yuck")
                server_running = False
        #print("thread done")

                


def main_old(host='192.168.1.162', port=5000):
    sock = socket.socket()
    sock.bind((host, port))
    try:
        sock.listen(5)
        print('Server started.')

        while 'connected':
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            thread = Thread(target=retrieve_screenshot, args=(conn,))
            thread.start()
    finally:
        sock.close()



# Global variable to track whether the server is running
server_running = True

def handle_sigint(sig, frame):
    global server_running
    print("\nCtrl+C received. Closing the server...")
    server_running = False

def main(host='192.168.1.162', port=5000, trigger=False):

    print("blah")
    
# https://stackoverflow.com/questions/656933/communicating-with-a-running-python-daemon?rq=3
# https://stackoverflow.com/questions/44940164/stopping-a-python-multiprocessing-basemanager-serve-forever-server

    # The script is already running; send a message to the existing instance.
    # Implement your message-sending logic here.
#    if trigger:
#        class RemoteManager(BaseManager):
#            pass
#        
#        RemoteManager.register('RemoteOperations')
#        manager = RemoteManager(address=('localhost', 12345), authkey=b'secret')
#        manager.connect()
#        
#        remoteops = manager.RemoteOperations()
#        print(remoteops.add(2, 3))
#        print(remoteops.multiply(2, 3))
#        pass
#    else:
#        # Create the lock file to indicate that the script is running.
#        create_lock_file()
#        from multiprocessing.managers import BaseManager
#
#        class RemoteOperations:
#            def add(self, a, b):
#                print('adding in server process!')
#                return a + b
#        
#            def multiply(self, a, b):
#                print('multiplying in server process!')
#                return a * b
#        
#        class RemoteManager(BaseManager):
#            pass
#        
#        RemoteManager.register('RemoteOperations', RemoteOperations)
#        
#        manager = RemoteManager(address=('', 12345), authkey=b'secret')
#        #manager.get_server().serve_forever()
#        manager.start()

        # Your script's main logic goes here.

        # Remove the lock file when the script is done.
       # remove_lock_file()
        
    global server_running
    sock = socket.socket()
    # https://stackoverflow.com/questions/4465959/python-errno-98-address-already-in-use
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    
    try:
        sock.listen(5)
        print('Server started.')
        
        # Set up a signal handler for Ctrl+C
        signal.signal(signal.SIGINT, handle_sigint)
 
        while server_running:
            #print("here")
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            #thread = Thread(target=retrieve_screenshot, args=(conn,))
            retrieve_screenshot(conn)
        time.sleep(1)  # Wait for new messages

            #thread.start()
            #print("screenhot process done")
    except KeyboardInterrupt:
        #print('joining thread')
        #thread.join()
        pass  # This will handle Ctrl+C gracefully
    finally:
        print('closing socket')
        sock.close()
#        manager.shutdown()

p = tkinter.Tk()
        
if __name__ == '__main__':
    print("ack")
    main()
