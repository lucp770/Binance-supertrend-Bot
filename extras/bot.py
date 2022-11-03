import ccxt
import pandas as pd
import ta
from ta.volatility import BollingerBands,AverageTrueRange
# print(dir(ccxt))#list all properites of the object ccxt


# print(ccxt.exchanges)#list all available exchanges


exchange = ccxt.binance()
print(exchange)

# markets = exchange.load_markets()

# for market in markets:
# 	print(market)


coins = ['ETC/TRY','ETH/BTC']

bars=exchange.fetch_ohlcv('ETH/USDT',limit=200)

#create a pandas dataframe to apply ta indicators.
#do not get the last element because is still a uncertain candle.
df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
bb_indicator = BollingerBands(df['close'])

# print(bb_indicator.bollinger_hband())

# print('\n',dir(bb_indicator))
df['upper_band']=bb_indicator.bollinger_hband()
df['lower_band']=bb_indicator.bollinger_lband()
df['moving_average']=bb_indicator.bollinger_mavg()


df = df[20:]
print('df apos o calculo das bandas de boillinger \n \n', df.head())

def plot_BB(data_frame_close_prices):
	df = data_frame_close_prices
	

	pass
#lets get the Average True Range indicator

atr_indicator = AverageTrueRange(df['high'],df['low'],df['close'])
df['atr'] = atr_indicator.average_true_range()

print('df apos a adesao do atr \n \n', df.tail())


# print(ccxt.exchanges)
"""
exchange_id = '<Exchange_name>'
exchange_class = getattr(ccxt,exchange_id)

#execute the call method of the class, passing the API_key to execute private functions.

config_object = {'apiKey': 'YOUR_API_KEY', 'secret': 'YOUR_SECRET', timeout: 30000, 'enableRateLimit': True}

exchange = exchage_class(config_object)




"""


