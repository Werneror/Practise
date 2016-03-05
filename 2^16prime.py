import math
#coding:utf-8
def SimpleIsPrime(n):
    '''不借助外力的、简单的判断n是否是质数，是质数返回True，否则返回False'''
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
    #遍历判断小于根号n的奇数，判断是否整除n
    i = 3
    sqn = math.sqrt(n)
    while i<sqn :
        if n%i==0 :
           return False
        i += 2
    #若无一整除n，则n必为素数，返回True
    return True

f = open("2^16prime.txt", "w")
n = 2
maxn = 2**16
while n<=maxn :
    if SimpleIsPrime(n):
        f.write(str(n)+"\n")
    n += 1
f.close()
