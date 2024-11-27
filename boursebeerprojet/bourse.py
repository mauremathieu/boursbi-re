import random
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from PIL import Image
import threading

import boursebeerprojet.config as config 

# Classe action
class Stock:
    def __init__(self, name, price, min_price, color):
        self.name = name
        self.price = price
        self.min_price = min_price
        self.color = color
        self.price_history = [price]
    
    def update_price(self, change):
        self.price += change
        if self.price < self.min_price:  
            self.price = self.min_price
        self.price_history.append(self.price)

# Classe marché
class Market:
    def __init__(self, stocks):
        self.stocks = stocks
        self.fig, self.ax = plt.subplots(figsize=config.DISPLAY_SETTINGS["figsize"])
        self.fig.subplots_adjust(left=config.DISPLAY_SETTINGS["left_margin"], 
                                 right=config.DISPLAY_SETTINGS["right_margin"], 
                                 top=config.DISPLAY_SETTINGS["top_margin"], 
                                 bottom=config.DISPLAY_SETTINGS["bottom_margin"])
        self.buttons = []  
        plt.ion()

    def buy_stock(self, stock_name):
        stock = next((s for s in self.stocks if s.name == stock_name), None)
        if stock:
            self.update_market(stock)
            return True
        else:
            return False
    
    def update_market(self, bought_stock):
        var = np.array([-0.15, -0.10, 0, 0.15, 0.2])
        variation = np.random.choice(var[:3])
        achat = np.random.choice(var[3:])
        for stock in self.stocks:
            if stock.name == bought_stock.name:
                stock.update_price(achat)
            else:
                stock.update_price(variation)

    def event_crash(self, event_stock):
        var = np.array([0.1, 0.15, 0.2, 0.25])
        delta = np.random.choice(var)
        delta2 = np.random.choice(var[1:])
        for stock in self.stocks:
            if stock.name == event_stock.name:
                stock.price = max(stock.min_price + delta, stock.min_price)
                stock.price_history.append(stock.price)
            else:
                stock.update_price(delta2)

    def event_BR(self, event_stock):
        var = np.array([0.4, 0.45, 0.5, 0.55, 0.6])
        var2 = np.array([0.2, 0.25, 0.3, 0.35])
        delta = np.random.choice(var)
        for stock in self.stocks:
            if stock.name == event_stock.name:
                stock.update_price(delta)
            else:
                stock.update_price(-np.random.choice(var2))

    def plot_prices(self):
        self.ax.clear()
        for stock in self.stocks:
            history_to_display = stock.price_history[-config.PRICE_HISTORY_LENGTH:]
            x_values = np.linspace(0, len(history_to_display) - 1, len(history_to_display))
            self.ax.plot(x_values, history_to_display, label=stock.name, 
                         marker=config.DISPLAY_SETTINGS["marker"], 
                         linestyle=config.DISPLAY_SETTINGS["linestyle"], 
                         markersize=config.DISPLAY_SETTINGS["markersize"],
                         color=stock.color)
            self.ax.text(x_values[-1], history_to_display[-1], stock.name, 
                         fontsize=config.DISPLAY_SETTINGS["legend_fontsize"], 
                         verticalalignment='top', horizontalalignment='left', color=stock.color)

        self.ax.set_title(config.DISPLAY_SETTINGS["title"], 
                          fontsize=config.DISPLAY_SETTINGS["title_fontsize"], 
                          fontweight=config.DISPLAY_SETTINGS["title_fontweight"])
        self.ax.grid(True, linestyle=config.DISPLAY_SETTINGS["grid_linestyle"], linewidth=config.DISPLAY_SETTINGS["grid_linewidth"])
        self.ax.set_xlim(left=0)
        for stock in self.stocks:
            history_to_display = stock.price_history[-config.PRICE_HISTORY_LENGTH:]
            x_values = np.linspace(0, len(history_to_display) - 1, len(history_to_display))
            self.ax.text(x_values[-1], history_to_display[-1], 
                         f'{stock.price:.2f}€', fontsize=config.DISPLAY_SETTINGS["text_fontsize"], 
                         verticalalignment='bottom', horizontalalignment='left', color=stock.color)
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()

    def setup_buttons(self):
        for idx, stock in enumerate(self.stocks):
            ax_button_buy = plt.axes([0.1 + idx * 0.2, 0.01, 0.15, 0.05])
            button_buy = Button(ax_button_buy, f"Achat {stock.name}", color=stock.color)
            button_buy.on_clicked(lambda event, stock_name=stock.name: self.buy_and_plot(stock_name))
            self.buttons.append(button_buy)

            ax_button_crash = plt.axes([0.01, 0.8 - idx * 0.2, 0.1, 0.05])
            button_crash = Button(ax_button_crash, f"Crash {stock.name}", color=stock.color)
            button_crash.on_clicked(lambda event, stock_obj=stock: self.crash_event_and_plot(stock_obj))
            self.buttons.append(button_crash)

            ax_button_bullrun = plt.axes([0.01, 0.85 - idx * 0.2, 0.1, 0.05])
            button_bullrun = Button(ax_button_bullrun, f"BR {stock.name}", color=stock.color)
            button_bullrun.on_clicked(lambda event, stock_obj=stock: self.bullrun_event_and_plot(stock_obj))
            self.buttons.append(button_bullrun)

    def buy_and_plot(self, stock_name):
        if self.buy_stock(stock_name):
            self.plot_prices()

    def crash_event_and_plot(self, stock_obj):
        self.event_crash(stock_obj)
        self.plot_prices()

    def bullrun_event_and_plot(self, stock_obj):
        self.event_BR(stock_obj)
        self.plot_prices()

    def start_auto_variation(self):
        def vary_prices():
            while True:
                for stock in self.stocks:
                    stock.update_price(random.choice([-0.05, 0, 0.05]))
                self.plot_prices()
                time.sleep(config.TIME_INTERVAL)
        
        thread = threading.Thread(target=vary_prices)
        thread.daemon = True
        thread.start()

# classe acheteur
class Agent:
    def __init__(self, name, market):
        self.name = name
        self.market = market

# Simulation
if __name__ == "__main__":
    config.market.plot_prices()
    config.market.setup_buttons()
    config.market.start_auto_variation()
    plt.show(block=True)