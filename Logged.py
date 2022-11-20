#this class contains the tk window with the functionalities when the user is logged in.
import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox
import matplotlib.pyplot as plt                                     # Usos para a montagem do gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Importando função da matplot, para o gráfico
import json
from datetime import datetime
import ccxt
import re
import Trad
import config


class Logged_UI(tk.Tk):
	"""this class contains all the available windows when the user authentication has been confirmed."""
	def __init__(self, key,secret):
		tk.Tk.__init__(self)

		self.wm_title("Binance Supertrend Bot")
		self.geometry("400x400")
		self.eval('tk::PlaceWindow . center')

		container = tk.Frame(self, height = 400, width = 600)
		container.grid(column = 0 , row = 0)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)


		self.frames = {}
		self.user_balance = ''

		self.Api_key = key
		self.Secret = secret

		# create private ccxt instance
		self.exchange = ccxt.binance({'apiKey': self.Api_key, 'secret': self.Secret, 'timeout': 30000, 'enableRateLimit': True})

		self.user_balance = self.exchange.fetchBalance()

		self.frame = Configuration(container,self)
		self.frame.grid(row = 0 , column =0, sticky ="nsew")

		# for F in (config):
		# 	frame = F(container,self)

		# 	self.frames[F] = frame
		# 	frame.grid(row = 0 , column =0, sticky ="nsew")

		self.show_frame(self.frame)

	def show_frame(self, frame):
		frame.tkraise()

	def hide_frame(self,tel):
		frame = self.frames[tel]
		frame.grid_forget()


class Configuration(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)


		ttk.Label(self, text = "Selected the tradding configurations: ").grid(column = 1, row = 1, columnspan =2, pady = 10)

		# get the user balance

		user_funds = self.get_user_funds(controller)[0]
		
		ttk.Label(self, text = "User available Balance: " ).grid(column = 1, row = 2, pady = "20 10", padx = "10 0", sticky="w")
		ttk.Label(self, text = user_funds).grid( column = 2, row = 2, pady = "20 10",  padx = "10 0", sticky="w")

		ttk.Label(self, text = "Select crypto: ").grid(column = 1, row = 3, pady ="10 10",  padx = "10 0", sticky="w")

		self.selecteded_currency = tk.StringVar()
		currencies = self.get_available_currencies()

		selected_currency = ttk.Combobox(self, textvariable = self.selecteded_currency, values =currencies ).grid(column = 2, row = 3,sticky="w", padx = "10 0")
		

		# amount to trade:

		ttk.Label(self, text = "type the amount to trade: ").grid(column = 1, row = 4, pady ="10 10", padx = "10 0", sticky="w")
		self.Amount = tk.StringVar()
		ttk.Entry(self, textvariable = self.Amount).grid(column  =2, row = 4, sticky = "e")


		#Start Button
		ttk.Button(self, text = "Start Trading", command = lambda: self.start_trading(controller) ).grid(column = 2, row = 5, sticky = "e")

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
			tradding_window = Trad.Tradding_UI(controller.Api_key,controller.Secret, selected)
			controller.destroy()

		else: tkinter.messagebox.showinfo("Error: Insulficient funds", "Please check if you have available coin to operate in the selected market")


		# if yes then:
			# show_frame(Trading)
			# invoque function to create the canvas and input in the screen.



if __name__ == "__main__":
	obj = Logged_UI(config.API_KEY, config.API_Secret)
	obj.mainloop()
