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

    try:
        #print(f"🔌 Connecting to WebSocket: {ws_url}")
        ws = websocket.WebSocket()
        ws.connect(ws_url)

        a = get_current_html(ws)
        #print(a)
        if "Your profile, status Busy" in a:
            print("Busy")
        elif "Your profile, status Available" in a:
            print("Availabile")
        elif "Your profile, status In a call" in a:
            print("In a call")
        else:
            #print(a)
            print("Error")
            

        ws.close()
#        print("❌ Could not determine Teams status.")

    except Exception as e:
        print(f"🚨 Error connecting to WebSocket: {e}")

# Run the function
get_teams_status()
