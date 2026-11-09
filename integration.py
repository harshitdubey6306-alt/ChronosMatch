import mmap
import struct
import time
import engine

order_format = 'Q d I'
order_size = struct.calcsize(order_format)
# We will read the 100,000 orders you previously blasted into the buffer
total_orders = 100000 

def run_integration():
    print("Connecting Zero-Copy IPC Bus to Cython Engine...")
    
    with open("order_buffer.dat", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        
        start_time = time.perf_counter()
        
        for i in range(total_orders):
            # 1. Read exact bytes for one order instantly from RAM
            raw_bytes = mm.read(order_size)
            if not raw_bytes or len(raw_bytes) < order_size:
                break
                
            # 2. Unpack the C-struct back into Python numbers
            order_id, price, quantity = struct.unpack(order_format, raw_bytes)
            
            # 3. Assign Buy (1) for even IDs, Sell (2) for odd IDs
            side = 1 if order_id % 2 == 0 else 2
            
            # 4. Feed instantly into the Cython engine
            engine.submit_order(order_id, side, price, quantity)
            
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        
        mm.close()
        
        print("\n--- Integration Complete ---")
        print(f"Processed {total_orders} orders in {elapsed:.4f} seconds.")
        
        # Check the final spread
        best_bid, best_ask = engine.get_spread()
        print(f"Final Spread -> Best Bid: ${best_bid:.2f} | Best Ask: ${best_ask:.2f}")

if __name__ == "__main__":
    run_integration()