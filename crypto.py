# -*- coding: utf-8 -*-
import copy
def gcd(a, b):
    if a < b:
        a, b = b, a
    while b != 0:
        temp = a % b
        a = b
        b = temp
    return a

def inverse(a,m):
    '''返回整数a在模m的有限域中的逆元，若无逆元则返回0'''
    for i in range(1,m):
        if (a*i)%m==1:
            return i
    return 0

def solveone(a, b, m):
    '''解同余式ax=b(mod m)，有解则返回解，否则返回None'''
    #print 'solveone',a,b,m
    am = gcd(a,m)#am是a和m的最大公约数
    if b==1:
        if am != 1:
            return None
        else:
            return inverse(a,m)
    else:
        if b%am==0:
            return (inverse(a/am,m/am)*b)%m/am
        else:
            return None

def solvefirst(a, b, m):
    '''求解模m的域上的多元一次方程组的第一个
    未知数的解，a是系数矩阵(二维列表)，b是值列表'''
    l = len(a)
    x = []
    for row in a:
        if len(row)!=l:
            print u'希望是一个方阵'
            return
        for number in range(0,l):
            row[number] = row[number]%m

    if len(b)!=l:
        print u'b的长度和a不匹配'
        return
    for number in range(0,l):
        b[number] = b[number]%m

    for row, e in zip(a,b):
        row.append(e)
    i = l-1
    #print "#"*30
    #for row in a:
    #    print row 
    #print "#"*30
    while i>0:
        lastrow = a[i-l]
        j = 1
        while lastrow[i-l-1]==0 and -(i-l-j)<l:
            #print i-l-j
            lastrow = a[i-l-j]
            j+=1
        for row in a[:i-l]:
            rowlastrowelement = row[i-l-1]
            if rowlastrowelement ==0:
                continue
            lastrowlastrowelement = lastrow[i-l-1]
            #print 'rowlastrowelement',rowlastrowelement
            #print 'lastrowlastrowelement',lastrowlastrowelement
            for number in range(0,l+1):
                #print row,lastrow, number
                row[number] = row[number]*lastrowlastrowelement%m
                lastrow[number] = lastrow[number]*rowlastrowelement%m
                row[number] = (row[number]-lastrow[number])%m
            #for row in a:
            #    print row 
        i = i-1
    x = solveone(a[0][0], a[0][-1], m)
    return x

def solve(a, b, m):
    '''求解模m的域上的多元一次方程组的的解，
    a是系数矩阵(二维列表)，b是值列表，返回一个一维数组x'''
    l = len(a)
    x = []
    for i in range(0,l):
        x.append(solvefirst(copy.deepcopy(a), b[:], m))
        a = a[1:]
        b = b[1:]
        for j in range(0,len(a)):
            b[j] = (b[j]-a[j][0]*x[-1])%26
            a[j] = a[j][1:]
    return x
            
if __name__ == '__main__':
    m = 26
    a = [[0,3,8,1], [18,15,11,1],[0,24,4,1],[3,4,16,1]]
    b1 = [3,12,14,23]
    b2 = [18,18,15,11]
    b3 = [17,8,11,9]

    x1 = solve(a,b1,m)
    x2 = solve(a,b2,m)
    x3 = solve(a,b3,m)

    print x1
    print x2
    print x3
