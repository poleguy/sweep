# run with
#
# killall chrome
# google-chrome·--app=https://teams.microsoft.com·--remote-debugging-port=9222·--remote-allow-origins=http://localhost:9222

# for elgar:
#     google-chrome --app=https://teams.microsoft.com --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222 --user-data-dir=/home/poleguy/flippy-data/2023/remap/remote-debug-profile --profile-directory=Default

# for flippy:
# google-chrome --app=https://teams.microsoft.com --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222 --user-data-dir=/home/poleguy/remote-debug-profile --profile-directory=Default


# DevTools remote debugging requires a non-default data directory. Specify this using --user-data-dir.

# python3 teams_chrome_status.py

# run from?

# if you see:
# Error fetching debugger URL: HTTPConnectionPool(host='localhost', port=9222): Max retries exceeded with url: /json (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7921622ab150>: Failed to establish a new connection: [Errno 111] Connection refused'))
# adjust ~/flippy-data/2023/reamp/hotkey-teams

import signal
import requests
import websocket
import json
import time
import bash

PORT = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0'
#PORT = None
DEBUG_URL = "http://localhost:9222/json"

def get_teams_debugger_url():
    """Fetch the WebSocket Debugger URL for the Microsoft Teams tab."""
    try:
        response = requests.get(DEBUG_URL)
        tabs = response.json()
        
        for tab in tabs:
            tab_to_print = tab.get("url","")
            #print(f"tab is: {tab_to_print}")
            if "teams.microsoft.com" in tab.get("url", ""):
                #print(f"Found Teams tab: {tab['url']}")
                return tab.get("webSocketDebuggerUrl")

        print("Teams is not open in Chrome.")
        return None
    except Exception as e:
        print(f"Error fetching debugger URL: {e}")
        print("Trouble fetching debugger URL, maybe teams is not running yet?")
        return None


def get_current_html(ws):
    payload = {
        "id": 2,
        "method": "Runtime.evaluate",
        "params": {
            #"expression": "document.documentElement.outerHTML"
            "expression": """
(() => {
  const el = document.querySelector('[aria-label^="Your profile, status"]');
  return el ? el.getAttribute('aria-label') : null;
})()
"""

        }
    }
    ws.send(json.dumps(payload))
    return json.loads(ws.recv())["result"]["result"]["value"]

