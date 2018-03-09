var buf = Buffer.alloc(10);
buf.write('abcde', 0, 5, 'ascii');
console.log(buf.toString());
console.log(buf.length);
// 验证只部分解码的字符不会被写入
buf.write('我', 5, 'ascii');
console.log(buf.toString());
console.log(buf.length);
