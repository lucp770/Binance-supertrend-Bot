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

class Tradding_UI(tk.Tk):
	"""this class contains all the available windows when the user authentication has been confirmed."""
	def __init__(self, key,secret):
		tk.Tk.__init__(self)

		self.wm_title("Binance Supertrend Bot")

		self.user_balance = ''
		
		self.Api_key = key
		self.Secret = secret

def open_new_frame(value,key,secret):
    frame2 = ttk.Frame(root, padding = "3 3 12 12")
    frame2.grid(column=0, row=0, sticky = "nswe")
    ttk.Label(frame2, text = "LIVE TRADING ").grid(column = 1, row = 2,sticky = "nswe")
    ttk.Label(frame2, text = "Ammount alocated:  " + value).grid(column = 0, row = 3, sticky = tk.W)

    ttk.Label(frame2, text = "current price: ").grid(column = 0, row = 4, sticky = tk.W)
    current_price = tk.StringVar()
    ttk.Label(frame2, textvariable = current_price).grid(column =1, row = 4, sticky=tk.W)


    #create canvas
    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.get_tk_widget().grid(row = 1, columnspan = 2, sticky = "nswe")

    #get price data
    closing_prices, timestamp = get_data(key,secret)

    #update the canvas with the data

    plt.plot(timestamp, closing_prices)
    fig.autofmt_xdate()
    fig.canvas.draw_idle()

    #create a new loop that stop returning to the original frame
    while 1:
        #get the data again, update the graph and all the values.
        closing_prices, timestamp = get_data(key,secret)

        #redraw the figure:
        plt.clf()
        plt.plot(timestamp, closing_prices)
        fig.autofmt_xdate()
        fig.canvas.draw_idle()

        #show current prices.
        current_price.set(closing_prices[-1])

        root.update_idletasks()
        root.update()
        print('preso no loop ....')
        time.sleep(0.01)

def get_data(key, secret):
    exchange = ccxt.binance({'apiKey': key, 'secret': secret, 'timeout': 30000, 'enableRateLimit': True})
    bars=exchange.fetch_ohlcv('ETH/USDT',limit=100, timeframe='1m')
    # df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
    #
    closing_prices = [value[4] for value in bars]
    timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]
    # timestamp = datetime.fromtimestamp(timestamp/1000.0)
    # print(timestamp[:4])

    return closing_prices, timestamp


if __name__ == "__main__":
	root = Tradding_UI(config.API_KEY, config.API_Secret)
	
	key = root.Api_key
	secret = root.Secret

	# create a exchange object instance:
	exchange = ccxt.binance({'apiKey': key, 'secret': secret, 'timeout': 30000, 'enableRateLimit': True})

	open_new_frame('10',key,secret)


	
