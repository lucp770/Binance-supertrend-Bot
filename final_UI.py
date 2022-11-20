import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox
import matplotlib.pyplot as plt                                     # Usos para a montagem do gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Importando função da matplot, para o gráfico
import json
from datetime import datetime
import ccxt

import Logged

class Page_managment(tk.Tk):
	"""
	this class inherits the main window object, and serves as a basis for displaying the frames
	"""
	#constructor

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		#invoque a method to name the window
		self.wm_title("Test application")
		


		container = tk.Frame(self, height = 400, width = 600)
		container.grid(column = 0 , row = 0)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight =1)

		#create a dictionary to store the frames of the application
		self.frames = {}

		# important variables used in various frames

		self.ApiKey = ''
		self.Secret = ''
		

		for F in (splash_screen,Log_in):
			frame = F(container, self)#this create the instances

			self.frames[F] = frame
			frame.grid(column = 0 , row = 0)
		self.show_frame(splash_screen)

		# insert image:
		


	def show_frame(self, page):
		#frame to show
		frame = self.frames[page]

		#show the frame
		frame.tkraise()

	def hide_frame(self, page):
		frame = self.frames[page]
		frame.grid_forget()

class splash_screen(tk.Frame):

	#constructor
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		controller.overrideredirect(True)
		ttk.Label(self, padding = "50", text = "Welcome to the Binance Supertrend Bot", font = ("Helvetica", 16)).grid(column = 1, row = 1)
		
		# bgimage = tk.PhotoImage(file = "extras/Binance_Logo.png")
		# print(dir(bgimage))
		# canvas1 = tk.Canvas(self, width = 200, height=200)
		# canvas1.grid(column = 1, row = 2, sticky ="nsew")
		# canvas1.create_image(0,0,image = bgimage, anchor = "nw")
		
		
		controller.after(3000, lambda: controller.show_frame(Log_in))
		controller.after(3000, lambda: controller.hide_frame(splash_screen))
		


class Log_in(tk.Frame):

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		controller.title("Binance Supertrend Bot ")
		controller.eval('tk::PlaceWindow . center')
		controller.geometry("600x400")
		controller.resizable(0,0)
		#creating the layout
		tk.Label(self, text = "Please insert a valid API KEY: ").grid(column = 1, row = 1, columnspan = 2,padx =" 20 0", pady = "30 10")
		
		# insert padding to position the elements.
		ttk.Label(self, text = "API key: ").grid(column  =1, row = 2, padx="20 0", sticky ="w")

		ApiKey = tk.StringVar()
		ttk.Entry(self, textvariable = ApiKey, width = 50).grid(column = 2, row = 2, padx = 20,pady = 8)


		ttk.Label(self, text = "API Secret: ").grid(column = 1, row =3,  padx="20 0", sticky = "e")

		ApiSecret = tk.StringVar()
		ttk.Entry(self, textvariable = ApiSecret, width = 50).grid(column =2, row =3)

		btn_Log_in = ttk.Button(self, text = "Log In", command = lambda: log_in()).grid(column = 2, row = 4,padx = "0 20", pady = 8, sticky = "e")

		def log_in():
			print("funcao log in")
			# get the api key
			APK = ApiKey.get()
			Secret = ApiSecret.get()
			logInObj = {'apiKey': APK, 'secret': Secret, 'timeout': 30000, 'enableRateLimit': True}
			# rate limit exist to limit the number of requeests to the exchange and not be banned
			# timeout: 
			# create a ccxt instance to validade the api key.

			try:
				exchange = ccxt.binance(logInObj)

				# trow error with credentials are missing
				exchange.checkRequiredCredentials()

				# validate the api key by checking the balance
				balance = exchange.fetchBalance()

				controller.ApiKey = APK 
				controller.Secret = Secret 

				# after checking the user data, create a new window (tk object with all the user functionalities, after it is logged in)
				new_window = Logged.Logged_UI(controller.ApiKey,controller.Secret)
				controller.destroy()
				new_window.mainloop()

				# controller.show_frame(config)
				# controller.hide_frame(Log_in)
				# controller.show_frame(config)

			except Exception as e:
				tkinter.messagebox.showinfo("Error: Invalid Credentials", "Please check the inserted credentials")
				print(e)


if __name__ == "__main__":
	obj = Page_managment()
	obj.mainloop()

# pesquisar o limite de transação.
