# cython: language_level=3
# engine.pyx

from libc.stdlib cimport malloc, free
from libc.stdio cimport printf

# Define Order Side: 1 for BUY, 2 for SELL
cdef enum OrderSide:
    BUY = 1
    SELL = 2

# Limit Order structure stored directly in C memory
cdef struct Order:
    unsigned long long order_id
    unsigned int side        # 1 = BUY, 2 = SELL
    double price
    unsigned int quantity

# Fixed-size memory pools for book depth to prevent dynamic allocation spikes
DEF MAX_ORDERS = 1024

cdef Order buy_book[MAX_ORDERS]
cdef int buy_count = 0

cdef Order sell_book[MAX_ORDERS]
cdef int sell_count = 0

cdef void match_buy_order(Order* incoming):
    global sell_count, buy_count
    cdef int i = 0
    cdef unsigned int fill_qty = 0

    while i < sell_count and incoming.quantity > 0:
        # Check Price cross: Buy price >= Best Sell price
        if incoming.price >= sell_book[i].price:
            if incoming.quantity <= sell_book[i].quantity:
                fill_qty = incoming.quantity
            else:
                fill_qty = sell_book[i].quantity

            incoming.quantity -= fill_qty
            sell_book[i].quantity -= fill_qty

            printf("[TRADE MATCH] Buy #%llu matched with Sell #%llu | Qty: %u @ $%.2f\n",
                   incoming.order_id, sell_book[i].order_id, fill_qty, sell_book[i].price)

            # If sell order is fully filled, compact the array
            if sell_book[i].quantity == 0:
                for j in range(i, sell_count - 1):
                    sell_book[j] = sell_book[j + 1]
                sell_count -= 1
                continue
        i += 1

    # If remainder left, insert into buy book (if space permits)
    if incoming.quantity > 0 and buy_count < MAX_ORDERS:
        buy_book[buy_count] = incoming[0]
        buy_count += 1

cdef void match_sell_order(Order* incoming):
    global buy_count, sell_count
    cdef int i = 0
    cdef unsigned int fill_qty = 0

    while i < buy_count and incoming.quantity > 0:
        # Check Price cross: Sell price <= Best Buy price
        if incoming.price <= buy_book[i].price:
            if incoming.quantity <= buy_book[i].quantity:
                fill_qty = incoming.quantity
            else:
                fill_qty = buy_book[i].quantity

            incoming.quantity -= fill_qty
            buy_book[i].quantity -= fill_qty

            printf("[TRADE MATCH] Sell #%llu matched with Buy #%llu | Qty: %u @ $%.2f\n",
                   incoming.order_id, buy_book[i].order_id, fill_qty, buy_book[i].price)

            # If buy order is fully filled, compact the array
            if buy_book[i].quantity == 0:
                for j in range(i, buy_count - 1):
                    buy_book[j] = buy_book[j + 1]
                buy_count -= 1
                continue
        i += 1

    # If remainder left, insert into sell book
    if incoming.quantity > 0 and sell_count < MAX_ORDERS:
        sell_book[sell_count] = incoming[0]
        sell_count += 1

# Bridge function callable from standard Python
cpdef void submit_order(unsigned long long order_id, unsigned int side, double price, unsigned int quantity):
    cdef Order ord
    ord.order_id = order_id
    ord.side = side
    ord.price = price
    ord.quantity = quantity

    if side == 1:
        match_buy_order(&ord)
    else:
        match_sell_order(&ord)

cpdef tuple get_spread():
    global buy_count, sell_count
    cdef double best_bid = 0.0
    cdef double best_ask = 0.0

    if buy_count > 0:
        best_bid = buy_book[0].price
    if sell_count > 0:
        best_ask = sell_book[0].price

    return (best_bid, best_ask)