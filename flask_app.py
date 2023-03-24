from flask import Flask, render_template, request
# import webview
from flask_sock import Sock
import time
import json

# insert the src directory in the list of folders where the interpreter look for modules.
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')

#imports from src
import utilities

################# Application #########################

app = Flask(__name__)

sockets = Sock(app)

# window = webview.create_window('Binance supertren Bot', app)

@app.route("/")
def homepage():
	return render_template("main.html")


@app.route("/", methods = ['POST'])
def login():
	print(request)
	# get the api key e secret from the body of the POST method.
	api_key  = request.form.get('apikey')
	api_secret = request.form.get('secret')
	
	valid_key = utilities.validate_key(api_key, api_secret)

	if valid_key:

		# get user balance.
		balance  = utilities.getUserBalance(api_key, api_secret)
		print(balance)

		#get available coins:(this should get only the coins the user can trade)
		available_coins = utilities.getMarkets()

		#render the loggin page
		return render_template("configuration_page.html", apiKey = api_key, apiSecret = api_secret, userBalance = balance, markets = available_coins)

	else:
		#render the error page.
		return render_template("error_page.html")

@sockets.route('/tradding')
def echo(ws):
	while True:
        	data_received = ws.receive()#receive data about user preferences.
        	parsed_data = json.loads(data_received)
        	selected_coin = parsed_data['selectedCoin']
        	trading_amount = parsed_data['traddingAmmount']
        	while True:
        		data_package = []
        		historical_data = utilities.getHistoricalData(coin = 'ETH/BTC')
        		data_package.append(historical_data[15:])
        		supertrend_data = utilities.supertrend_indicator(bars =historical_data)
        		data_package.append(supertrend_data)
        		print('\n testing: ')
        		print(supertrend_data[0])
        		print(historical_data[15])
        		data_package = json.dumps(data_package)
        		ws.send(data_package)
        		time.sleep(1)


if __name__ =="__main__":
	app.run(debug=True)
	# webview.start()

	# https://plotly.com/javascript/getting-started/


"""
valor agregado no software:
	-analise tecnica, bots e trade autonomo personalizado diretamente da sua corretora.

Pitch:
	existe uma grande demanda pela  capacidade de se implementar estratégias automas de trading que permite.

"""

"""
O problema presente é que o trading não pode ser baseado em websockets. uma vez que a emissão de eventos
pelo sistema de websockets é distribuido para todos os usuários conectados.

-os indicadores como supertrend, e etc. podem ser calculados no lado servidor, mas o trading precisa ser
realizado por uma chamada REST específica para o backend, ou via front end para permitir que os dados gerais sejam enviados, para todos os usuários conectados,
mas ainda sim usuários diferentes podem ser coletados.


"""
