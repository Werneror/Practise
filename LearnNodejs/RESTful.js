var express = require('express');
var app = express();
var fs = require('fs');
var userFile = "users.json";


//添加的新用户数据
var user = {
   "user4" : {
      "name" : "mohit",
      "password" : "password4",
      "profession" : "teacher",
      "id": 4
   }
}


app.get('/listUsers', function(req, res){
   fs.readFile(__dirname + "/" + userFile, 'utf8', function(err, data){
      console.log(data);
      res.end(data);
   });
});

app.get('/addUser', function(req, res){
   fs.readFile(__dirname + "/" + userFile, 'utf8', function(err, data){
      data = JSON.parse(data);
      data["user4"] = user["user4"];
      console.log(data);
      res.end(JSON.stringify(data));
   });
});

app.get('/deleteUser', function(req, res){
    fs.readFile(__dirname + "/" + userFile, 'utf8', function(err, data){
       data = JSON.parse(data);
       delete data["user" + 2];
       console.log(data);
       res.end(JSON.stringify(data));
    });
});

app.get('/:id', function(req, res){
    fs.readFile(__dirname + "/" + userFile, 'utf8', function(err, data){
       data = JSON.parse(data);
       var user = data["user" + req.params.id]
       console.log(user);
       res.end(JSON.stringify(user));
    });
});

var server = app.listen(8081, function(){
    var host = server.address().address;
    var port = server.address().port;
    console.log("应用实例，访问地址为 http://%s:%s", host, port);
});
