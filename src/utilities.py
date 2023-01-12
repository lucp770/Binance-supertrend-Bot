import ccxt

def validate_key(apiKey, apiSecret):
	logInObj = {'apiKey': apiKey, 'secret': apiSecret, 'timeout': 30000, 'enableRateLimit': True}
	print('conecting to binance .....')
			# rate limit exist to limit the number of requeests to the exchange and not be banned
			# create a ccxt instance to validade the api key.

	try:
		exchange = ccxt.binance(logInObj)

		# trow error with credentials are missing
		exchange.checkRequiredCredentials()

		# validate the api key by checking the balance
		balance = exchange.fetchBalance()

		return True

	except Exception as e:
		return False


# users = [{'id':1, 'name':'Lucas', 'api_hash': 'lipsum'}]
	


