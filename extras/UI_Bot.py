from tkinter import *
from tkinter import ttk
import time
import tkinter.messagebox
import matplotlib.pyplot as plt                                     # Usos para a montagem do gráfico
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg     # Importando função da matplot, para o gráfico

from datetime import datetime

import supertrend_bot
import ccxt


########################################## FUNCTIONS ########################################
def get_data():
    exchange = ccxt.binance()
    bars=exchange.fetch_ohlcv('ETH/USDT',limit=100, timeframe='1m')
    # df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
    #
    closing_prices = [value[4] for value in bars]
    timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]
    # timestamp = datetime.fromtimestamp(timestamp/1000.0)
    # print(timestamp[:4])

    return closing_prices, timestamp

def open_new_frame(value):
    frame2 = ttk.Frame(root, padding = "3 3 12 12")
    frame2.grid(column=0, row=0, sticky = (N,W,E,S))
    ttk.Label(frame2, text = "LIVE TRADING ").grid(column = 1, row = 2,sticky =(N,W,E,S))
    ttk.Label(frame2, text = "Ammount alocated:  " + value).grid(column = 0, row = 3, sticky = W)

    ttk.Label(frame2, text = "current price: ").grid(column = 0, row = 4, sticky = W)
    current_price = StringVar()
    ttk.Label(frame2, textvariable = current_price).grid(column =1, row = 4, sticky=W)


    #create canvas
    fig = plt.figure()
    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.get_tk_widget().grid(row = 1, columnspan = 2, sticky =(N,W,E,S))

    #destroy frame 1
    frame1.destroy()

    root.geometry('650x600')

    #get price data
    closing_prices, timestamp = get_data()

    #update the canvas with the data

    plt.plot(timestamp, closing_prices)
    fig.autofmt_xdate()
    fig.canvas.draw_idle()

    #create a new loop that stop returning to the original frame
    while 1:
        #get the data again, update the graph and all the values.
        closing_prices, timestamp = get_data()

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

def Log_in():
    """
    should close the log_in frame and open the start frame
    """
    key = API_KEY.get()
    value = Ammount.get()
    positioned =False#need to check whether or not it is positioned before start tradding.


    if key =="a":
        print("open new frame, destroy previous")
        print(value)

        open_new_frame(value)
        #in reality this need  to try to construc a instance of exchange and only accept this if the key is valid
    else:
        tkinter.messagebox.showinfo("Error", "Invalid API KEY")
        print("invalid key")    
    

###################################### GRAPHICAL INTERFACE ######################################


root = Tk()
root.title('Supertrend Bot')
root.geometry("300x200")
#centralizar a interface


#________________________Frame 0 : Loading page______________________________#

frame0 = ttk.Frame(root, padding = "3 3 12 12")
frame0.grid( column = 0, row = 0)
ttk.Label(frame0, text = "Welcome to the Binance supertrend tradding Bot").grid(column = 1, row =1, sticky = (N,W,E,S))
time.sleep(30)

frame0.destroy()






#_________________________Frame 1: Insert valid API KEY_____________________#




#______________________Frame 2: show user balance, and chose crypto to trade __________#







#______________________Frame 3: Live trading screeen ___________________________________#


frame1 = ttk.Frame(root,padding="3 3 12 12" )
frame1.grid(column =0, row = 0, sticky =(N,W,E,S))
root.columnconfigure(0,weight = 1)
root.rowconfigure(0,weight=1)
#first row: API_KEY
ttk.Label(frame1, text = "API KEY : ").grid(column = 1, row = 1)

API_KEY = StringVar()
API_KEY_Entry = ttk.Entry(frame1 , width = 18, textvariable = API_KEY)
API_KEY_Entry.grid(column = 2, row = 1,sticky = (W,E))

API_KEY_Entry.focus()

#second row: Amount to trade
ttk.Label(frame1, text = "Ammount to trade : ").grid(column = 1, row = 2)

Ammount = StringVar()
Ammount_Entry = ttk.Entry(frame1 , width = 10, textvariable = Ammount)
Ammount_Entry.grid(column = 2, row = 2, sticky = W)

#third row: Enter Button

ttk.Button(frame1, text = "Start", command = Log_in).grid(column=2,row =3,sticky=W)

#if frame 2 is open
#update the graph recurrently.


# root.bind("<Return>", Log_in)


root.mainloop()