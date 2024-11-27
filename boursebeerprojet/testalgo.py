import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

# Classe action
class Stock:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.price_history = [price]
    
    def update_price(self, change):
        self.price += change
        if self.price < 1:  
            self.price = 1
        self.price_history.append(self.price)

# Classe marché
class Market:
    def __init__(self, stocks):
        self.stocks = stocks
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  #initialisation figure
        self.buttons = []  
        plt.ion()  #affichage live
    
    def buy_stock(self, stock_name):
        stock = next((s for s in self.stocks if s.name == stock_name), None)
        if stock:
            print(f"Buying stock: {stock.name}")
            # maj achat
            self.update_market(stock)
            return True
        else:
            print(f"Stock {stock_name} not found.")
            return False
    
    def update_market(self, bought_stock):
        var = np.array([-0.1, -0.05, 0, 0.05, 0.1])
        variation = np.random.choice(var[:3])  # fluctu autres
        achat = np.random.choice(var[3:])  # fluctu achat
        for stock in self.stocks:
            if stock.name == bought_stock.name:
                stock.update_price(achat)  # update
            else:
                stock.update_price(variation)  # update
    
    def event_crash(self, event_stock):
    
        var = np.array([0.05, 0.1, 0.15, 0.2])
        delta = np.random.choice(var)   #fluctu crash
        delta2 = np.random.choice(var[:1])  # fluctu autres
        for stock in self.stocks:
            if stock.name == event_stock.name:
                stock.price = max(1 + delta, 1)  # update
            else:
                stock.update_price(delta2)  # update
            stock.price_history.append(stock.price)  # log

    def event_BR(self, event_stock):
    
        var = np.array([0.4, 0.45, 0.5, 0.55, 0.6])
        var2 = np.array([0.2, 0.25, 0.3, 0.35])
        delta = np.random.choice(var) #fluctu bull run
        for stock in self.stocks:
            if stock.name == event_stock.name:
               stock.price = max(stock.price + delta, 1)  # update
            else:
                stock.update_price(-np.random.choice(var2))  # update
            stock.price_history.append(stock.price)  # log


    def plot_prices(self):
        self.ax.clear()  # Clear 
        # Plot 
        for stock in self.stocks:
            self.ax.plot(stock.price_history, label=stock.name)
        
        self.ax.set_title("Prix des Bières")
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Prix")
        self.ax.legend()
        self.ax.grid(True)
        
        # affichage prix
        for stock in self.stocks:
            self.ax.text(len(stock.price_history) - 1, stock.price_history[-1], 
                         f'{stock.price:.2f}', fontsize=9, 
                         verticalalignment='bottom', horizontalalignment='center')
        

        #affichage logo
        logo_path = "logo.png"  
        logo_image = Image.open(logo_path)
        imagebox = OffsetImage(logo_image, zoom=0.05)   #ajuster la taille
    
        #placement
        ab = AnnotationBbox(imagebox, (1, 1), frameon=False, 
                            xycoords='axes fraction', box_alignment=(-0.1, 6.5)) #position %axes
        self.ax.add_artist(ab)

        self.fig.canvas.draw_idle()  # refresh canva
        self.fig.canvas.flush_events()  # GUI update
    


    def setup_buttons(self):
        #boutons
        for idx, stock in enumerate(self.stocks):
        # boutons achats
            ax_button_buy = plt.axes([0.1 + idx * 0.2, 0.001, 0.18, 0.035])  # Position buy button
            button_buy = Button(ax_button_buy, f"Achat {stock.name}")
            button_buy.on_clicked(lambda event, stock_name=stock.name: self.buy_and_plot(stock_name))
            self.buttons.append(button_buy)

        # boutons crash
            ax_button_crash = plt.axes([0.001, 0.8 - idx * 0.2, 0.085, 0.05])  # Position crash button
            button_crash = Button(ax_button_crash, f"Crash {stock.name}")
            button_crash.on_clicked(lambda event, stock_obj=stock: self.crash_event_and_plot(stock_obj))
            self.buttons.append(button_crash)

        # boutons bull run
            ax_button_bullrun = plt.axes([0.9, 0.8 - idx * 0.2, 0.1, 0.05])  # Position bull run button
            button_bullrun = Button(ax_button_bullrun, f"BR {stock.name}")
            button_bullrun.on_clicked(lambda event, stock_obj=stock: self.bullrun_event_and_plot(stock_obj))
            self.buttons.append(button_bullrun)

    
    def buy_and_plot(self, stock_name):
        # achète plot
        if self.buy_stock(stock_name):
            self.plot_prices()

    def crash_event_and_plot(self, stock_obj):
        #crash plot
        self.event_crash(stock_obj)
        self.plot_prices()

    def bullrun_event_and_plot(self, stock_obj):
        #bull run plot
        self.event_BR(stock_obj)
        self.plot_prices()


# classe acheteur
class Agent:
    def __init__(self, name, market):
        self.name = name
        self.market = market

# prix initiaux
stocks = [
    Stock("Chouffe", 1.5),
    Stock("Pils", 1.5),
    Stock("Kriek", 1.5),
    Stock("Stout", 1.5),
]

market = Market(stocks)

agent = Agent("Martin", market)

# Simulation
if __name__ == "__main__":
    market.plot_prices()  # plot initial
    market.setup_buttons()  # ajouts boutons
    plt.show(block=True)  # maintenir display


# à ajouter ? 
#prix max
#revoir les prix mins et max avec bureau