"""
ChronosMatch Exchange Feed Simulator
"""
import mmap
import struct
import time
import random
import os

FILE_SIZE = 10 * 1024 * 1024
order_format = 'Q d I'
order_size = struct.calcsize(order_format)

def run_writer():
    if not os.path.exists("live_bus.dat"):
        print("Initializing zero-copy ring buffer...")
        with open("live_bus.dat", "wb") as f:
            f.write(b'\x00' * FILE_SIZE)
    else:
        print("Ring buffer found. Connecting to existing bus...")
        
    print("Starting live order firehose! Press Ctrl+C to stop.")
    with open("live_bus.dat", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        
        # THE FIX: Instantly zero out the memory map to clear ghost data
        # This prevents the server from sprinting ahead of the writer.
        print("Clearing old ghost data...")
        mm.seek(0)
        mm.write(b'\x00' * FILE_SIZE)
        
        order_id = 1
        offset = 0
        
        try:
            while True:
                price = round(random.uniform(90.0, 210.0), 2)
                qty = random.randint(1, 100)
                
                raw_bytes = struct.pack(order_format, order_id, price, qty)
                mm.seek(offset)
                mm.write(raw_bytes)
                
                order_id += 1
                offset = (offset + order_size) % FILE_SIZE
                
                time.sleep(0.001) 
        except KeyboardInterrupt:
            print("\nFirehose stopped.")
            mm.close()

if __name__ == "__main__":
    run_writer()