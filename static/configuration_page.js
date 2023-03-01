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

function transformToDate(unixtimestamp){
	let date  = new Date(unixtimestamp);
	let string = date.getFullYear() + '-' + 0 + (date.getMonth()+1) + '-' + date.getDate() + ' '+
	 date.getHours() + ':' + date.getMinutes();
	return string;
}

function generatePlot(data){
	// data is an array with 30 elements.
	
	// define empty arrays.
	let timestamp=[]; 
	let open =[];
	let high =[];
	let low =[];
	let close =[];
	let volume =[];

	// for each element on data fill the array.
	data.forEach(datapoint =>{
		timestamp.push(transformToDate(datapoint[0]));
		open.push(datapoint[1]);
		high.push(datapoint[2]);
		low.push(datapoint[3]);
		close.push(datapoint[4]);
		volume.push(datapoint[5]);
	});

	let totalSize = Math.abs(Math.max(...high) - Math.min(...low));

	let trace1 ={
		x:timestamp,
		close: close,

		decreasing: {line: {color: '#7F7F7F'}}, 

		high: high,

		increasing: {line: {color: '#17BECF'}}, 

  		line: {color: 'rgba(31,119,180,1)'},

  		low: low,
  		open: open,

  		type: 'candlestick', 
	  	xaxis: 'x', 
	  	yaxis: 'y'
	};

	let plotData = [trace1];
	// need to create trace 2 e trace 3 do indicador supertrend.

	let layout = {
		dragmode: 'zoom',
		margin: {
			r: 10, 
		    t: 25, 
		    b: 40, 
		    l: 60
		},

		showLegend: false,
		 xaxis: {
		    autorange: true, 
		    domain: [0, 1], 
		    range: [timestamp[0], timestamp[timestamp.length-1]], 
		    rangeslider: {range: [timestamp[0], timestamp[timestamp.length-1]]}, 
		    title: 'Date', 
		    type: 'date'
		  }, 

		yaxis: {
		    autorange: true, 
		    domain: [0, 1], 
		    range: [Math.min(...low),Math.max(...high)], 
		    type: 'linear'
  		}
	};

	console.log(timestamp[0],timestamp[timestamp.length-1] );
	let panel = document.getElementById('tester');
	Plotly.newPlot(panel, plotData, layout);
	
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

function getUserSelection(){

	let selectedCoin= comboBox.value;
	let traddingAmmount = Number(userInputAmount.value);


	return {selectedCoin, traddingAmmount}

}

function executeTrade(){
	socket = new WebSocket("ws://localhost:5000/tradding");
	socket.onopen = function (event) {
	console.log('conection opened with the server: ');

	let userSelection = JSON.stringify(getUserSelection());

	// send user information to the server.
	socket.send(userSelection);
		};

	socket.onmessage = function(event){
	console.log(' the server have sent a message');
	
	// the data is a string, parse to obtain an array
	let data = JSON.parse(event.data);
	generatePlot(data)

}


}

function checkAmount(){
	// get the inserted ammoun

	let {selectedCoin, traddingAmmount} = getUserSelection();
	
	// get the selling and buying asset
	if (selectedCoin != 'Select'){

	let separator = selectedCoin.search('/');
	let sellAsset = selectedCoin.substring(separator+1, selectedCoin.length);
	let buyAsset = selectedCoin.substring(0,separator);

	// let traddingAmmount = Number(userInputAmount.value);

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

			executeTrade();
			
			
			// i opt to use websockets to server comunication( an eg: https://stackoverflow.com/questions/15721679/update-and-render-a-value-from-flask-periodically)
			
		}

	}

	}

	
}


// ---------------------------------------APPLICATION START HERE ----------------------------------//

startBtn.addEventListener('click', ()=>{
	checkAmount();
	
})

stopBtn.addEventListener('click', ()=>{
	if(socket){
		socket.close()
		console.log('stop btn pressionado');
	}
})

// o site precisa ter uma opção para configurações avançadas onde o usuario pode ser escolher parametros para configurar o indicador supertrend
// dentre esses para metros o multiplicador que é aplicado ao ATR, o número de elementos usados para calcular o ATR.
