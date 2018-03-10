var EventEmitter = require('events').EventEmitter;
var domain = require('domain');

var emitter1 = new EventEmitter();

// 创建域
var domain1 = domain.create();
domain1.on('error', function(err){
   console.log("domain1 处理这个错误（" + err.message + "）");
});

// 显示绑定
domain1.add(emitter1);

emitter1.on('error', function(err){
    console.log("监听器处理这个错误（" + err.message + "）");
});

emitter1.emit('error',  new Error('看看谁来处理我'));
emitter1.removeAllListeners('error');

emitter1.emit('error',  new Error('再来看看谁来处理我'));

var domain2 = domain.create();
domain2.on('error', function(err){
    console.log("domain2 处理这个错误（" + err.message + "）");
})

// 隐式绑定
domain2.run(function(){
   var emitter2 = new EventEmitter();
   emitter2.emit('error', new Error('谁会处理我呢？好纠结&_&'));
});

domain1.remove(emitter1);
emitter1.emit('error', new Error('谁都抓不到我！！！'));
