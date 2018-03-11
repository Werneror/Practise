# LearnNodejs

这些是我[学习Node.js](http://www.runoob.com/nodejs/)时写的代码。


## [server.js](server.js)

我的第一个Node.js程序，创建服务器，访问显示“Hello World”。


## [callback1.js](callback1.js)

阻塞式读取文件代码实例。


## [callback2.js](callback2.js)

非阻塞式读取文件代码实例。


## [eventEmitterTest.js](eventEmitterTest.js)

Node.js 事件循环-事件驱动程序实例。

疑惑在于该程序是输出是：

```
$ node main.js
连接成功。
数据接收成功。
程序执行完毕。
```

既然 Node.js 的每一个 API 都是异步的，那么为何“程序执行完毕。”是最后输出而不是最先输出？


## [event.js](event.js)
EventEmitter 用法的简单例子。


## [eventConnection.js](eventConnection.js)

EventEmitter 用法的复杂点的例子。

注：

1. listenerCount 是类方法所以写“require('events').EventEmitter.listenerCount(...)”而不写“eventEmitter.listenerCount(...)”
2. eventEmitter.on()与eventEmitter.addListener()没有区别


## [createBuffer.js](createBuffer.js)

创建缓冲区。

## [writeBuffer.js](writeBuffer.js)

写缓冲区。疑惑在于什么叫做“只部分解码的字符不会被写入”。


## [readBuffer.js](readBuffer.js)

读缓冲区。


## [bufferToJSON.js](bufferToJSON.js)

缓冲区转为JSON数据。


## [BufferOperation.js](BufferOperation.js)

缓冲区其他操作。


## [StreamOperation.js](StreamOperation.js)

流的操作实例。


## [compress.js](compress.js)

用链式流压缩文件。


## [decompress.js](decompress.js)

用链式流解压文件。


## [router.js](router.js)

http服务路由初探。


## [global.js](global.js)

Node.js 全局对象。


## [utilTest.js](utilTest.js)

Node.js 核心模块 util 使用实例。


## [file1.js](file1.js)

文件操作，包括打开、关闭、读、写文件。


## [file2.js](file2.js)

文件操作，包括截取、删除文件，创建、读取、删除目录。


## [request.js](request.js)

获取GET/POST请求参数。


## [osTest.js](osTest.js)

os 模块使用示例。


## [pathTest.js](pathTest.js)

path 模块使用示例。


## [serverBase.js](serverBase.js)

简单的静态文件 Web 服务器。


## [client.js](client.js)

Web 客户端示例代码。


## [expressDemo](expressDemo)

一个简单的 express 项目，实现了取 GET、POST 参数，读取 cookie，上传文件等功能。


## [RESTful.js](RESTful.js)

REST 风格的Web服务器，实现了增删查功能。


## [master.js](master.js)

子进程相关。


## [mysqlTest.js](mysqlTest.js)

nodejs 操作 Mysql 数据库。


## [mongodbTest.js](mongodbTest.js)

nodejs 操作 mongodb 数据库。
