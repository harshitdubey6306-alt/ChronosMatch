import mmap
import struct

# 1. Define the exact same byte format used in the writer
order_format = 'Q d I'
order_size = struct.calcsize(order_format)

# 2. Open the existing memory buffer file
with open("order_buffer.dat", "r+b") as f:
    # Map the file into memory
    mm = mmap.mmap(f.fileno(), 0)

    # 3. Read the exact number of bytes for one order
    raw_order_bytes = mm.read(order_size)

    # 4. Unpack the raw C-bytes back into standard Python numbers
    order_id, price, quantity = struct.unpack(order_format, raw_order_bytes)

    print(f"Instantly read from RAM -> ID: {order_id}, Price: ${price:.2f}, Quantity: {quantity}")
    
    mm.close()