from flask import Flask, render_template, request
import webview

# insert the src directory in the list of folders where the interpreter look for modules.
import os
current_dir = os.getcwd()
import sys
sys.path.append(current_dir+'/src')

#imports from src
import utilities

################# Application #########################

app = Flask(__name__)

window = webview.create_window('Binance supertren Bot', app)

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
		#render the loggin page
		return render_template("configuration_page.html")
	else:
		#render the error page.
		return render_template("error_page.html")
if __name__ =="__main__":
	# app.run(debug=True)
	webview.start()