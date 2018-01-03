# coding:utf-8
s = raw_input()     #输入字符串
s = s[::-1]              #翻转输入的字符串

print "xor ebx,ebx ;ebx=0"
print "mov dword ptr [ebp-04h], ebx"

m = 4
n = 1
tmp_h = ""
tmp_s = ""
for i in s:
    tmp_h += str(hex(ord(i))).replace("0x","")
    tmp_s = i + tmp_s
    if n%4==0:
        m += 4
        print "mov dword ptr [ebp-0"+str(hex(m)).replace("0x", "")+"h], 0"+tmp_h  +"h;"+tmp_s
        tmp_h = ""
        tmp_s = ""
    n += 1

if len(tmp_h)==8:
    m += 4
    print "mov dword ptr [ebp-0"+str(hex(m)).replace("0x", "")+"h], 0"+tmp_h  +"h;"+tmp_s
if len(tmp_h)==6:
    m += 2
    print "mov word ptr [ebp-0"+str(hex(m)).replace("0x", "")+"h], 0"+tmp_h[:4]  +"h;"+tmp_s[1:]
    m += 1
    print "mov byte ptr [ebp-0"+str(hex(m)).replace("0x", "")+"h], 0"+tmp_h[4:]  +"h;"+tmp_s[:1]
if len(tmp_h)==4:
    m += 2
    print "mov word ptr [ebp-0"+str(hex(m)).replace("0x", "")+"h], 0"+tmp_h  +"h;"+tmp_s
if len(tmp_h)==2:
    m += 1
    print "mov byte ptr [ebp-0"+str(hex(m)).replace("0x", "")+"h], 0"+tmp_h  +"h;"+tmp_s

print "lea eax, [ebp-0"+str(hex(m)).replace("0x", "")+"h]"
