var fs = require('fs');

// 从流中读数据
console.log('从流中读数据：');
var data = '';
// 创建可读流
var readerStream = fs.createReadStream('input.txt');
// 设置编码为 UTF8
readerStream.setEncoding('UTF8');

// 处理流事件 --> data, end, 和 error
readerStream.on('data', function(chunk) {
    data += chunk;
    console.log("读了 " + chunk.length + " 字节数据");
});
readerStream.on('end', function() {
    //console.log(data);
});
readerStream.on('error', function(err) {
    console.log(err.stack);
});

// 写入流
console.log('写入流：');
var data = "卑鄙是卑鄙者的通行证，高尚";
// 创建一个可以写入的流，写入到文件 output.txt 中
var writerStream = fs.createWriteStream('output.txt');
// 使用 UTF8 编码写入数据
writerStream.write(data, 'UTF8');
// 标记文件末尾
writerStream.end();
// 处理流事件 --> data, end 和 error
writerStream.on('finish', function() {
    console.log("写入成功。");
});
writerStream.on('error', function(err) {
    console.log(err.stack);
});

// 管道流
console.log('管道流：');
// 创建一个可读流
var readerStream2 = fs.createReadStream('input2.txt');
// 创建一个可写流
var writerStream2 = fs.createWriteStream('output2.txt');
// 管道读写操作
readerStream2.pipe(writerStream2);

console.log('程序执行完毕。');
