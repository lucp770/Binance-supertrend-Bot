import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox
import matplotlib.pyplot as plt                                     # Usos para a montagem do gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Importando função da matplot, para o gráfico
import json
from datetime import datetime
import supertrend_bot
import ccxt
import config
import pandas as pd

class Tradding_UI(tk.Tk):
    def __init__(self, key,secret,coin ='ETH/USDT'):
        tk.Tk.__init__(self)
        self.wm_title("Binance Supertrend Bot")
        self.selected_coin = coin
        self.user_balance = ''
        self.Api_key = key
        self.Secret = secret

def open_new_frame(value,key,secret, coin = "ETH/USDT"):
    frame2 = ttk.Frame(root, padding = "3 3 12 12")
    frame2.grid(column=0, row=0, sticky = "nswe")
    ttk.Label(frame2, text = "LIVE TRADING ").grid(column = 0,columnspan = 2, row = 2,sticky = "nswe")
    ttk.Label(frame2, text = "Ammount alocated:  " + value).grid(column = 0, row = 3, sticky = tk.W)

    ttk.Label(frame2, text = "current price: ").grid(column = 0, row = 4, sticky = "w")
    current_price = tk.StringVar()
    ttk.Label(frame2, textvariable = current_price).grid(column =1, row = 4, sticky=tk.W)


    #create canvas
    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.get_tk_widget().grid(row = 1, columnspan = 2, sticky = "nswe", padx=5, pady = 5)

    #get price data
    prices_dataframe = get_data(key,secret)

    #update the canvas with the data
    generate_candlesticks(prices_dataframe, fig)

    # fig.autofmt_xdate()
    # fig.canvas.draw_idle()

    #create a new loop that stop returning to the original frame
    while 1:
        #get the data again, update the graph and all the values.
        prices_dataframe = get_data(key,secret)

        #redraw the figure:
        plt.clf()
        generate_candlesticks(prices_dataframe, fig, coin)
        # plt.plot(timestamp, closing_prices)
        # fig.autofmt_xdate()
        # fig.canvas.draw_idle()

        #show current prices.
        price = prices_dataframe['close'].values[-1]
        current_price.set(prices_dataframe['close'].values[-1])

        root.update_idletasks()
        root.update()
        print('preso no loop ....')
        print(price)
        time.sleep(0.01)

def get_data(key, secret, coin = "ETH/USDT"):
    exchange = ccxt.binance({'apiKey': key, 'secret': secret, 'timeout': 30000, 'enableRateLimit': True})
    bars=exchange.fetch_ohlcv(coin,limit=50, timeframe='1m')
    df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
    df['timestamp'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x/1000.0))
    #
    # closing_prices = [value[4] for value in bars]
    # timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]
    # timestamp = datetime.fromtimestamp(timestamp/1000.0)
    # print(timestamp[:4])

    return df

def generate_candlesticks(dataframe, pltfigure, coin = "ETH/USDT"):

    # define the width of the candlesticks elements
    width_bar = .4
    width_line = .05

    # the two types of bars
    green_bars = dataframe[dataframe.close > dataframe.open]
    red_bars  = dataframe[dataframe.close < dataframe.open]

    # create the green bars: the arguments are (position , lenght of the bar, width of the bar,y coordinate of the bottom , color )
    plt.bar(green_bars.index, green_bars.close - green_bars.open, width_bar, bottom  = green_bars.open, color = "green")
    plt.bar(green_bars.index, green_bars.high - green_bars.close, width_line, bottom  = green_bars.close, color = "green")
    plt.bar(green_bars.index, green_bars.low - green_bars.open, width_line, bottom  = green_bars.open, color = "green")
    
    index_labels = []
    date_labels = []
    for i in green_bars.index:
        if i%5 ==0:
            date_labels.append(green_bars.timestamp[i].time())
            index_labels.append(i)
    
    for i in red_bars.index:
        if i%5==0:
            date_labels.append(red_bars.timestamp[i].time())
            index_labels.append(i)

    plt.xticks(index_labels, date_labels)

    # create the red bars: 
    plt.bar(red_bars.index, red_bars.close - red_bars.open, width_bar, bottom  = red_bars.open, color = "red")
    plt.bar(red_bars.index, red_bars.high - red_bars.close, width_line, bottom  = red_bars.close, color = "red")
    plt.bar(red_bars.index, red_bars.low - red_bars.open, width_line, bottom  = red_bars.open, color = "red")


    plt.title(coin)
    plt.ylabel("Price")

    pltfigure.autofmt_xdate()
    pltfigure.canvas.draw_idle()


if __name__ == "__main__":
	root = Tradding_UI(config.API_KEY, config.API_Secret)
	
	key = root.Api_key
	secret = root.Secret

	# create a exchange object instance:
	exchange = ccxt.binance({'apiKey': key, 'secret': secret, 'timeout': 30000, 'enableRateLimit': True})

	open_new_frame('10',key,secret)


	
