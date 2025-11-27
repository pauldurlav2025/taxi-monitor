import asyncio
import json
import websockets
import random
from taxi_monitor.zones import get_random_start_location

HOST = "localhost"
PORT = 64000
NUM_taxies = 20

LOCATION_REPORTING_INTERVAL = 5  # seconds


class TaxiClient:
    def __init__(
        self, 
        taxi_id,
        websocket=None
    ):
        self.id = f"TAXI-{taxi_id}"
        self.latitude, self.longitude = get_random_start_location()
        self.websocket = websocket 
        self.keep_connected = True

    def travel(self):
        self.latitude += random.uniform(-0.002, 0.002)
        self.longitude += random.uniform(-0.002, 0.002)
        
    async def start_journey(self):
        uri = f"ws://{HOST}:{PORT}"
        while self.keep_connected:
            try:
                async with websockets.connect(uri) as websocket:
                    print(f"{self.id}: Connected to server.")
                    self.websocket = websocket
                    while self.keep_connected:
                        self.travel()
                        taxi_shadow = {
                            "id": self.id,
                            "latitude": self.latitude,
                            "longitude": self.longitude
                        }
                        
                        await websocket.send(json.dumps(taxi_shadow))
                        await asyncio.sleep(5) 
                        
            except websockets.exceptions.ConnectionClosed:
                print(f"[{self.id}] Connection closed. Retrying in {LOCATION_REPORTING_INTERVAL} seconds...")
            except ConnectionRefusedError:
                print(f"[{self.id}] Server not running. Retrying in {LOCATION_REPORTING_INTERVAL} seconds...")
            except Exception as e:
                print(f"[{self.id}] An unexpected error occurred: {e}")

            await asyncio.sleep(LOCATION_REPORTING_INTERVAL)

async def main():
    global taxi_list
    taxi_list = []
    taxi_tasks = []

    for i in range(0, NUM_taxies):
        taxi_list.append(TaxiClient(i + 1))
    
    for i in range(0, NUM_taxies):
        taxi_tasks.append(taxi_list[i].start_journey())
    
    await asyncio.gather(*taxi_tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        for i in range(0, NUM_taxies):
            taxi_list[i].keep_connected = False
        print("\nTaxi clients shut down.")