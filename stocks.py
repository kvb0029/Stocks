import datetime


class Stock:
    def __init__(self, name, ticker, price):
        self.name = name
        self.ticker = ticker
        self.price = price

    def update_price(self, new_price):
        self.price = new_price

    def __str__(self):
        return f"{self.name} ({self.ticker}): ${self.price:.2f}"


class Portfolio:
    def __init__(self):
        self.holdings = {}  # {ticker: {'stock': Stock, 'quantity': int}}

    def buy_stock(self, stock, quantity):
        if stock.ticker in self.holdings:
            self.holdings[stock.ticker]['quantity'] += quantity
        else:
            self.holdings[stock.ticker] = {'stock': stock, 'quantity': quantity}
        print(f"Bought {quantity} shares of {stock.name} ({stock.ticker}).")

    def sell_stock(self, ticker, quantity):
        if ticker not in self.holdings:
            print(f"You do not own any shares of {ticker}.")
            return
        if self.holdings[ticker]['quantity'] < quantity:
            print(f"Not enough shares to sell. You own {self.holdings[ticker]['quantity']} shares.")
            return

        self.holdings[ticker]['quantity'] -= quantity
        if self.holdings[ticker]['quantity'] == 0:
            del self.holdings[ticker]
        print(f"Sold {quantity} shares of {ticker}.")

    def view_portfolio(self):
        if not self.holdings:
            print("Portfolio is empty.")
            return

        print("\nPortfolio:")
        for ticker, details in self.holdings.items():
            stock = details['stock']
            quantity = details['quantity']
            value = stock.price * quantity
            print(f"{stock.name} ({ticker}) - {quantity} shares @ ${stock.price:.2f} each, Total Value: ${value:.2f}")
        print()


class Transaction:
    def __init__(self, stock, quantity, price, transaction_type):
        self.stock = stock
        self.quantity = quantity
        self.price = price
        self.transaction_type = transaction_type  # "BUY" or "SELL"
        self.date = datetime.datetime.now()

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d %H:%M:%S')}] {self.transaction_type}: {self.quantity} shares of {self.stock.ticker} @ ${self.price:.2f}"


class User:
    def __init__(self, username, initial_balance=10000.0):
        self.username = username
        self.balance = initial_balance
        self.portfolio = Portfolio()
        self.transaction_history = []

    def buy_stock(self, stock, quantity):
        cost = stock.price * quantity
        if cost > self.balance:
            print(f"Insufficient balance to buy {quantity} shares of {stock.name} ({stock.ticker}).")
            return

        self.balance -= cost
        self.portfolio.buy_stock(stock, quantity)
        transaction = Transaction(stock, quantity, stock.price, "BUY")
        self.transaction_history.append(transaction)

    def sell_stock(self, ticker, quantity):
        if ticker not in self.portfolio.holdings:
            print(f"You do not own any shares of {ticker}.")
            return

        stock = self.portfolio.holdings[ticker]['stock']
        earnings = stock.price * quantity
        self.balance += earnings
        self.portfolio.sell_stock(ticker, quantity)
        transaction = Transaction(stock, quantity, stock.price, "SELL")
        self.transaction_history.append(transaction)

    def view_portfolio(self):
        self.portfolio.view_portfolio()

    def view_balance(self):
        print(f"Current Balance: ${self.balance:.2f}")

    def view_transaction_history(self):
        if not self.transaction_history:
            print("No transactions yet.")
            return

        print("\nTransaction History:")
        for transaction in self.transaction_history:
            print(transaction)
        print()


def main():
    # Predefined stocks
    stocks = {
        "AAPL": Stock("Apple Inc.", "AAPL", 175.50),
        "GOOGL": Stock("Alphabet Inc.", "GOOGL", 2800.00),
        "TSLA": Stock("Tesla Inc.", "TSLA", 750.25),
        "AMZN": Stock("Amazon Inc.", "AMZN", 3400.00),
    }

    print("Welcome to the Stock Market Management System!")
    username = input("Enter your username: ")
    user = User(username)

    while True:
        print("\nMenu:")
        print("1. View Available Stocks")
        print("2. Buy Stock")
        print("3. Sell Stock")
        print("4. View Portfolio")
        print("5. View Balance")
        print("6. View Transaction History")
        print("7. Update Stock Prices")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            print("\nAvailable Stocks:")
            for stock in stocks.values():
                print(stock)

        elif choice == "2":
            ticker = input("Enter the stock ticker to buy: ").upper()
            if ticker not in stocks:
                print("Invalid stock ticker.")
                continue
            try:
                quantity = int(input("Enter the quantity to buy: "))
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid quantity.")
                continue

            user.buy_stock(stocks[ticker], quantity)

        elif choice == "3":
            ticker = input("Enter the stock ticker to sell: ").upper()
            try:
                quantity = int(input("Enter the quantity to sell: "))
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid quantity.")
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
                print("Invalid stock ticker.")
                continue
            try:
                new_price = float(input("Enter the new price: "))
                if new_price <= 0:
                    print("Price must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid price.")
                continue

            stocks[ticker].update_price(new_price)
            print(f"Updated {ticker} price to ${new_price:.2f}")

        elif choice == "8":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()