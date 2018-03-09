// 前正在执行的脚本的文件名
console.log(__filename);

// 当前执行脚本所在的目录
console.log(__dirname);

// 在指定的毫秒(ms)数后执行指定函数，只执行一次指定函数。返回一个代表定时器的句柄值
setTimeout(function(){console.log("Time out!")}, 1000);

// 停止一个之前通过 setTimeout() 创建的定时器。
// 参数 t 是通过 setTimeout() 函数创建的定时器。
var t = setTimeout(function(){console.log("Time out!, Me too")}, 100);
clearTimeout(t);

// 在指定的毫秒(ms)数后执行指定函数，会不停地调用函数，直到 clearInterval() 被调用
i = setInterval(function(){console.log("Ha, ha...")}, 1000);

// clearInterval 用于清除 setInterval
setTimeout(function(){clearInterval(i)}, 5000);

// console.log 有多个参数时类似 C 语言 printf() 命令的格式输出
console.log("你好啊，我的朋友，%s，我们已经%d年没有见面了。", "王二", 32);

// console.dir 用来对一个对象进行检查（inspect），并以易于阅读和打印的格式显示
console.dir(setTimeout);

// console.time(label) 输出时间，表示计时开始。
console.time("My time");

// console.timeEnd(label) 结束时间，表示计时结束。
console.timeEnd("My time");

// 	console.trace(message[, ...]) 当前执行的代码在堆栈中的调用路径
console.trace("This is my function");

// 输出到终端
process.stdout.write("Hello World!" + "\n");
// pid 当前进程的进程号
console.log("pid: " + process.pid);
// title 进程名，默认值为"node"，可以自定义该值
console.log("title: " + process.title);
// arch 当前 CPU 的架构：'arm'、'ia32' 或者 'x64'
console.log("arch: " + process.arch);
// platform 运行程序所在的平台系统 'darwin', 'freebsd', 'linux', 'sunos' 或 'win32'
console.log("platform: " + process.platform);

// 退出时触发
process.on('exit', function(code){
   setTimeout(function(){
       console.log("我很可怜，因为执行不到。");
   }, 0);
   console.log("退出码为%d。", code);
});
console.log("程序执行完毕。");
