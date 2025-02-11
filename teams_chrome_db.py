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
                print(f"✅ Found Teams tab: {tab['url']}")
                return tab.get("webSocketDebuggerUrl")

        print("❌ Teams is not open in Chrome.")
        return None
    except Exception as e:
        print(f"Error fetching debugger URL: {e}")
        return None

def get_teams_status():
    """Connect to Chrome DevTools via WebSocket and extract Teams status from IndexedDB."""
    ws_url = get_teams_debugger_url()
    if not ws_url:
        return

    try:
        print(f"🔌 Connecting to WebSocket: {ws_url}")
        ws = websocket.WebSocket()
        ws.connect(ws_url)

        # Enable IndexedDB debugging
        ws.send(json.dumps({"id": 1, "method": "IndexedDB.enable"}))
        print("✅ Enabled IndexedDB debugging")

        # Request the list of IndexedDB databases
        ws.send(json.dumps({
            "id": 2,
            "method": "IndexedDB.requestDatabaseNames",
            "params": {"securityOrigin": "https://teams.microsoft.com"}
        }))
        print("🔍 Requested IndexedDB databases...")

        start_time = time.time()
        while True:
            response = json.loads(ws.recv())
            print(f"📩 WebSocket Response: {response}")  # Debugging - Show all responses

            if "result" in response and "databaseNames" in response["result"]:
                db_names = response["result"]["databaseNames"]
                print(f"📂 Teams IndexedDB Databases: {db_names}")

                if "appCache" in db_names:
                    print("✅ Found 'appCache' database. Requesting status...")
                    
                    # Request Object Stores in the "appCache" database
                    ws.send(json.dumps({
                        "id": 3,
                        "method": "IndexedDB.requestData",
                        "params": {
                            "securityOrigin": "https://teams.microsoft.com",
                            "databaseName": "appCache",
                            "objectStoreName": "status",
                            "indexName": "",
                            "skipCount": 0,
                            "pageSize": 1
                        }
                    }))
                    break  # Stop after finding appCache
            
            # Timeout after 10 seconds
            if time.time() - start_time > 10:
                print("⏳ Timed out waiting for response.")
                break

        # Listen for response with Teams status
        start_time = time.time()
        while True:
            response = json.loads(ws.recv())
            print(f"📩 WebSocket Response (Status Data): {response}")  # Debugging

            if "result" in response and "objectStoreDataEntries" in response["result"]:
                entries = response["result"]["objectStoreDataEntries"]
                for entry in entries:
                    try:
                        raw_value = entry["value"]["value"]
                        status_data = json.loads(raw_value)
                        if "status" in status_data:
                            print(f"🎯 Microsoft Teams Status: {status_data['status']}")
                            ws.close()
                            return
                    except:
                        continue

            # Timeout after 10 seconds
            if time.time() - start_time > 10:
                print("⏳ Timed out waiting for status response.")
                break

        ws.close()
        print("❌ Could not determine Teams status.")

    except Exception as e:
        print(f"🚨 Error connecting to WebSocket: {e}")

# Run the function
get_teams_status()
