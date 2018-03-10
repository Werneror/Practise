var fs = require("fs");

// 异步读取
fs.readFile('input.txt', function(err, data){
    if(err){
        console.error(err);
    }
    console.log("异步读取： " + data.toString());
});

// 同步读取
var data = fs.readFileSync('input.txt');
console.log("同步读取：" + data.toString());


// 读取文件信息
fs.stat('input.txt', function(err, stats){
    if(err){
        return console.error(err);
    }
    console.log(stats);
    console.log("[stat]读取文件信息成功！");

    // 检查文件类型
    console.log("是否为文件(isFile)？" + stats.isFile());
    console.log("是否为目录(isDiectory)？" + stats.isDirectory());
})


//写入文件
console.log("准备写入文件");
fs.writeFile('output.txt', '我是通过writeFile写入的文件内容！', function(err){
    if(err){
        return console.error(err);
    }
    console.log("数据写入成功！");
    console.log("------我是分割线------");
    console.log("读取写入的数据！");
    fs.readFile('output.txt', function(err, data){
        if(err){
            return console.error(err);
        }
        console.log("异步读取文件数据：" + data.toString());
    });
});

// 异步打开文件
console.log("准备打开文件！");
var buf = new Buffer(1024);
fs.open('input.txt', 'r+', function(err, fd){
    if(err){
        return console.error(err);
    }
    console.log("文件打开成功！");
    // 读取文件
    fs.read(fd, buf, 0, 10, 0, function(err, bytes){
       if(err){
           console.error(err);
       }
       console.log(bytes + " 字节被读取");

       // 仅输出读取的字节
       if(bytes > 0){
           console.log(buf.slice(0,bytes).toString());
       }

       // 关闭文件
       fs.close(fd, function(err){
           if(err){
               console.error(err);
           }
           console.log("文件关闭成功！");
       })

    });
});
