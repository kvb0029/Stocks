import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Stock:
    """Represents a stock with a name, ticker, and price."""
    def __init__(self, name, ticker, price):
        self.name = name
        self.ticker = ticker
        self.price = price

    def update_price(self, new_price):
        """Updates the stock's price."""
        self.price = new_price

    def __str__(self):
        """String representation of the stock."""
        return f"{self.name} ({self.ticker}): ${self.price:.2f}"

class DStockOperations:
    """ functions related to stock management."""

    @staticmethod
    def analyze_stock(stock):
        """function to analyze stock (returns nothing)."""
        logging.info(f"Analyzing {stock.name} ({stock.ticker}). This is a placeholder function.")

    @staticmethod
    def compare_stocks(stock1, stock2):
        logging.info(f"Comparing {stock1.name} ({stock1.ticker}) with {stock2.name} ({stock2.ticker}).")

    @staticmethod
    def predict_stock_performance(stock):
        logging.info(f"Predicting performance for {stock.name} ({stock.ticker}).")


class Portfolio:
    """Manages a collection of stocks owned by a user."""
    def __init__(self):
        self.holdings = {}  # {ticker: {'stock': Stock, 'quantity': int}}

    def buy_stock(self, stock, quantity):
        """Adds stocks to the portfolio."""
        if stock.ticker in self.holdings:
            self.holdings[stock.ticker]['quantity'] += quantity
        else:
            self.holdings[stock.ticker] = {'stock': stock, 'quantity': quantity}
        logging.info(f"Bought {quantity} shares of {stock.name} ({stock.ticker}).")

    def sell_stock(self, ticker, quantity):
        """Removes stocks from the portfolio."""
        if ticker not in self.holdings:
            logging.info(f"You do not own any shares of {ticker}.")
            return
        if self.holdings[ticker]['quantity'] < quantity:
            logging.info(f"Not enough shares to sell. You own {self.holdings[ticker]['quantity']} shares.")
            return

        self.holdings[ticker]['quantity'] -= quantity
        if self.holdings[ticker]['quantity'] == 0:
            del self.holdings[ticker]
        logging.info(f"Sold {quantity} shares of {ticker}.")

    def view_portfolio(self):
        """Displays the portfolio."""
        if not self.holdings:
            logging.info("Portfolio is empty.")
            return

        logging.info("\nPortfolio:")
        for ticker, details in self.holdings.items():
            stock = details['stock']
            quantity = details['quantity']
            value = stock.price * quantity
            logging.info(f"{stock.name} ({ticker}) - {quantity} shares @ ${stock.price:.2f} each, Total Value: ${value:.2f}")
        logging.info("")


class Transaction:
    """Represents a transaction for buying or selling stocks."""
    def __init__(self, stock, quantity, price, transaction_type):
        self.stock = stock
        self.quantity = quantity
        self.price = price
        self.transaction_type = transaction_type  # "BUY" or "SELL"
        self.date = datetime.datetime.now()

    def __str__(self):
        """String representation of the transaction."""
        return f"[{self.date.strftime('%Y-%m-%d %H:%M:%S')}] {self.transaction_type}: {self.quantity} shares of {self.stock.ticker} @ ${self.price:.2f}"


class User:
    """Represents a user with a portfolio and transaction history."""
    def __init__(self, username, initial_balance=10000.0):
        self.username = username
        self.balance = initial_balance
        self.portfolio = Portfolio()
        self.transaction_history = []

    def buy_stock(self, stock, quantity):
        """Buys stocks and adds to portfolio."""
        cost = stock.price * quantity
        if cost > self.balance:
            logging.info(f"Insufficient balance to buy {quantity} shares of {stock.name} ({stock.ticker}).")
            return

        self.balance -= cost
        self.portfolio.buy_stock(stock, quantity)
        transaction = Transaction(stock, quantity, stock.price, "BUY")
        self.transaction_history.append(transaction)

    def sell_stock(self, ticker, quantity):
        """Sells stocks and removes from portfolio."""
        if ticker not in self.portfolio.holdings:
            logging.info(f"You do not own any shares of {ticker}.")
            return

        stock = self.portfolio.holdings[ticker]['stock']
        earnings = stock.price * quantity
        self.balance += earnings
        self.portfolio.sell_stock(ticker, quantity)
        transaction = Transaction(stock, quantity, stock.price, "SELL")
        self.transaction_history.append(transaction)

    def view_portfolio(self):
        """Displays the user's portfolio."""
        self.portfolio.view_portfolio()

    def view_balance(self):
        """Displays the user's balance."""
        logging.info(f"Current Balance: ${self.balance:.2f}")

    def view_transaction_history(self):
        """Displays the user's transaction history."""
        if not self.transaction_history:
            logging.info("No transactions yet.")
            return

        logging.info("\nTransaction History:")
        for transaction in self.transaction_history:
            logging.info(transaction)
        logging.info("")


def main():
    # Predefined stocks
    stocks = {
        "AAPL": Stock("Apple Inc.", "AAPL", 175.50),
        "GOOGL": Stock("Alphabet Inc.", "GOOGL", 2800.00),
        "TSLA": Stock("Tesla Inc.", "TSLA", 750.25),
        "AMZN": Stock("Amazon Inc.", "AMZN", 3400.00),
    }

    logging.info("Welcome to the Stock Market Management System!")
    username = input("Enter your username: ")
    user = User(username)

    while True:
        logging.info("\nMenu:")
        logging.info("1. View Available Stocks")
        logging.info("2. Buy Stock")
        logging.info("3. Sell Stock")
        logging.info("4. View Portfolio")
        logging.info("5. View Balance")
        logging.info("6. View Transaction History")
        logging.info("7. Update Stock Prices")
        logging.info("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            logging.info("\nAvailable Stocks:")
            for stock in stocks.values():
                logging.info(stock)

        elif choice == "2":
            ticker = input("Enter the stock ticker to buy: ").upper()
            if ticker not in stocks:
                logging.info("Invalid stock ticker.")
                continue
            try:
                quantity = int(input("Enter the quantity to buy: "))
                if quantity <= 0:
                    logging.info("Quantity must be greater than zero.")
                    continue
            except ValueError:
                logging.info("Invalid quantity.")
                continue

            user.buy_stock(stocks[ticker], quantity)

        elif choice == "3":
            ticker = input("Enter the stock ticker to sell: ").upper()
            try:
                quantity = int(input("Enter the quantity to sell: "))
                if quantity <= 0:
                    logging.info("Quantity must be greater than zero.")
                    continue
            except ValueError:
                logging.info("Invalid quantity.")
                continue

            user.sell_stock(ticker, quantity)

        elif choice == "4":
            user.view_portfolio()

        elif choice == "5":
            user.view_balance()

        elif choice == "6":
            user.view_transaction_history()

        elif choice == "7":
            ticker = input("Enter the stock ticker to update: ").upper()
            if ticker not in stocks:
                logging.info("Invalid stock ticker.")
                continue
            try:
                new_price = float(input("Enter the new price: "))
                if new_price <= 0:
                    logging.info("Price must be greater than zero.")
                    continue
            except ValueError:
                logging.info("Invalid price.")
                continue

            stocks[ticker].update_price(new_price)
            logging.info(f"Updated {ticker} price to ${new_price:.2f}")

        elif choice == "8":
            logging.info("Exiting the system. Goodbye!")
            break

        else:
            logging.info("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
