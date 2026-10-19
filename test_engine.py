import engine

print("--- Testing ChronosMatch Order Matching ---")

# 1. Place a SELL order: ID=101, Side=2 (SELL), Price=$150.00, Qty=50
print("Submitting Sell Order: 50 units @ $150.00")
engine.submit_order(101, 2, 150.00, 50)

# 2. Place another SELL order higher up: ID=102, Side=2 (SELL), Price=$152.00, Qty=100
print("Submitting Sell Order: 100 units @ $152.00")
engine.submit_order(102, 2, 152.00, 100)

# Check current spread
best_bid, best_ask = engine.get_spread()
print(f"Current Spread -> Best Bid: ${best_bid:.2f} | Best Ask: ${best_ask:.2f}")

# 3. Place an aggressive BUY order: ID=201, Side=1 (BUY), Price=$151.00, Qty=30
# This should match 30 units against order #101 at $150.00!
print("\nSubmitting Crossing Buy Order: 30 units @ $151.00...")
engine.submit_order(201, 1, 151.00, 30)

# 4. Place another BUY order that clears the rest of order #101:
print("\nSubmitting Crossing Buy Order: 40 units @ $150.00...")
engine.submit_order(202, 1, 150.00, 40)