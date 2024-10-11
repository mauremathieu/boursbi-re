import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Define a Stock class with a price attribute and a method to update the price
class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.price_history = [price]  # Track price history
    
    def update_price(self, percentage_change):
        self.price += self.price * percentage_change
        if self.price < 1:  # Prevent prices from going below 1 unit
            self.price = 1
        self.price_history.append(self.price)  # Log price change

# Define a Market class that manages all stocks
class Market:
    def __init__(self, stocks):
        self.stocks = stocks
    
    def buy_stock(self, stock_name):
        # Find the stock to buy
        stock = next((s for s in self.stocks if s.name == stock_name), None)
        if stock:
            print(f"Buying stock: {stock.name}")
            # Update all prices after the transaction
            self.update_market(stock)
            return True
        else:
            print(f"Stock {stock_name} not found.")
            return False
    
    def update_market(self, bought_stock):
        # Price variation based on the stock bought
        variation = random.uniform(-0.05, 0.02)  # Random change in the market (between -5% and +0%)
        achat = random.uniform(0.02,0.1)
        for stock in self.stocks:
            if stock.name == bought_stock.name:
                stock.update_price(achat)  # If the stock is bought, increase its price by 10%
            else:
                stock.update_price(variation)  # Other stocks fluctuate randomly
    
    def plot_prices(self):
        plt.close()  # Close the previous plot window if it exists
        
        # Plot the price history of all stocks
        plt.figure(figsize=(10, 6))
        
        for stock in self.stocks:
            plt.plot(stock.price_history, label=stock.name)
        
        plt.title("Prix des Bières")
        plt.xlabel("Temps")
        plt.ylabel("Prix")
        plt.legend()
        plt.grid(True)

        # Display current stock prices on the plot
        for stock in self.stocks:
            plt.text(len(stock.price_history) - 1, stock.price_history[-1], 
                     f'{stock.price:.2f}', 
                     fontsize=9, 
                     verticalalignment='bottom', 
                     horizontalalignment='center')

        # Create buttons for each stock
        ax_button_area = plt.axes([0.1, 0.02, 0.8, 0.05])  # Button area at the bottom
        self.buttons = []
        for idx, stock in enumerate(self.stocks):
            ax_button = plt.axes([0.1 + idx * 0.2, 0.01, 0.18, 0.05])  # Position buttons
            button = Button(ax_button, f"Buy {stock.name}")
            button.on_clicked(lambda event, stock_name=stock.name: self.buy_and_plot(stock_name))
            self.buttons.append(button)

        plt.show()

    def buy_and_plot(self, stock_name):
        # Buy stock and update the plot
        if self.buy_stock(stock_name):
            self.plot_prices()

# Define an Agent (buyer)
class Agent:
    def __init__(self, name, market):
        self.name = name
        self.market = market

# Initialize some stocks with starting prices
stocks = [
    Stock("Chouffe", 3.5),
    Stock("Pils", 1.5),
    Stock("Kriek", 2.5),
    Stock("Stout", 2.0),
    Stock("Btest",1.2),
]

# Create a market
market = Market(stocks)

# Create an agent
agent = Agent("Martin", market)

# Run the market and display the interactive plot with buttons
if __name__ == "__main__":
    market.plot_prices()

plt.close()
plt.show()