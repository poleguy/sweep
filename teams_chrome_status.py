# run with
#
# killall chrome
# google-chrome·--app=https://teams.microsoft.com·--remote-debugging-port=9222·--remote-allow-origins=http://localhost:9222
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

DEBUG_URL = "http://localhost:9222/json"

def get_teams_debugger_url():
    """Fetch the WebSocket Debugger URL for the Microsoft Teams tab."""
    try:
        response = requests.get(DEBUG_URL)
        tabs = response.json()
        
        for tab in tabs:
            if "teams.microsoft.com" in tab.get("url", ""):
                #print(f"Found Teams tab: {tab['url']}")
                return tab.get("webSocketDebuggerUrl")

        print("Teams is not open in Chrome.")
        return None
    except Exception as e:
        print(f"Error fetching debugger URL: {e}")
        return None


def get_current_html(ws):
    payload = {
        "id": 2,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "document.documentElement.outerHTML"
        }
    }
    ws.send(json.dumps(payload))
    return json.loads(ws.recv())["result"]["result"]["value"]

    
def get_teams_status():
    """Connect to Chrome DevTools via WebSocket and extract Teams status from IndexedDB."""
    ws_url = get_teams_debugger_url()
    if not ws_url:
        return

    #print(f"🔌 Connecting to WebSocket: {ws_url}")
    ws = websocket.WebSocket()
    ws.connect(ws_url)

    a = get_current_html(ws)
    status = "Unknown status"
    #print(a)
    target = '"Your profile, status '
    n = len(target)
    status_idx = a.find(target)
    if status_idx == -1:
        print(a)
        print("Error!")

    status_str = a[status_idx+n:].split('"')[0]
    
    
    if "Busy" in status_str:
        status = "Busy"
    elif "Available" in status_str:
        status = "Available"
    elif "In a call" in status_str:
        status = "In a call"
    else:
        print(status_str)
        print("Not handled")
    #print(status)
        

    ws.close()


    return status

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
        self.open_serial()
        self.thread.start()

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
    writer = SerialWriter(port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0', message="Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not?")

    # https://alexandra-zaharia.github.io/posts/how-to-stop-a-python-thread-cleanly/
    stop_event = threading.Event()
    signal.signal(signal.SIGINT, handle_kb_interrupt)
    try:
        while g_running:
            # Run the function
            status = get_teams_status() # this takes about 400-500msec
            #led_on_when = ['In a call', 'Busy'] # for testing
            led_on_when = ['In a call', 'Presenting']
            if status in led_on_when:
                print(f"on: {status}")
                writer.on()
            else:
                print(f"off: {status}")
                writer.off()

            time.sleep(2.0) # no sense hammering it too hard, but we want the light to go on quickly
            #writer.write()
#    except KeyboardInterrupt as e:
#        pass
    finally:
        #writer.stop()
        #writer.thread.join()
        pass

    print("stopping")
    writer.stop()

    print("done")
    for t in g_threads:
        t.join()
    print("doner")
        



# https://gist.github.com/vfreex/8904bb57dd751ae078a3b1e3e3f11278
