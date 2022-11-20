#this script allows to list the exchanges and the respective coins.
from matplotlib import pyplot as plt
from datetime import datetime
import mplfinance as mpf
import ccxt
import pandas as pd


def get_data():
	exchange = ccxt.binance()
	bars=exchange.fetch_ohlcv('ETH/USDT',limit=20,timeframe='1m')
	df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
	df['timestamp'] = df['timestamp'].apply(lambda x: datetime.fromtimestamp(x/1000.0))

	# #
	# timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]
	# open_price = [value[1] for value in bars]
	# high = [value[2] for value in bars]
	# low = [value[3] for value in bars]
	# close = [value[4] for value in bars]

	return df


prices = get_data()

# print(pd.to_datetime(df['timestamp'], unit = 's'))


def generate_candlesticks(dataframe):
	plt.figure()

	#define width of candlestick elements
	width = .4
	width2 = .05

	#define up and down prices
	up = prices[prices.close>=prices.open]
	print(up)
	down = prices[prices.close<prices.open]

	#define colors to use
	col1 = 'green'
	col2 = 'red'

	#plot up prices
	plt.bar(up.index,up.close-up.open,width,bottom=up.open,color=col1)
	plt.bar(up.index,up.high-up.close,width2,bottom=up.close,color=col1)
	plt.bar(up.index,up.low-up.open,width2,bottom=up.open,color=col1)

	#plot down prices
	plt.bar(down.index,down.close-down.open,width,bottom=down.open,color=col2)
	plt.bar(down.index,down.high-down.open,width2,bottom=down.open,color=col2)
	plt.bar(down.index,down.low-down.close,width2,bottom=down.close,color=col2)

	#rotate x-axis tick labels
	plt.xticks(rotation=45, ha='right')

	#display candlestick chart
	plt.show()



generate_candlesticks(prices)












# #create two sets (red and green dots)

#  # green_bars = [[timestamp[i],open_price[i],high[i], low[i], close[i]] for i in range(len(open_price)) if open_price[i] > close[i]]

# green_bars = []
# red_bars = []

# for i in range(len(timestamp)):
# 	if open_price[i] > close[i]:
# 		green_bars.append([timestamp[i], open_price[i], high[i], low[i], close[i]])
# 	else:
#  		red_bars.append([timestamp[i], open_price[i], high[i], low[i], close[i]])

# # print(red_bars[:3])

# width = .3
# print([[bar[1] for bar in green_bars]])
# #plto green bars
# plt.bar([bar[0] for bar in green_bars], height = [bar[-1] for bar in green_bars], width = .0004, bottom = [bar[1] for bar in green_bars], color = 'green')

# #plot red bars
# plt.bar([bar[0] for bar in red_bars], height = [bar[-1] for bar in red_bars], width = .0004, bottom = [bar[1] for bar in red_bars], color = 'red')
# # plt.yscale("logit")
# # plt.ylim((0,0.2))

# plt.xticks(rotation=30, ha='right')
# plt.show()

# #plot red bars
# # plt.bars()




# # plt.plot(timestamp, closing_prices)
# # plt.show()

