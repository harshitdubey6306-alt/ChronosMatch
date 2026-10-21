import mmap
import struct
import engine
import time

order_format = 'Q d I'
order_size = struct.calcsize(order_format)
FILE_SIZE = 10 * 1024 * 1024

def run_reader():
    # Wait a brief moment to ensure the writer has created the file
    time.sleep(1) 
    print("Engine listening on zero-copy bus... Press Ctrl+C to stop.")
    
    with open("live_bus.dat", "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        offset = 0
        last_id = 0
        
        try:
            while True:
                mm.seek(offset)
                raw_bytes = mm.read(order_size)
                order_id, price, qty = struct.unpack(order_format, raw_bytes)
                
                # Only process if a NEW order has actually been written
                if order_id > last_id:
                    side = 1 if order_id % 2 == 0 else 2
                    engine.submit_order(order_id, side, price, qty)
                    
                    last_id = order_id
                    offset = (offset + order_size) % FILE_SIZE
                    
                    # Print an update to the terminal every 1,000 orders
                    if order_id % 1000 == 0:
                        best_bid, best_ask = engine.get_spread()
                        print(f"Processed {order_id} orders | Live Spread -> Bid: ${best_bid:.2f} Ask: ${best_ask:.2f}")
                else:
                    # Spin-wait (checking continuously for new data)
                    pass
        except KeyboardInterrupt:
            print("\nEngine shut down safely.")
            mm.close()

if __name__ == "__main__":
    run_reader()