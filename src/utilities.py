import ccxt
import json

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


# users = [{'id':1, 'name':'Lucas', 'api_hash': 'lipsum'}]
	


