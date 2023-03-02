import ccxt
import pandas as pd
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')

import utilities


exchange = ccxt.binance()
bars = exchange.fetch_ohlcv('ETH/BTC',timeframe = '1m',limit= 100);

df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])

df2 = utilities.supertrend_indicator(bars)
print(df.head())

print('\n', df2)