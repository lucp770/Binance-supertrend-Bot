const btn = document.querySelector('.btn');
let apiKey = document.querySelector('.key');
let apiSecret = document.querySelector('.secret');

const startBtn = document.querySelector('.start-tradding-btn');
const userInputAmount = document.querySelector('.trading-amount-class');
const assets = document.querySelectorAll('.asset');

const comboBox = document.querySelector('.combo');

// array of objects for user available assets.
const userAvailableAssets = [];

function constructAssetsObj(){
	assets.forEach(div =>{
		let asset = div.children[0].textContent;
		let total = div.children[1].textContent;
		// console.log(asset+'\n'+total);

		userAvailableAssets.push({asset, total})
	})
}


function connectServer(){
	let socket = new WebSocket("ws://localhost:5000/tradding");

	socket.onopen = function  (event){
		console.log('conected to the server');
}

	return socket;

}

constructAssetsObj();

function checkAmount(){
	// get the inserted ammoun

	let selectedCoin= comboBox.value
	

	// get the selling and buying asset
	if (selectedCoin != 'Select'){

	let separator = selectedCoin.search('/');
	let sellAsset = selectedCoin.substring(separator+1, selectedCoin.length);
	let buyAsset = selectedCoin.substring(0,separator);

	console.log(userInputAmount)

	let traddingAmmount = Number(userInputAmount.value);

	let match = userAvailableAssets.find(coin => coin.asset === sellAsset);

	if(match === undefined){
		alert('please check if you have the selling asset in your account');
	}
	else{
		// check if the user has enough
		if(Number(match.total) < traddingAmmount){
			alert('Please check if you have in your account the amount selected to trade')
			// make the border of the asset become red
		}
		else{
			console.log('user can trade');
			// two options: use client side trading.(this requires to rewrite a lot of code, maybe is not possible because )
			// conect flask with websockets to use the previously developed algorithm.(this seens hard)
			let socket = new WebSocket("ws://localhost:5000/tradding");
			socket.onopen = function (event) {
			console.log('conection opened with the server: ');
			socket.send("WebSocket is really cool");
				};

			socket.onmessage = function(event){
			console.log(' the server have sent a message');
			console.log(event.data);
		}


			// i opt to use websockets to server comunication( an eg: https://stackoverflow.com/questions/15721679/update-and-render-a-value-from-flask-periodically)
		}

	}
	



	}

	
}

function showPlot(){
	console.log('clicado');
}




startBtn.addEventListener('click', ()=>{
	checkAmount();
	
})
