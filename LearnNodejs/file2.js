var fs = require("fs");
var buf = new Buffer(1024);


console.log("准备截取文件！");
fs.open('input.txt', 'r+', function(err, fd){
    if(err){
        return console.error(err);
    }
    console.log("文件打开成功！");
    console.log("截取文件前10个字节的内容。");

    // 截取文件
    fs.ftruncate(fd, 10, function(err){
        if(err){
            console.log(err);
        }
        console.log("文件截取成功。");

        fs.read(fd, buf, 0, buf.length, 0, function(err, bytes){
            if(err){
                console.error(err);
            }

            // 仅输出读取的文字
            if(bytes > 0){
                console.log(buf.slice(0, bytes).toString());
            }

            // 关闭文件
            fs.close(fd, function(err){
                if(err){
                    console.error(err);
                }
                console.log("文件关闭成功！");
            });
        });
    });
});


console.log("准备删除文件！");
fs.unlink('output.txt', function(err){
    if(err){
        return console.error(err);
    }
    console.log("文件删除成功！");
});


console.log("准备创建目录/tmp/test！");
fs.mkdir('/tmp/test/', function(err){
    if(err){
        return console.error(err);
    }
    console.log("目录创建成功！");
})


console.log("准备读取目录/tmp/！");
fs.readdir('/tmp/', function(err, files){
    if(err){
        return console.error(err);
    }
    files.forEach(function(file){
        console.log(file);
    })
})


console.log("准备删除目录/tmp/test！");
fs.rmdir('/tmp/test', function(err){
    if(err){
        return console.error(err);
    }
    console.log("读取 /tmp 目录");
    fs.readdir('/tmp/', function(err, files){
        if(err){
            console.error(err);
        }
        files.forEach(function(file){
            console.log(file);
        })
    })
})
