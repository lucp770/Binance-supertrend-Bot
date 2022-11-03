#this script allows to list the exchanges and the respective coins.
from matplotlib import pyplot as plt
from datetime import datetime
import mplfinance as mpf
import ccxt

def get_data():
	exchange = ccxt.binance()
	bars=exchange.fetch_ohlcv('ETH/BTC',limit=20,timeframe='1m')
	# df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
	#
	timestamp = [datetime.fromtimestamp(value[0]/1000.0) for value in bars]
	open_price = [value[1] for value in bars]
	high = [value[2] for value in bars]
	low = [value[3] for value in bars]
	close = [value[4] for value in bars]

	return timestamp, open_price, high, low, close


timestamp, open_price, high, low, close = get_data()

#create two sets (red and green dots)

 # green_bars = [[timestamp[i],open_price[i],high[i], low[i], close[i]] for i in range(len(open_price)) if open_price[i] > close[i]]

green_bars = []
red_bars = []

for i in range(len(timestamp)):
	if open_price[i] > close[i]:
		green_bars.append([timestamp[i], open_price[i], high[i], low[i], close[i]])
	else:
 		red_bars.append([timestamp[i], open_price[i], high[i], low[i], close[i]])

# print(red_bars[:3])

width = .3
print([[bar[1] for bar in green_bars]])
#plto green bars
plt.bar([bar[0] for bar in green_bars], height = [bar[-1] for bar in green_bars], width = .0004, bottom = [bar[1] for bar in green_bars], color = 'green')

#plot red bars
plt.bar([bar[0] for bar in red_bars], height = [bar[-1] for bar in red_bars], width = .0004, bottom = [bar[1] for bar in red_bars], color = 'red')
# plt.yscale("logit")
# plt.ylim((0,0.2))

plt.xticks(rotation=30, ha='right')
plt.show()

#plot red bars
# plt.bars()




# plt.plot(timestamp, closing_prices)
# plt.show()

