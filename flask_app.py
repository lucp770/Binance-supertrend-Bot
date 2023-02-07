from flask import Flask, render_template, request
import webview
from flask_sock import Sock
import time

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
        data = ws.receive()
        # here, get data from ccxt and the supertrend strategy.
        
        while True:
        	historical_data = utilities.getHistoricalData()
        	ws.send(historical_data)
        	time.sleep(1)




# better alternative with better suport: https://flask-sock.readthedocs.io/en/latest/
# https://github.com/miguelgrinberg/flask-sock


if __name__ =="__main__":
	app.run(debug=True)
	# webview.start()

	# https://plotly.com/javascript/getting-started/
