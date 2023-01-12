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


		container = tk.Frame(self, height = 400, width = 600)
		container.pack(side = "top", fill = "both", expand =True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.user_balance = ''
		self.current_price = tk.StringVar()
		self.Api_key = key
		self.Secret = secret
		# create private ccxt instance
		self.exchange = ccxt.binance({'apiKey': self.Api_key, 'secret': self.Secret, 'timeout': 30000, 'enableRateLimit': True})
		self.user_balance = self.exchange.fetchBalance()
		self.frame = Trading(container,self)
		self.frame.grid(row = 0 , column =0, sticky ="nsew")

		self.show_frame(self.frame)

	def show_frame(self, frame):
		frame.tkraise()

	def hide_frame(self,frame):
		frame.grid_forget()

	def update_data(self):
		while 1:

		# 	# get the current datan
			closing_prices,timestamp = self.get_data()

		# 	# redraw figure
			plt.clf()
			plt.plot(timestamp, closing_prices)
			fig.autofmt_xdate()
			fig.canvas.draw_idle()

			self.current_price.set(closing_prices[-1])
			print(self.current_price.get())

			self.update_idletasks()
			self.update()
			self.frame.update()
			self.frame.update_idletasks()


			print('preso no loop....')
			print(self.frame.price)
			# print(timestamp, closing_prices)
			time.sleep(0.01)

	def get_data(self, coin = 'ETH/USDT'):
		exchange = ccxt.binance()
		bars = exchange.fetch_ohlcv(coin, limit=100, timeframe='1m')
		closing_prices = [value[4] for value in bars]
		timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]

		return closing_prices, timestamp

class Trading(tk.Frame):
	self.local_price= Tradding_UI.current_price.get()
	self.price = ttk.Label(self, textvariable = local_price)

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.create_canvas(controller)

	def create_canvas(self,controller):
		ttk.Label(self, text = "Current Price: ").grid(column = 1, row = 2)

		# create canvas
		global fig
		fig = plt.figure()
		canvas = FigureCanvasTkAgg(fig, master = self)
		canvas.get_tk_widget().grid(row = 1, columnspan =  2, sticky = "nsew")

		# get the data:
		closing_prices, timestamp = self.get_data()
		local_price = controller.current_price.get()
		print('local price: ', local_price)
		global price
		self.price.grid(column = 2, row = 2)

		# plot
		plt.plot(timestamp, closing_prices)
		fig.autofmt_xdate()
		fig.canvas.draw_idle()


		print('primeiro passo')

		time.sleep(0.1)

		closing_prices,timestamp = self.get_data()

		print('indo para o segundo passo')
		plt.clf()
		plt.plot(timestamp, closing_prices)
		fig.autofmt_xdate()
		fig.canvas.draw_idle()

		# controller.update_idletasks()
		# controller.update()

		print('segundo passo concluido')

	def get_data(self, coin = 'ETH/USDT'):
		exchange = ccxt.binance()
		bars = exchange.fetch_ohlcv(coin, limit=100, timeframe='1m')
		closing_prices = [value[4] for value in bars]
		timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]

		return closing_prices, timestamp


if __name__ == "__main__":
	obj = Tradding_UI(config.API_KEY, config.API_Secret)
	obj.update_data()
	



#problema encontrado: ao remover o for loop, a inicialização do frame parece não funcionar direito.
# a funcao nao consegue ser acessada fora da classe
# tentar reescrever o método call?
