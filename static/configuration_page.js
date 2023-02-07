const btn = document.querySelector('.btn');

const startBtn = document.querySelector('.start-tradding-btn');
const stopBtn = document.querySelector('.stop-tradding-btn');
const userInputAmount = document.querySelector('.trading-amount-class');
const assets = document.querySelectorAll('.asset');

const comboBox = document.querySelector('.combo');
let socket;

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

constructAssetsObj();

function connectServer(){
	let socket = new WebSocket("ws://localhost:5000/tradding");

	socket.onopen = function  (event){
		console.log('conected to the server');
}

	return socket;

}




function generatePlot(data){
	let [timestamp,open,high,low,close,volume] = data;
	console.log({timestamp,open,high,low,close,volume});

}

function testePlot(){
	let panel = document.getElementById('tester');
	Plotly.newPlot( panel, [{
	x: [1, 2, 3, 4, 5],
	y: [1, 2, 4, 8, 16] }], {
	margin: { t: 0 } } );
}
// need to generate a candlestick plot.
// https://plotly.com/javascript/candlestick-charts/

testePlot();

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
			
			socket = new WebSocket("ws://localhost:5000/tradding");
			socket.onopen = function (event) {
			console.log('conection opened with the server: ');

			socket.send("WebSocket is really cool");
				};

			socket.onmessage = function(event){
			console.log(' the server have sent a message');
			
			// the data is a string, parse to obtain an array
			let data = JSON.parse(event.data);
			data = data[0];

			generatePlot(data)
			// console.log(data);
// 
			// generate plot
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

stopBtn.addEventListener('click', ()=>{
	if(socket){
		socket.close()
		console.log('stop btn pressionado');
	}
})
