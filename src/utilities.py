import ccxt
import json
from datetime import datetime
import pandas as pd
pd.set_option('display.max_rows',None)

import warnings
warnings.filterwarnings('ignore')


def validate_key(apiKey, apiSecret):
	logInObj = {'apiKey': apiKey, 'secret': apiSecret, 'timeout': 30000, 'enableRateLimit': True}

	try:
		exchange = ccxt.binance(logInObj)

		# trow error with credentials are missing
		exchange.checkRequiredCredentials()

		# validate the api key by checking the balance
		balance = exchange.fetchBalance()

		return True

	except Exception as e:
		return False

def getUserBalance(apiKey, apiSecret):
	logInObj = {'apiKey': apiKey, 'secret': apiSecret, 'timeout': 30000, 'enableRateLimit': True}

	try:
		exchange = ccxt.binance(logInObj)
		# validate the api key by checking the balance
		balance = exchange.fetchBalance()
		balance = balance['free']

		non_zero = [(i,j) for i,j in balance.items() if j != 0.0 ]
		# user_funds = json.dumps(non_zero)

		return non_zero
	except Exception as e:
		print(e)

def getMarkets():
	exchange = ccxt.binance()
	markets = [market for market in exchange.load_markets()]
	return markets

def getHistoricalData(coin ='ETH/USDT', timeframe = '1m', limit = 30):
	# this function is executed periodically
	exchange = ccxt.binance()
	bars = exchange.fetch_ohlcv(coin,timeframe = timeframe,limit= limit)
	#bars is an array limit x 6, where the columns are ['timestamp','open','high','low','close','volume']

	# get the supertrend from bars
	
	# transfor the result in a string with json.dumps
	bars = json.dumps(bars)
	return bars

def check_in_uppertrend(df):


def supertrend_indicator(bars, period = 15):

	def true_range(df):
		df['previous_close'] = df['close'].shift(1)
		df['high-low'] = df['high'] - df['low']
		df['high-pc'] = df['high'] - df['previous_close']
		df['low-pc'] = df['low'] - df['previous_close']

		return df[['high-low','high-pc', 'low-pc']].max(axis=1)

	def avg_true_range(df,n_data_points):
		"""N is the number of datapoints to average from"""
		df['true_range'] = true_range(df)
		atr = df['true_range'].rolling(n_data_points).mean()
		return atr

	# supertrend starts here
	df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
	df['upper_band'] = (df['high']+df['low'])/2 + (multiplier*df['ATR'])
	df['lower_band'] = (df['high']+df['low'])/2 - (multiplier*df['ATR'])

	# return the lower band, the upper band, and the signal
	for current_price_idx in range(1,len(df.index)):
		previous_price_idx = current_price_idx - 1

		if df['close'][current_price_idx] > df['upper_band'][previous_price_idx]:
			df['in_uptrend'] = True 
		elif df['close'][current_price_idx] < df['lower_band'][]











# users = [{'id':1, 'name':'Lucas', 'api_hash': 'lipsum'}]
	


