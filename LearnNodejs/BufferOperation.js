// 缓冲区合并
console.log("\n缓冲区合并：");
var buffer1 = Buffer.from('我是好人。', 'utf8');
var buffer2 = Buffer.from('而你，', 'utf8');
var buffer3 = Buffer.from('是个坏人！', 'utf8');
var buffer = Buffer.concat([buffer1, buffer2, buffer3]);
console.log(buffer.toString('utf8'));

// 缓冲区比较
console.log("\n缓冲区比较：");
var buffer1 = Buffer.from('ABC');
var buffer2 = Buffer.from('ABCD');
var result = buffer1.compare(buffer2);

if(result < 0) {
    console.log(buffer1 + " 在 " + buffer2 + " 之前");
}else if(result == 0) {
    console.log(buffer1 + " 与 " + buffer2 + " 相同");
}else {
    console.log(buffer1 + " 在 " + buffer2 + "之后");
}

// 缓冲区拷贝
console.log("\n缓冲区拷贝：");
var buf1 = Buffer.from('abcdefghijkl');
var buf2 = Buffer.from('RUNOOB');
buf2.copy(buf1, 2); // 将 buf2 插入到 buf1 的指定位置上
console.log(buf1.toString());

// 缓冲区裁剪
console.log("\n缓冲区裁剪：");
var buffer1 = Buffer.from('runoob');
var buffer2 = buffer1.slice(1, 3);
console.log("buffer1 content: " + buffer1.toString());
console.log("buffer2 content: " + buffer2.toString());

// 缓冲区长度
console.log("\n缓冲区长度：");
var buffer = Buffer.from('www.runoob.com');
console.log("buffer length: " + buffer.length);
