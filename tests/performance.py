
import time

start_time = time.perf_counter()

# Create 1000 sample orders
orders = []

for i in range(1000):
    orders.append({
        "order_id": i + 1,
        "price": 100,
        "quantity": 5
    })

end_time = time.perf_counter()

execution_time = end_time - start_time

print("Total orders:", len(orders))
print("Execution time:", execution_time, "seconds")

if execution_time > 0:
    throughput = len(orders) / execution_time
    print("Throughput:", throughput, "orders/second")