import ccxt
import pandas as pd
from datetime import datetime 
pd.set_option('display.max_rows',None)
import schedule
import time

import warnings
warnings.filterwarnings('ignore')

def true_range(df):
	df['previous_close'] = df['close'].shift(1)
	df['high-low'] = df['high'] - df['low']
	df['high-pc'] = df['high'] - df['previous_close']
	df['low-pc'] = df['low'] - df['previous_close']
	return df[['high-low','high-pc', 'low-pc']].max(axis=1)

def avg_true_range(df,N=14):
	"""N is the number of days to average"""
	df['true_range'] = true_range(df)
	atr = df['true_range'].rolling(N).mean()
	return atr 

def supertrend(df,multiplier=3, period=14):
	print('calculating supertrend')
	df['ATR']= avg_true_range(df,period)

	df['upper_band'] = (df['high']+df['low'])/2 + (multiplier*df['ATR'])
	df['lower_band'] = (df['high']+df['low'])/2 - (multiplier*df['ATR'])

	df['in_uptrend'] = True 


	#let's loop on the dataframe and change the values of the column 'in_uptrend'

	for current in range(1,len(df.index)):
		previous = current -1
		#keep track of the current and previous index

		if df['close'][current] > df['upper_band'][previous]:
			df['in_uptrend'] = True
			
		elif df['close'][current] < df['lower_band'][previous]:
			df['in_uptrend'] = False
		else:
			df['in_uptrend'][current] = df['in_uptrend'][previous]

			if df['in_uptrend'][current] and df['lower_band'][current] < df['lower_band'][previous]:
				df['lower_band'][current] = df['lower_band'][previous]#the next lower band is set to the previous if is not greater than the previous value

			#do the same but for the upper band

			if not df['in_uptrend'][current] and df['upper_band'][current] > df['upper_band'][previous]:
				df['upper_band'][current] = df['upper_band'][previous]
	return df

# supertrend(df)#calculates the buy and sell signals based on the last 14 days of price movement.

def show_relevant_data(df):
	print(df.loc[:,['timestamp','close','upper_band','lower_band','in_uptrend']])


def check_buy_sell_signal(df):
	last_row = len(df.index) - 1
	previous_row = last_row - 1
	print(df.tail(2))

	if not df['in_uptrend'][previous_row] and df['in_uptrend'][last_row]:
		print('buy buy .....')

	if df['in_uptrend'][previous_row] and not df['in_uptrend'][last_row]:
		print('Sell sell')

	print(last_row, previous_row)
def run_bot():
	print("I'm working")
	#get the binance exchange
	exchange = ccxt.binance()

	# get the historical data]
	bars = exchange.fetch_ohlcv('ETH/USDT',timeframe='15m',limit=100)

	#create and configure a pandas dataframe
	df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
	df['timestamp']=pd.to_datetime(df['timestamp'],unit='ms')

	supertrend_data = supertrend(df)
	check_buy_sell_signal(df)


if __name__ == '__main__' :
	print('running as the main script ....')
	#configuring the schedule to run every 10s
	# schedule.every(2).seconds.do(run_bot)

	# while True:
	# 	schedule.run_pending()
	# 	time.sleep(1)

	exchange = ccxt.binance()

	# get the historical data]
	bars = exchange.fetch_ohlcv('ETH/USDT',timeframe='1m',limit=100)

	#create and configure a pandas dataframe
	df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
	df['timestamp']=pd.to_datetime(df['timestamp'],unit='ms')

	supertrend_data = supertrend(df)

	# slicing the dataframe
	supertrend_data = supertrend_data.loc[:, ['timestamp', 'close', 'upper_band', 'lower_band', 'in_uptrend']]
	supertrend_data = supertrend_data[15:]#remove the first 15 datapoints that do not work because of the ATR calculation
	# print(supertrend_data.head())

	supertrend_data_lista = supertrend_data.values
	


"""Supertrend
Summary

The Supertrend helps you make the right trading decisions
. However, there are times when it generates false signals.
 Therefore, it is best to use the right combination of several indicators. 
 Like any other indicator, Supertrend works best when used with 
 other indicators such as MACD, Parabolic SAR, or RSI."""