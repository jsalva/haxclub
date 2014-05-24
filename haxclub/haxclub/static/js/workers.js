var worker = new Worker('/static/js/hax/worker.js');

worker.onmessage = function(oEvent){
    console.log('Worker message recieved.');
};

worker.addEventListener('message', function(oEvent){
    console.log('Another message recieved. Well not really, it was the same one.')

});

worker.postMessage('')
