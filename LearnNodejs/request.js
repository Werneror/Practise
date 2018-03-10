var url = require('url');
var http = require('http');
var util = require('util');
var querystring = require('querystring');

var postHtml =
'<html><head><meta charset="utf-8"><title>就是测试一下</title></head>' +
'<body>' +
'<form method="post">' +
'网站名： <input name="name"><br>' +
'网站 URL： <input name="url"><br>' +
'<input type="submit">' +
'</form>' +
'</body></html>';

http.createServer(function(req, res){
    res.writeHead(200, {'Content-Type': 'text/html; charset=utf-8'})

    var body = '';
    req.on('data', function(chunk){
        body += chunk;
    })

    req.on('end', function(err){
        if(err){
            console.error(err);
        }
        body = querystring.parse(body);
        if(body.name && body.url){
            res.write("网站名： " + body.name);
            res.write('<br>')
            res.write("网站URL： " + body.url);
        }else{
            res.write(postHtml);
            var params = url.parse(req.url, true).query;
            res.write("GET参数：<br>" + util.inspect(url.parse(req.url, true).query));
            res.write("<br>");
        }
        res.end();
    });

}).listen(8888);
