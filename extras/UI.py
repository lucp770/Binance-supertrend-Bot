from tkinter import *
from tkinter import ttk
import time
import tkinter.messagebox
import matplotlib.pyplot as plt                                     # Usos para a montagem do gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Importando função da matplot, para o gráfico

from datetime import datetime
import supertrend_bot
import ccxt


###########window configuration variables ##############



####################### splash screen ####################
splash  = Tk()
splash.title('Supertrend Bot')

splash.geometry("500x300")
#Hide the title bar
splash.overrideredirect(True)
splash.eval('tk::PlaceWindow . center')

#add the frame and welcome message
splash_screen = ttk.Frame(splash, padding = "10 10 10 10").pack()
ttk.Label(splash_screen,padding = "50", text = "Welcome to the Binance Supertrend Bot", font = ("Helvetica", 16)).pack()

#centralizar a interface

######################## main program ####################

def open_config_window(frame):
	
	#close initial frame #this does not work because frame 1 is not defined here.
	frame.destroy()
	main.destroy()
	#open config frame
	frame2 = ttk.Frame(main,padding = "30 70 10 10").grid(column = 0, row = 0)

	#available funds:
	funds = StringVar()
	funds_label = ttk.Label(frame2, text = "Available funds: ", padding = "30").grid(column = 0, row =0)


def check_API_key(frame):
	
	#check the validity of api key
	ApiKey = API_KEY.get()

	try:
		exchange = ccxt.binance()
		available_coins = exchange.load_markets()
		available_coins = [market for market in available_coins]
		print(available_coins)

		open_config_window(frame)
	except Exception as e:
		tkinter.messagebox.showinfo("Error", "Invalid API KEY")
		print(e)
	

	#create a ccxt instance and show balance, available coins in binance.
	pass

def open_tradding_window():
	pass

def main_window():
	splash.destroy()
	main = Tk()
	main.title('Supertrend Bot')
	main.geometry("400x300")
	main.resizable(0,0)
	main.eval('tk::PlaceWindow . center')
	frame1 = ttk.Frame(main, padding = "30 70 10 10").grid(column = 0, row = 0)

	ttk.Label(frame1,text = "Please insert a valid API key", padding = "10").grid(column = 1 , row = 0,columnspan = 2)
	#create a instance and list all the coins.

	API_key_label = ttk.Label(frame1, text = "API KEY: ").grid(column = 1, row = 1)

	global API_KEY 
	API_KEY= StringVar()
	API_KEY_Entry = ttk.Entry(frame1 , width = 18, textvariable = API_KEY)
	API_KEY_Entry.grid(column = 2, row = 1)
	API_KEY_Entry.focus()

	ttk.Button(frame1, text = "Continue", command = lambda: check_API_key(frame1)).grid(column =2, row =3, sticky = E)

	

splash.after(3000, main_window)


mainloop()



"""
class application(Tk):
	
	#call the superclass constructor
	super().__init__()
	
	self.
	
	def call_splashscreen(self):

		self.splash  = Tk()
		self.splash.title('Supertrend Bot')
		self.splash.geometry("500x300")

		#Hide the title bar
		self.splash.overrideredirect(True)
		self.splash.eval('tk::PlaceWindow . center')

		#add the frame and welcome message
		self.splash_screen = ttk.Frame(splash, padding = "10 10 10 10").pack()
		self.ttk.Label(splash_screen,padding = "50", text = "Welcome to the Binance Supertrend Bot", font = ("Helvetica", 16)).pack()

		
		splash.after(3000, lambda: splash.destroy())


	def __init__():
		#create a splashcreen for a couple of seconds.
		call_splashscreen()

		main_screen()



app = application()






"""
# class application(self, ):

