var EventEmitter = require('events').EventEmitter;
var event = new EventEmitter();
event.on('some_event', function(arg1, arg2){
    console.log('listener1', arg1, arg2);
});
event.on('some_event', function(arg1, arg2){
    console.log('listener2', arg1, arg2);
});
setTimeout(function(){
    event.emit('some_event', 'arg1 参数', 'arg2 参数');
}, 1000);
