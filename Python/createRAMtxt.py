# -*- coding: utf-8 -*-
def printb(s, l):
    n = bin(s)[2:]
    a = l - len(n)
    if a==0:
        print n
    elif a<0:
        n=n[a:]
        s = int(n,2)
        printb(s,l)
    else:
        print '0'*a+n
s = 0
while True:
    if s>=2**8:
        break
    printb(s, 8)
    s+=1
