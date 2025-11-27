import asyncio
import websockets
import json
from taxi_monitor.zones import get_current_zone

global command_line


HOST = "0.0.0.0" 
PORT = 64000

TAXI_STATUS = {}
CONNECTIONS = set()

command_line = ""

async def safe_send(websocket, message):
    try:
        await websocket.send(message)
    except (websockets.exceptions.ConnectionClosedOK, websockets.exceptions.ConnectionClosedError):
        pass

async def on_data_received(websocket):
    global command_line
    CONNECTIONS.add(websocket)
    taxi_id = None
    
    try:
        async for message in websocket:
            try:
                data = json.loads(message)

                taxi_id = data.get("id")
                latitude = data.get("latitude")
                longitude = data.get("longitude")
                new_zone = get_current_zone(latitude, longitude)
                
                if taxi_id not in TAXI_STATUS:
                    TAXI_STATUS[taxi_id] = {
                        "latitude": latitude,
                        "longitude": longitude,
                        "current_zone": new_zone,
                    }
                    report = f"{taxi_id}: Initial zone: {new_zone}"
                elif latitude == None:
                    report = f"{taxi_id}: Disconnected"
                    del TAXI_STATUS[taxi_id]    
                else:
                    old_zone = TAXI_STATUS[taxi_id]["current_zone"]
                    if new_zone != old_zone:
                        report = f"{taxi_id}: {old_zone} -> {new_zone}"
                        print(f"\r{report}", end='')
                        print(f"\n>{command_line}", end='')
                    else:
                        report = f"{taxi_id}: {new_zone}"
                        
                    TAXI_STATUS[taxi_id].update({
                        "latitude": latitude,
                        "longitude": longitude,
                        "current_zone": new_zone,
                    })

                await safe_send(websocket, report)
                
            except json.JSONDecodeError:
                print(f"Received invalid JSON message: {message}")
                await safe_send(websocket, "ERROR: Invalid JSON format.")
                
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Connection closed gracefully for {taxi_id}")
    except Exception as e:
        print(f"Error occurred with {taxi_id}: {e}")

async def cli_interface():
    global command_line
    print("\nTaxi Monitoring CLI")
    print("Available Commands: \nz <id> - zone-status <TAXI_ID>\nl - list\ne - exit")
    
    while True:
        try:
            command_line = await asyncio.to_thread(input, "> ")
            parts = command_line.strip().lower().split()
            command = parts[0] if parts else ""
            
            if command == "e":
                print("Shutting down CLI. Press Ctrl+C again to stop the server.")
                break
                
            elif command == "l":
                if not TAXI_STATUS:
                    print("No taxies currently connected.")
                    continue
                print("Currently Connected Taxies")
                for taxi_id in TAXI_STATUS.keys():
                    zone = TAXI_STATUS[taxi_id]['current_zone']
                    print(f"{taxi_id}: {zone}")
                
            elif command == "z" and len(parts) == 2:
                taxi_id_query = parts[1].upper() 
                if taxi_id_query in TAXI_STATUS:
                    status = TAXI_STATUS[taxi_id_query]
                    print(f"Status: {taxi_id_query} - Latitude: {status['latitude']:.4f}, Longitude: {status['longitude']:.4f}, Zone: {status['current_zone']}")
                else:
                    print(f"ERROR: Taxi {taxi_id_query} not found or disconnected.")
            
            else:
                print("Invalid command")

        except EOFError:
            print("\nShutting down CLI.")
            break
        except Exception as e:
            print(f"An error occurred in CLI: {e}")

async def run_server():
    server = await websockets.serve(
        on_data_received,
        HOST,
        PORT,
    )
    print(f"Central Taxi Monitoring Server started on ws://{HOST}:{PORT}")
    await asyncio.gather(server.wait_closed(), cli_interface())

def main():
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
    