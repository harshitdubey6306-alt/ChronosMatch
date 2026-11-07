import heapq
from typing import NamedTuple, List

from order_manager import OrderManager, BUY, SELL



class Trade(NamedTuple):
    trade_id: int
    buy_id: object
    sell_id: object
    price: float
    quantity: int

class MatchingEngine:
    def __init__(self, manager=None):
        self.manager = manager or OrderManager()
        self._bids = []      # entries: (-price, seq, order)
        self._asks = []      # entries: (price, seq, order)
        self.trades: List[Trade] = []
        self._trade_id = 0

        
    # ---------- internals ----------
    @staticmethod
    def _clean(heap):
        """Drop cancelled / filled orders sitting on top of the heap."""
        while heap and heap[0][2].quantity == 0:
            heapq.heappop(heap)