import asyncio
import mmap
import struct
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# Manages active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

# Background task to read from mmap and broadcast
async def read_mmap_and_broadcast():
    MMAP_FILE = "live_bus.dat" 
    FILE_SIZE = 10 * 1024 * 1024
    order_format = 'Q d I'
    order_size = struct.calcsize(order_format)
    
    while True:
        try:
            with open(MMAP_FILE, "r+b") as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                offset = 0
                last_order_id = 0
                
                print("Connected to live_bus.dat. Broadcasting trades...")
                while True:
                    mm.seek(offset)
                    raw_bytes = mm.read(order_size)
                    
                    if len(raw_bytes) == order_size:
                        order_id, price, qty = struct.unpack(order_format, raw_bytes)
                        
                        # Only broadcast if we read a fresh, valid order
                        if order_id != 0 and order_id != last_order_id:
                            payload = {
                                "order_id": order_id,
                                "price": price,
                                "qty": qty
                            }
                            await manager.broadcast(payload)
                            last_order_id = order_id
                            
                            # Advance the offset just like the writer
                            offset = (offset + order_size) % FILE_SIZE
                        else:
                            # No new data written yet; yield control to keep WebSocket alive
                            await asyncio.sleep(0.01)
                    else:
                        await asyncio.sleep(0.01)
                        
        except FileNotFoundError:
            print(f"Waiting for {MMAP_FILE} to be created by the writer...")
            await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    # Start the mmap reader in the background when the server starts
    asyncio.create_task(read_mmap_and_broadcast())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)