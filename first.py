import random

#変数管理台帳
#hoge：テキトーな数字

#print
print("Hello, world!")

#変数の宣言、参照
hoge = 1
print(hoge)

#if文
if hoge:
    print("hoge=true")

#for文
for i in range(10):
    print(i)

#各種演算
print(1+1)
print(2-1)
print(2*3)
print(5/2)
print(33%7)
print(7//2)
print(7**2)

#ランダム
print(random.randrange(10))

huga = [1,2,3,4,5]
for h in huga:
    print("huga", h)
    huga.remove(h)
print(huga)