var MongoClient = require('mongodb').MongoClient;
var url = 'mongodb://localhost:27017/runoob';

MongoClient.connect(url, function(err, db){
    if(err) throw err;
    console.log("数据库已创建");
    var dbase = db.db("runoob");
    dbase.createCollection('site', function(err, res){
        console.log("创建集合！");
    });
    var myobj = [
        { name: '菜鸟工具', url: 'https://c.runoob.com', type: 'cn'},
        { name: 'Google', url: 'https://www.google.com', type: 'en'},
        { name: 'Facebook', url: 'https://www.google.com', type: 'en'}
       ];
    dbase.collection("site").insertMany(myobj, function(err, res){
        if(err) throw err;
        console.log("文档插入成功。");
        console.log("插入文档的数量为：" + res.insertedCount);
    });
    dbase.collection('site').find({}).toArray(function(err,result){
        if(err) throw err;
        console.log(result);
    })
    var whereStr = {name:"菜鸟教程"};
    dbase.collection('site').find(whereStr).toArray(function(err,result){
        if(err) throw err;
        console.log(result);
    });
    var updateStr = {$set: { "url" : "https://www.runoob.com" }};
    dbase.collection('site').updateOne(whereStr, updateStr, function(err, res){
        if(err) throw err;
        console.log("文档更新成功");
    });

    dbase.collection("site").deleteOne(whereStr, function(err, obj){
        if(err) throw err;
        console.log("文档删除成功");
        db.close();
    })
});
