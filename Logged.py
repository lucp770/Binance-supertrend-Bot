#this class contains the tk window with the functionalities when the user is logged in.
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
import re


class Logged_UI(tk.Tk):
	"""this class contains all the available windows when the user authentication has been confirmed."""
	def __init__(self, key,secret):
		tk.Tk.__init__(self)

		self.wm_title("Binance Supertrend Bot")

		container = tk.Frame(self, height = 400, width = 600)
		container.pack(side = "top", fill = "both", expand =True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)


		self.frames = {}
		self.user_balance = ''

		self.Api_key = key
		self.Secret = secret

		# create private ccxt instance
		self.exchange = ccxt.binance({'apiKey': self.Api_key, 'secret': self.Secret, 'timeout': 30000, 'enableRateLimit': True})

		self.user_balance = self.exchange.fetchBalance()


		for F in (config, Trading):
			frame = F(container,self)

			self.frames[F] = frame
			frame.grid(row = 0 , column =0, sticky ="nsew")

		self.show_frame(config)

	def show_frame(self, tel):
		frame =self.frames[tel]
		frame.tkraise()

	def hide_frame(self,tel):
		frame = self.frames[tel]
		frame.grid_forget()




class config(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)


		ttk.Label(self, text = "Configure Screen").grid(column = 1, row = 1)

		# get the user balance

		user_funds = self.get_user_funds(controller)[0]
		
		ttk.Label(self, text = "User available Balance: " ).grid(column = 1, row = 2)
		ttk.Label(self, text = user_funds).grid( column = 2, row = 2)

		ttk.Label(self, text = "Select crypto: ").grid(column = 1, row = 3)

		self.selecteded_currency = tk.StringVar()
		currencies = self.get_available_currencies()

		selected_currency = ttk.Combobox(self, textvariable = self.selecteded_currency, values =currencies ).grid(column = 2, row = 3)
		

		# amount to trade:

		ttk.Label(self, text = "type the amount to trade: ").grid(column = 1, row = 4)
		self.Amount = tk.StringVar()
		ttk.Entry(self, textvariable = self.Amount).grid(column  =2, row = 4)


		#Start Button
		ttk.Button(self, text = "Start Trading", command = lambda: self.start_trading(controller) ).grid(column = 2, row = 5)

	def get_available_currencies(self):
		exchange = ccxt.binance()
		markets = [market for market in exchange.load_markets()]
		return markets

	def get_user_funds(self,controller):
		# create a valid instance of ccxt private
		#retrieves a list. 
		balance = controller.user_balance
		balance = balance['free']

		non_zero = [(i,j) for i,j in balance.items() if j != 0.0 ]
		user_funds = json.dumps(non_zero)
		return [user_funds, non_zero]

	def start_trading(self,controller):

		# checks if selected pair, correspond to user funds.
		non_zero = self.get_user_funds(controller)[1]

		# get the selected value on the combobox.
		selected = self.selecteded_currency.get()
		Amount = self.Amount.get()

		print('non_zero: ', non_zero, '\n \n selected: ',selected)

		# use re to get the coin to sell.
		second_pair = re.split("/",selected)[1]
		print(second_pair)

		user_can_trade = False
		# checks if the coin is in the user balance.

		for i in non_zero:
			print(i[0])
			if i[0] ==second_pair and float(i[1]) >= float(Amount):
				print('Match!!')

				print('Amount selected: ', Amount)

				print('non_zero[1]', i[1])
				user_can_trade = True


		if user_can_trade:
			print('\n \n........start tradding')
	
			# create the tradding window.

		else: tkinter.messagebox.showinfo("Error: Insulficient funds", "Please check if you have available coin to operate in the selected market")


		# if yes then:
			# show_frame(Trading)
			# invoque function to create the canvas and input in the screen.

class Trading(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

	def create_canvas(self):
		# create canvas
		fig = plt.figure()
		canvas = FigureCanvasTkAgg(fig, master = self)
		canvas.get_tk_widget().grid(row = 1, columnspan =  2, sticky = "nsew")

		# get the data:
		closing_prices, timestamp = self.get_data()

		# plot
		plt.plot(timestamp, closing_prices)
		fig.autofmt_xdate()
		fig.canvas.draw_idle()

		# create the trading loop
		while 1:

			# get the current data
			closing_prices,timestamp = get_data()

			# redraw figure
			plt.clf()
			plt.plot(timestamp, closing_prices)
			fig.autofmt_xdate()
			fig.canvas.draw_idle()

			#here we create our trading strategie.

	def get_data(self, coin = 'ETH/USDT'):
		exchange = ccxt.binance()
		bars = exchange.fetch_ohlcv(coin, limit=100, timeframe='1m')
		closing_prices = [value[4] for value in bars]
		timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]

		return closing_prices, timestamp 

if __name__ == "__main__":
	obj = Logged_UI('dthjzdvBJHYUJkZebr4QOmv4HmhfYG7NUVuhOG5pApVWSfZNuvZKq8Ybsg9TIdR6','87EYMXsZOLgPHBa8Ilp5XisnWenuzZN8gOT7TKjroAjLlSvKtEiE3TjbDp2yRhi6')
	obj.mainloop()
