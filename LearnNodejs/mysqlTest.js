var mysql = require('mysql');
var connection = mysql.createConnection({
    host:'localhost',
    user:'root',
    password:'root',
    database:'test'
});

connection.connect();

// 查询数据库
var sql ='SELECT * FROM websites';
connection.query(sql, function(error, results){
    if(error){
        console.error('[SELECT ERROR] - ', err.message);
    }else{
        console.log('--------------------SELECT---------------------');
        console.log(results);
        console.log('-----------------------------------------------');
    }
});

// 插入数据
var addSql = 'INSERT INTO websites(id, name, url, alexa, country) VALUES (0,?,?,?,?)';
var addSqlParams =['若水斋', 'https://blog.werner.wiki/', '3412314', 'CN'];
connection.query(addSql, addSqlParams, function(err, result){
    if(err){
        console.error('[INSERT ERROR] - ', err.message);
    }else{
        console.log('--------------------INSERT---------------------');
        console.log('INSERT ID: ', result.insertId);
        console.log('-----------------------------------------------');
    }
});

// 更新数据
var modSql = 'UPDATE websites SET name = ?, url= ? WHERE id = ?';
var modSqlParams = ['若水斋杂记', 'https://wiki.werner.wiki/', 7];
connection.query(modSql, modSqlParams, function(err, result){
    if(err){
        console.error('[UPDATE ERROR] - ', err.message);
    }else{
        console.log('--------------------UPDATE---------------------');
        console.log('UPDATE affectedRows', result.affectedRows);
        console.log('-----------------------------------------------');
    }
});

// 删除数据
var delSql = 'DELETE FROM websites WHERE id = 9';
connection.query(delSql, function(err, result){
    if(err){
        console.error('[DELETE ERROR] - ', err.message);
    }else{
        console.log('--------------------DELETE---------------------');
        console.log('DELETE affectedRows', result.affectedRows);
        console.log('-----------------------------------------------');
    }
});

connection.end();
