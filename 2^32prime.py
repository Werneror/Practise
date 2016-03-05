#coding:utf-8
import math
def IsPrimeByList(n, filename):
    """通过filename给定的质数表判断整数n是否是质数"""
    #判断n的类型，如果不是整数，则一定不是素数，返回False
    if not isinstance(n, int):
        return False        
    #若n为-1,0,1则不是整数，返回False
    if n==1 or n==-1 or n==0 :
        return False
    #若n为负数，则将其取反
    if n<0 :
        n = -n
    #若n为2，则是素数，返回True
    if n==2 :
        return True
    #若n为偶数，则返回False
    if n%2==0 :
        return False
    #遍历判断小于根号n的质数（质数表中给出），判断是否整除n
    sqn = math.sqrt(n)
    flist = open(filename, "r")
    for i in flist:
        i = int(i)
        if n%i==0 :
            flist.close()
            return False
        if i > sqn :
            flist.close()
            return True
    return True

f = open("2^32prime.txt", "a")
n = 2
maxn = 2**32
while n<=maxn :
    if IsPrimeByList(n, "2^32prime.txt"):
        f.write(str(n)+"\n")
    n += 1
f.close()
