import mmap
import struct
import os

# 1. Define what our trade order looks like in raw C-bytes
# 'Q' = Order ID (8 bytes), 'd' = Price (8 bytes), 'I' = Quantity (4 bytes)
order_format = 'Q d I'
order_size = struct.calcsize(order_format)

# 2. Create an empty file to act as our shared memory space
# We will make it big enough to hold exactly 1000 orders
buffer_size = order_size * 1000
with open("order_buffer.dat", "wb") as f:
    f.write(b'\x00' * buffer_size)

# 3. Open the file and map it directly into RAM
with open("order_buffer.dat", "r+b") as f:
    # mmap.mmap(file_descriptor, length)
    mm = mmap.mmap(f.fileno(), 0)

    # 4. Pack a fake trade order (ID: 1, Price: 150.50, Quantity: 100)
    raw_order_bytes = struct.pack(order_format, 1, 150.50, 100)

    # 5. Write the raw bytes into the memory map
    mm.write(raw_order_bytes)
    
    print("Order successfully written to RAM!")
    
    # Close the memory map
    mm.close()