const btn = document.querySelector('.btn');
let apiKey = document.querySelector('.key');
let apiSecret = document.querySelector('.secret');

const startBtn = document.querySelector('.start-tradding-btn');
const userInputAmount = document.querySelector('.trading-amount-class');
const assets = document.querySelectorAll('.asset');


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

function checkAmount(){
	console.log('clicado');
}


startBtn.addEventListener('click', ()=>{
	// checkAmount();
	
})
