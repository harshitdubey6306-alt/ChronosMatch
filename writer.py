"""
ChronosMatch Exchange Feed Simulator
This module acts as a continuous live data firehose.
It generates random limit orders and writes them directly 
into a shared memory-mapped file (mmap) as raw C-struct bytes,
simulating a high-frequency trading exchange feed.
"""

import mmap
import struct
import time
import random
import os

# Pre-allocate a 10MB memory-mapped file
FILE_SIZE = 10 * 1024 * 1024
order_format = 'Q d I'
order_size = struct.calcsize(order_format)

def run_writer():
    print("Initializing zero-copy ring buffer...")
    with open("live_bus.dat", "wb") as f:
        f.write(b'\x00' * FILE_SIZE)
        
    print("Starting live order firehose! Press Ctrl+C to stop.")
    with open("live_bus.dat", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        order_id = 1
        offset = 0
        
        try:
            while True:
                # Generate a random trade
                price = round(random.uniform(90.0, 210.0), 2)
                qty = random.randint(1, 100)
                
                # Pack and write to the exact memory offset
                raw_bytes = struct.pack(order_format, order_id, price, qty)
                mm.seek(offset)
                mm.write(raw_bytes)
                
                order_id += 1
                # Loop back to the start of the file if we hit the 10MB limit
                offset = (offset + order_size) % FILE_SIZE
                
                # A micro-sleep to prevent completely locking up your Windows UI
                time.sleep(0.001) 
        except KeyboardInterrupt:
            print("\nFirehose stopped.")
            mm.close()

if __name__ == "__main__":
    run_writer()