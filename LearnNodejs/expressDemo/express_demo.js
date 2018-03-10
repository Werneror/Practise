var express = require('express');
var bodyParser = require('body-parser');
var multer = require('multer');
var fs = require('fs');
var cookieParser = require('cookie-parser');
var util = require('util');
var app = express();

// 创建 application/x-www-form-urlencoded 编码解析
var urlencodeParser = bodyParser.urlencoded({extended: false});

app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended: false}));
app.use(multer({dest: '/tmp/'}).array('image'));
app.use(cookieParser());

// 主页输出 Hello GET
app.get('/', function(req, res){
    console.log("主页 GET 请求");
    console.log("Cookies: " + util.inspect(req.cookies));
    res.send('Hello GET');
});

// POST 请求
app.post('/', function(req, res){
    console.log("主页 POST 请求");
    res.send('Hello POST');
});

// /del_user 页面响应
app.get('/del_user', function(req, res){
    console.log("/del_user 响应 DELETE 请求");
    res.send('删除页面');
});

// /list_user 页面 GET 请求
app.get('/list_user', function(req, res){
    console.log("/list_user GET 请求");
    res.send('用户列表页面');
});

// 对页面 abcd, abxcd, ab123cd 等响应 GET 请求
app.get('/ab*cd', function(req, res){
    console.log("/ab*cd GET 请求");
    res.send('正则匹配');
});

app.get('/index.html', function(req, res){
    res.sendFile(__dirname + '/' + 'index.html');
});

app.get('/upload.html', function(req, res){
    res.sendFile(__dirname + '/' + 'upload.html');
});

app.post('/file_upload', function(req, res){
   console.log(req.files[0]); // 上传文件的信息
   var des_file = __dirname + '/' + req.files[0].originalname;
   fs.readFile(req.files[0].path, function(err, data){
      fs.writeFile(des_file, data, function(err){
         if(err) {
             console.error(err);
         }else{
             response = {
                 message: 'File uploaded successfully',
                 filename: req.files[0].originalname
             }
         }
         console.log(response);
         res.end(JSON.stringify(response));
      });
   });
});

app.get('/process_get', function(req, res){
    // 输出 JSON 格式
    var response = {
        "first_name": req.query.first_name,
        "last_name": req.query.last_name
    };
    console.log(response);
    res.writeHead(200,{'Content-Type':'text/html;charset=utf-8'});
    res.end(JSON.stringify(response));
});

app.post('/process_post', urlencodeParser, function(req, res){
    // 输出 JSON 格式
    var response = {
        "first_name": req.body.first_name,
        "last_name": req.body.last_name
    };
    console.log(response);
    res.writeHead(200,{'Content-Type':'text/html;charset=utf-8'});
    res.end(JSON.stringify(response));
});

var server = app.listen(8081, function(){
    var host = server.address().address;
    var port = server.address().port;
    console.log("应用实例，访问地址为http://%s:%s", host, port);
});
