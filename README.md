# pythonbox

## getall.py
用于获取由指定网站中的指定后缀的文件

-h	查看帮助

-v	查看版本信息

-w	指定目标网站，应该是完整的URL地址

-A	指定目标文件后缀名，需含“.”,若有多个，则连在一起写，不用加空格

例如：

getall.py -w http://www.wangning.site -A .jpg.png

存在的问题：可能陷入url死循环而使程序停不下来。

##help.py
用于将python内置的帮助信息输出到文件

##T2与Mx的关系图.py
用于绘制T的平方和Mx的关系图

##tjdax.py
用于遍历tjdx学生证件照

##vuls2.0-beta.py
用于从NVD网站获取漏洞信息

##弗郎和费衍射绘图.py
用于绘制弗郎和费衍射绘图

##音叉U-f关系曲线.py
用于绘制音叉U-f关系曲线

##2^16prime.py
用于计算2^16内的所有质数

##2^16prime.txt
计算好的2^16内的所有质数

##2^32prime.py
用于计算2^32内的所有质数

##caesar.py
凯撒加密

##pushbox.py
推箱子小游戏，
需要gifs文件夹下的gif文件支持。

##rateList.py
爬去天猫评论信息的爬虫，获得的数据保存于数据库中。
若想使用该程序，请进行如下操作：

### 1.配置邮箱
修改在程序开头处的管理员邮箱，这个邮箱会接收程序运行的错误信息和完成信息：

	receiver = ["xxx@xxx.xxx",] 

正确配置函数 send163mail中的作为发件邮箱的163邮箱：

    sender = '************@163.com'  #设置发件邮箱，一定要自己注册的邮箱
    pwd = '************'  #设置发件邮箱的密码，等会登陆会用到

### 2.配置数据库
首先修改数据库配置部分：

	#在此处设置数据库连接信息
	db_config = {
	    "hostname": "localhost",#主机名
	    "username": "root",#数据库用户名
	    "password": "root",#数据库密码
	    "databasename": "test",#要存入数据的数据库名
	    }

然后进入Mysql执行一下语句创建数据库：

	CREATE DATABASE test DEFAULT charACTER SET utf8 COLLATE utf8_general_ci;

数据库名test可以随意修改，但两处要相同。
### 3.准备itemId.txt 和sellerId.txt

需要准备好各商品的itemId.txt 和sellerId.txt，同一类商品的itemId和sellerId分别存放在同一个文件中并放在以商品类别名命名的文件夹中，如下所示：

	 . 
	├── abc 
	│   ├── itemId.txt 
	│   └── sellerId.txt 
	├── def 
	│   ├── itemId.txt 
	│   └── sellerId.txt 
	├── ghi 
	│   ├── itemId.txt 
	│   └── sellerId.txt 
	└── rateList.py 

采用如上所示的文件目录结构最后生成的数据库会是这样的：

	mysql> show tables; 
	+----------------+ 
	| Tables_in_test | 
	+----------------+ 
	| abc            | 
	| def            | 
	| ghi            | 
	+----------------+ 

表abc中的数据是根据目录abc下的sellerId.txt 和itemId.txt 文件采集的。

### 4.其他提示

在云主机使用nohup python2 rateList.py &命令（执行后若无命令提示符可按回车）可以确保退出ssh后爬虫程序继续运行。
用ls命令查看日志文件的文件名就可以知道爬取进度。使用tail命令查看日志文件的最后几行，可以方便的追踪日志。

##crypto.py
密码学相关的运算

##LocationInfo.py和LocationInfo_en.py

全球各大洲国家主要城市的信息，有中英文


##BaiDuTranslate.py 

调用百度翻译API的demo

##createRAMtxt.py

用来生成verilog的$readmemb所需的文件

##idcard.py

穷举带*的身份证号的可能情况

##UDPtalk.py

基于UDP协议的内网聊天程序

##SH_char.py

用于生成shellcode中产生字符串的指令
shellcode中经常要用到字符串作为API的参数，这些字符串需要自己用汇编指令生成，比较麻烦，所以写了这个脚本。
只支持ASCII码。
