
import unittest


class TestTradingRules(unittest.TestCase):

    def test_equal_prices(self):
        buy_price = 100
        sell_price = 100

        self.assertGreaterEqual(buy_price, sell_price)

    def test_buy_price_higher(self):
        buy_price = 110
        sell_price = 100

        self.assertGreaterEqual(buy_price, sell_price)

    def test_buy_price_lower(self):
        buy_price = 90
        sell_price = 100

        self.assertLess(buy_price, sell_price)


if __name__ == "__main__":
    unittest.main()