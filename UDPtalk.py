#coding=utf-8
import sys
import threading
from socket import *
from time import ctime,sleep

#指定编码为utf8
reload(sys)  
sys.setdefaultencoding('utf8')  

def check_ip(ipaddr):
        '''验证IP地址的有效性'''
        addr=ipaddr.strip().split('.')  #切割IP地址为一个列表
        #print addr
        if len(addr) != 4:  #切割后列表必须有4个参数
                print "check ip address failed!"
                sys.exit()
        for i in range(4):
                try:
                        addr[i]=int(addr[i])  #每个参数必须为数字，否则校验失败
                except:
                        print "check ip address failed!"
                        sys.exit()
                if addr[i]<=255 and addr[i]>=0:    #每个参数值必须在0-255之间
                        pass
                else:
                        return False
                i+=1
        else:
                return True
                
def check_port(port):
    """验证输入的字符串是否是一个合法的端口号"""
    if(port.isdigit()):
        try:
            portnum = int(port)
        except:
            return False
        if(portnum>=0 and portnum<=65535):
            return True
        else:
            return False
    else:
        return False

def listion(myport):
    serverPort = myport
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        print "Y:\n"+message.encode(sys.stdin.encoding)
        print "I: "

def say(yourip, yourport):
    serverName = yourip
    serverPort = yourport
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    while True:
        message = raw_input('I:\n').decode(sys.stdin.encoding)
        if message=='q':
            message = "[WARNING]The other party has been offline."
            clientSocket.sendto(message, (serverName, serverPort))
            break
        clientSocket.sendto(message, (serverName, serverPort))
    clientSocket.close()

help = u'''
本程序用UDP作为运输层协议，仅供位于同一内网的主机间通信
本程序有三个参数，依次是对方IP地址，对方的UDP端口号，自己的UDP端口号
为正常通信，通信双方的“对方的UDP端口号”和“自己的UDP端口号”要对应
下面是命令示例，I和Y分别表示通信双方
I:  python UDPtalk.py 192.168.56.2 12000 12001
Y:  python UDPtalk.py 192.168.56.3 12001 12000
联系作者：me@wangning.site
2016.10.17
'''

if __name__ == '__main__':
    print "Welcome to use the UDPtalk."
    if len(sys.argv)==1 or sys.argv[1]=='-h':
        print help
        sys.exit()
    if  len(sys.argv)!=4:
        print "Please enter the appropriate parameters."
        sys.exit()
    yourip = sys.argv[1]
    if(not check_ip(yourip)):
        print "Please enter the correct IP address."
        sys.exit()
    yourport  = sys.argv[2]
    if(not check_port(yourport)):
        print "Please enter each other's port number correctly."
        sys.exit()
    else:
        yourport = int(sys.argv[2])
    myport = sys.argv[3]
    if(not check_port(myport)):
        print "Please enter your port number correctly."
        sys.exit()
    else:
        myport = int(sys.argv[3])
    threads = []
    t1 = threading.Thread(target=listion, args=(myport,))
    threads.append(t1)
    t2 = threading.Thread(target=say, args=(yourip, yourport,))
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print "Exit at %s" %ctime()
