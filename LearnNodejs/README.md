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