def get_activity_badge_count(ws, timeout=2.0):
    req_id = 45

    payload = {
        "id": req_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": """
(() => {
  // Find the Activity button by aria-label
  const activityBtn = Array.from(document.querySelectorAll('[aria-label]'))
    .find(el => el.getAttribute('aria-label')?.toLowerCase().includes('activity'));

  if (!activityBtn) return 0;

  // Badge is usually a sibling or descendant near the button
  const badge =
    activityBtn.querySelector('.fui-Badge') ||
    activityBtn.parentElement?.querySelector('.fui-Badge') ||
    activityBtn.nextElementSibling?.querySelector('.fui-Badge');

  if (!badge) return 0;

  // Extract numeric content
  const text = badge.textContent.trim();
  const num = parseInt(text, 10);

  return isNaN(num) ? 0 : num;
})()
"""
        }
    }

    ws.settimeout(timeout)
    ws.send(json.dumps(payload))

    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") != req_id:
            continue

        try:
            return msg["result"]["result"]["value"]
        except (KeyError, TypeError):
            return 0


def get_chat_badge_count(ws, timeout=2.0):
    req_id = 45

    payload = {
        "id": req_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": """
(() => {
  // Find the Chat button by aria-label
  const activityBtn = Array.from(document.querySelectorAll('[aria-label]'))
    .find(el => el.getAttribute('aria-label')?.toLowerCase().includes('chat'));

  if (!activityBtn) return 0;

  // Badge is usually a sibling or descendant near the button
  const badge =
    activityBtn.querySelector('.fui-Badge') ||
    activityBtn.parentElement?.querySelector('.fui-Badge') ||
    activityBtn.nextElementSibling?.querySelector('.fui-Badge');

  if (!badge) return 0;

  // Extract numeric content
  const text = badge.textContent.trim();
  const num = parseInt(text, 10);

  return isNaN(num) ? 0 : num;
})()
"""
        }
    }

    ws.settimeout(timeout)
    ws.send(json.dumps(payload))

    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") != req_id:
            continue

        try:
            return msg["result"]["result"]["value"]
        except (KeyError, TypeError):
            return 0


def mentions_is_bold(ws, timeout=2.0):
    req_id = 44

    # this may return None if in Calendar view, etc. So None and False are different.
    payload = {
        "id": req_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": """
(() => {
  const item = document.querySelector('[data-testid="list-item-activities-mentions"]');
  if (!item) return null;

  // Find the text span inside the list item
  const textEl = item.querySelector('span');
  if (!textEl) return null;

  const weight = window.getComputedStyle(textEl).fontWeight;

  // Normalize: numeric weights >= 600 are effectively bold
  const numeric = parseInt(weight, 10);
  return (weight === 'bold') || (!isNaN(numeric) && numeric >= 600);
})()
"""
        }
    }

    ws.settimeout(timeout)
    ws.send(json.dumps(payload))

    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") != req_id:
            continue

        try:
            return msg["result"]["result"]["value"]
        except (KeyError, TypeError):
            return None


def get_teams_status():
    """Connect to Chrome DevTools via WebSocket and extract Teams status from IndexedDB."""
    ws_url = get_teams_debugger_url()
    if not ws_url:
        return

    #print(f"Connecting to WebSocket: {ws_url}")
    ws = websocket.WebSocket()
    ws.connect(ws_url)

    a = get_current_html(ws)
    status = "Unknown status"
    #print(a)
    target = 'Your profile, status '
    n = len(target)
    status_idx = a.find(target)
    if status_idx == -1:
        #print(a)
        print("Warning, target not found in html. Maybe teams is restarting.")

    status_str = a[status_idx+n:].split('"')[0]
    
    
    if "Busy" in status_str:
        status = "Busy"
    elif "Available" in status_str:
        status = "Available"
    elif "In a call" in status_str:
        status = "In a call"
    elif "Be right back " in status_str:
        status = "Be right back"
    else:
        print(f"Current status is '{status_str}' which is not handled.")

    #print(status)
        

    ws.close()


    return status


def get_teams_mamola():
    """Detect unread @mentions in Microsoft Teams."""

    ws_url = get_teams_debugger_url()
    if not ws_url:
        return "Teams not running"

    ws = websocket.WebSocket()
    ws.connect(ws_url)


    is_unread = mentions_is_bold(ws)

    badge_count = get_activity_badge_count(ws)

    chat_badge_count = get_chat_badge_count(ws)

    if is_unread is None: # can't determine if mentions is bold
        if badge_count > 0 or chat_badge_count > 0:
            status = "unread activity or chat"
        else:
            status = "unknown"
    elif is_unread:
        status = "unread mentions"
    else:
        if badge_count > 0 or chat_badge_count > 0:
            status = "unread activity or chat"
        else:
            status = "no unread mentions"

    #if label and any(c.isdigit() for c in label):
    #    status = "unread mentions"

 
    ws.close()
    return status

def send_phone_notification(duration): # duration indicates how long the notification has been going, to escalate volume, etc.
    # better would be to send an email that triggers a notification.
    #bash.bash("sudo monit restart grandstream_gt802")
    bash.bash("notify-send Hello")
    
    
# Thanks Chad Zebedee

import threading
import time
import serial

g_threads = []
g_running = True

class SerialWriter:
    def __init__(self, port: str, baudrate: int = 115200, message: str = "default", interval: float = 1.0):
        global g_threads
        """
        Initialize the SerialWriter.
        :param port: Serial port (e.g., '/dev/ttyUSB0')
        :param baudrate: Baud rate for communication.
        :param message: Message to send when on.
        :param interval: Time interval (in seconds) between messages.
        """
        self.port = port
        self.baudrate = baudrate
        self.message = message
        self.interval = interval
        self.thread = threading.Thread(target=self._write)
        g_threads.append(self.thread)        
        self.led_on = False
        self.running = True
        if port != None:
            self.open_serial()
            self.thread.start()
        else:
            self.serial_conn = None
    def on(self):
        """Start writing to the serial port."""
        self.led_on = True

    def off(self):
        """Stop writing to the serial port."""
        self.led_on = False

    def stop(self):
        """Stop writing to the serial port."""
        self.off()
        if self.serial_conn:
            self.serial_conn.close()
        self.running = False
        #self.thread.join()

    def open_serial(self):
        self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
        try:
            self.serial_conn.open()
            if self.serial_conn.isOpen():
                return True
        except serial.SerialException as e:
            print("serial exception")
            pass
            

    def _write(self):
        """Internal loop that writes to the serial port at the specified interval."""
        while self.running:
            try:
                while self.running:
                    #if stop_event.is_set():
                    #    break
                    while self.led_on:
                        if self.serial_conn:
                            self.serial_conn.write((self.message + "\n").encode())
                        else:
                            self.open_serial()
                        #print("...")
                        time.sleep(0.1)
                    #print('idle')
                    time.sleep(0.1)
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                if self.serial_conn:
                    self.serial_conn.close()
                    self.serial_conn = None
                time.sleep(1.0)
                pass
                #self.stop()
        
            
        #self.stop()
        print("closing")        
        if self.serial_conn:
            self.serial_conn.close()


def handle_kb_interrupt(sig, frame):
    global g_threads
    global g_running
    print("handling interreupt")
    for t in g_threads:
        t.running = False
    g_running = False
    #stop_event.set()

    
if __name__ == "__main__":
    # Run the function

    # Sending data to the serial port will turn the light on for a couple seconds
    # The light will go off if serial data stops flowing
    #writer = SerialWriter(port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0', message="Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not?")
    writer = SerialWriter(port=PORT, message="Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not?")

    # https://alexandra-zaharia.github.io/posts/how-to-stop-a-python-thread-cleanly/
    #stop_event = threading.Event()
    signal.signal(signal.SIGINT, handle_kb_interrupt)
    # handle cleanup if everything goes wrong, so that the program closes properly and doesn't hang because of background threads, and can be restarted by a systemd service.
    # this also works for ctrl c
    try: 
        while g_running:
            try:
                # Run the function
                status = get_teams_status() # this takes about 400-500msec
                # Use "Be right back" for manually testing if lantern turns on correctly
                led_on_when = ['In a call', 'Presenting', 'Be right back']
                if status in led_on_when:
                    print(f"on: {status}")
                    writer.on()
                else:
                    print(f"off: {status}")
                    writer.off()
    
                #writer.write()
            except websocket._exceptions.WebSocketConnectionClosedException as e:
                print("Retrying, to handle error: 'Connection to remote host was lost'")
            except KeyError as e:
                print("Retrying, to handle error: 'Key Error'")

            status = get_teams_mamola() # another half second?
            if status == "unread mentions":
                send_phone_notification(0)
            elif status == "unread activity or chat":
                send_phone_notification(0)
            else: 
                print("No unread notifications")

            # no sense hammering it too hard, but we want the light to go on quickly, and even in case of error we don't want it using 100% resources
            time.sleep(2.0) 

    finally:
        print("finally")
        print("stopping")
        writer.stop()
            
        print("done")
        for t in g_threads:
            t.join()
            print("doner")
        



# https://gist.github.com/vfreex/8904bb57dd751ae078a3b1e3e3f11278
