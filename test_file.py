import unittest
from stock import Stock, Portfolio, User

class TestStockMarketManagementSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up common test data."""
        self.apple = Stock("Apple Inc.", "AAPL", 150.00)
        self.google = Stock("Alphabet Inc.", "GOOGL", 2800.00)
        self.user = User("test_user", initial_balance=10000.00)

    # Test Stock class
    def test_stock_creation(self):
        self.assertEqual(self.apple.name, "Apple Inc.")
        self.assertEqual(self.apple.ticker, "AAPL")
        self.assertEqual(self.apple.price, 150.00)

    def test_stock_update_price(self):
        self.apple.update_price(200.00)
        self.assertEqual(self.apple.price, 200.00)

    # Test Portfolio class
    def test_portfolio_buy_stock(self):
        self.user.buy_stock(self.apple, 10)
        holdings = self.user.portfolio.holdings
        self.assertIn("AAPL", holdings)
        self.assertEqual(holdings["AAPL"]["quantity"], 10)

    def test_portfolio_sell_stock(self):
        self.user.buy_stock(self.apple, 10)
        self.user.sell_stock("AAPL", 5)
        holdings = self.user.portfolio.holdings
        self.assertEqual(holdings["AAPL"]["quantity"], 5)

        # Sell all shares
        self.user.sell_stock("AAPL", 5)
        self.assertNotIn("AAPL", holdings)

    def test_portfolio_sell_nonexistent_stock(self):
        with self.assertLogs(level="INFO") as log:
            self.user.sell_stock("TSLA", 5)
        self.assertTrue(any("do not own" in message for message in log.output))

    # Test User class
    def test_user_initial_balance(self):
        self.assertEqual(self.user.balance, 10000.00)

    def test_user_buy_stock_deduct_balance(self):
        self.user.buy_stock(self.apple, 10)
        expected_balance = 10000.00 - (10 * 150.00)
        self.assertEqual(self.user.balance, expected_balance)

    def test_user_sell_stock_add_balance(self):
        self.user.buy_stock(self.apple, 10)
        self.user.sell_stock("AAPL", 5)
        expected_balance = 10000.00 - (10 * 150.00) + (5 * 150.00)
        self.assertEqual(self.user.balance, expected_balance)

    def test_user_insufficient_balance(self):
        with self.assertLogs(level="INFO") as log:
            self.user.buy_stock(self.google, 5)  # Too expensive for the balance
        self.assertTrue(any("Insufficient balance" in message for message in log.output))

    def test_user_transaction_history(self):
        self.user.buy_stock(self.apple, 10)
        self.user.sell_stock("AAPL", 5)
        self.assertEqual(len(self.user.transaction_history), 2)
        self.assertEqual(self.user.transaction_history[0].transaction_type, "BUY")
        self.assertEqual(self.user.transaction_history[1].transaction_type, "SELL")

    # Test edge cases
    def test_sell_more_than_owned(self):
        self.user.buy_stock(self.apple, 5)
        with self.assertLogs(level="INFO") as log:
            self.user.sell_stock("AAPL", 10)  # Trying to sell more than owned
        self.assertTrue(any("Not enough shares" in message for message in log.output))

    def test_update_stock_price(self):
        old_price = self.apple.price
        new_price = 175.00
        self.apple.update_price(new_price)
        self.assertNotEqual(self.apple.price, old_price)
        self.assertEqual(self.apple.price, new_price)


if __name__ == "__main__":
    unittest.main()
