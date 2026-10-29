import mmap
import struct
import asyncio
import random
import time
import os

# 1. Define the exact same byte format
order_format = 'Q d I'
order_size = struct.calcsize(order_format)
total_orders = 100000

# 2. Re-create the buffer to hold 100,000 orders
buffer_size = order_size * total_orders
with open("order_buffer.dat", "wb") as f:
    f.write(b'\x00' * buffer_size)

async def blast_orders(mm):
    """Simulates receiving a massive wave of trade orders."""
    print(f"Blasting {total_orders} orders into shared memory...")
    
    start_time = time.perf_counter()
    
    for i in range(total_orders):
        # Generate random mock trade data
        price = random.uniform(100.0, 200.0)
        quantity = random.randint(1, 1000)
        
        # Pack the bytes
        raw_order = struct.pack(order_format, i, price, quantity)
        
        # Write to memory instantly
        mm.write(raw_order)
        
        # Periodically yield control to simulate async websocket ingestion
        if i % 10000 == 0:
            await asyncio.sleep(0)
            
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    
    print(f"Finished! Wrote {total_orders} orders in {elapsed:.4f} seconds.")
    print(f"Throughput: {total_orders / elapsed:,.0f} orders/second")

async def main():
    # Open and map the file
    with open("order_buffer.dat", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        
        # Run the firehose
        await blast_orders(mm)
        
        mm.close()

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())