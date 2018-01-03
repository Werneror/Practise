# coding:utf-8
key = 5 
s = 'Happy New Year!'
s = s.upper()
m = ''
for char in s:
    if ord(char) >= ord('A') and ord(char) <= ord('Z'):
        char = chr(ord(char) + key)
        if ord(char) > ord('Z'):
            char = chr(ord('A') + ord(char) - ord('Z') -1)
    m += char
print(m)
