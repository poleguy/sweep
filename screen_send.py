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

#print(get_mouse_position())

def window_around_cursor1():
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    x,y = get_mouse_position()
    print(x,y)
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

def window_around_cursor():
    global left, top
    global last_x, last_y
    # returns a window WIDTH, HEIGHT centered around the cursor unless the cursor is too close to
    # the edge of the SERVER_WIDTH, SERVER_HEIGHT
    # then it limits to the edges of the screen

    DEAD_X = 300
    DEAD_Y = 170

    
    
    x,y = get_mouse_position()
    print(last_x, last_y, x, y)

    if x < last_x + DEAD_X and x > last_x - DEAD_X:
        # in dead zone
        x = last_x
    else:
        delta = int(((DEAD_X - abs(last_x - x))/DEAD_X)*SPEED_SCALE)
        if last_x - x > 0:
            delta = - delta
        x = last_x - delta
        print(delta)
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
        print(delta)
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
    last_x, last_y = get_mouse_position()
    with mss(with_cursor=True) as sct:
        # The region to capture
        #rect = {'top': 0+HEIGHT, 'left': SERVER_OFFSET, 'width': WIDTH, 'height': HEIGHT}


        while server_running:
            rect = window_around_cursor()
            print(rect)
            try:
                print('grab')
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
            except Exception as e:
                raise e
                print(e)
                print("yucky yuck")
                server_running = False
        print("thread done")

                


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

def main(host='192.168.1.162', port=5000):
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
            print("here")
            conn, addr = sock.accept()
            print('Client connected IP:', addr)
            #thread = Thread(target=retrieve_screenshot, args=(conn,))
            retrieve_screenshot(conn)
            #thread.start()
            print("screenhot process done")
    except KeyboardInterrupt:
        print('joining thread')
        #thread.join()
        pass  # This will handle Ctrl+C gracefully
    finally:
        print('closing socket')
        sock.close()

p = tkinter.Tk()
        
if __name__ == '__main__':
    main()
