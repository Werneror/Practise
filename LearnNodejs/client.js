var http = require('http');

// 用于请求的选项
var options = {
    host: 'localhost',
    port: 8080,
    path: '/serverBase.js'
};

// 处理响应的回调函数
var callback = function(response){
    // 不断更新数据
    var body = '';
    response.on('data', function(data){
       body += data;
    });
    response.on('end', function(){
        console.log(body);
    });
}

// 向服务器发送请求
var req = http.request(options, callback);
req.end();
