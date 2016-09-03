# ^_^ coding:utf-8 ^_^ 
def checkcode(idstr):
    """计算身份证号的最后一位验证码,
       输入参数是身份证号的前17位，是字符串,
       输出为字符，是验证码"""
    if(len(idstr)!=17):
        return False
    s = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    p = ["1","0","x","9","8","7","6","5","4","3","2"]
    sum = 0
    i=0
    for num in idstr:
        sum +=int(num)*s[i]
        i+=1
    return p[sum%11]

def verify_by_checkcode(idstr):
    """用最后一位校验码校验身份证号是否有效
       输入为18位的身份证号"""
    if len(idstr)!=18:
        return False
    if checkcode(idstr[:17])==idstr[17]:
        return True
    else:
        return False

def verify_by_birthday(idstr):
    """用生日校验身份证号是否有效
       输入为18位的身份证号"""
    try:
        year = int(idstr[6:10])
        if year<1900 or year>2020:
            return False
    except ValueError:
        pass
    try:
        mouth = int(idstr[10:12])
        if mouth<1 or mouth >12:
            return False
    except ValueError:
        pass
    try:
        day = int(idstr[12:14])
        if day<1 or day >31:
            return False
    except ValueError:
        pass
    bigmouth = [1,3,5,7,8,10,12]
    if (not mouth in bigmouth) and day>30:
        return False    #不是大月而一个月多余30天
    if mouth==2:
        if (year%4==0 and year%100!=0) or year%400==0: #闰年
            if day>29:
                return False
        else:
            if day>28:
                return False
    return True

def traversal(idstr):
    """将*号用数字遍历，返回遍历结果
    输入应该是这样的“622630199*112*04*0”
    在遍历过程中会验证生日是否符合实际
    """
    heaplist = []
    heaplist.append(idstr)
    while True:
        idstr=heaplist[0]
        try:
            position = idstr.index("*")
        except ValueError:
            break; 
        heaplist=heaplist[1:]
        l=idstr.split("*" ,1)
        if position==6:                   #年份的第一个数字
            span = [1,2]
        elif position==7:                 #年份的第二个数字
            span = [9,0]
        elif position==10:                #月份的第一个数字
            span = [1,0]
        elif position==12:                #日期的第一个数字
            span = [0,1,2,3]
        else:
            span = range(10)
        for i in span:
            temp = l[0]+str(i)+l[1]
            if verify_by_birthday(temp):
                heaplist.append(temp) 
    return heaplist


def guess_id_num(idstr):
    """用效验码和地方编码、生日得到有星号的身份证号的可能情况"""
    possible = []
    l = traversal(idstr)
    for idstr in l:
        if verify_by_checkcode(idstr):
            possible.append(idstr)
    return possible
if __name__ == '__main__':
    idstr="620602*98305*44687"
    l = guess_id_num(idstr)
    for i in l:
        print i
    print "len=",len(l)
