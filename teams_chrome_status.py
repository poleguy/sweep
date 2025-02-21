# run with
#
# killall chrome
# google-chrome·--app=https://teams.microsoft.com·--remote-debugging-port=9222·--remote-allow-origins=http://localhost:9222
# python3 teams_chrome_status.py

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
                #print(f"✅ Found Teams tab: {tab['url']}")
                return tab.get("webSocketDebuggerUrl")

        print("❌ Teams is not open in Chrome.")
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

class SerialWriter:
    def __init__(self, port: str, baudrate: int = 115200, message: str = "default", interval: float = 1.0):
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
        self.thread = None
        self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
        self.led_on = False

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

    def write(self):
        """Internal loop that writes to the serial port at the specified interval."""
        try:
            if self.led_on:
                self.serial_conn.write((self.message + "\n").encode())
                #  sleep(0.01)
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            self.stop()
            
if __name__ == "__main__":
    # Run the function

    # Sending data to the serial port will turn the light on for a couple seconds
    # The light will go off if serial data stops flowing
    writer = SerialWriter(port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0', message="Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not? Let's use a very long message. Why not?")
    try:
        while True:
            # Run the function
            status = get_teams_status()
            led_on_when = ['In a call', 'Busy']
            if status in led_on_when:
                print("on")
                writer.on()
            else:
                print("off")
                writer.off()

            time.sleep(0.001) # rate limit causes trouble between 0.1 and 0.2
            writer.write()
    finally:
        writer.stop()


        


