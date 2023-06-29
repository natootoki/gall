import random

#変数管理台帳
#hoge：テキトーな数字

# #print
# print("Hello, world!")

# #変数の宣言、参照
# hoge = 1
# print(hoge)

# #if文
# if hoge:
#     print("hoge=true")

# #for文
# for i in range(10):
#     print(i)

# #各種演算
# print(1+1)
# print(2-1)
# print(2*3)
# print(5/2)
# print(33%7)
# print(7//2)
# print(7**2)

# #ランダム
# print(random.randrange(10))

# # リストの0番目の要素、1番目の要素と繰り返していくので、一個飛ばしになる
# huga = [1,2,3,4,5]
# for h in huga:
#     print("huga", h)
#     huga.remove(h)
# print(huga)

# # リストの終わりに辿り付けず無限ループになる
# huga = [1,2,3,4,5]
# for h in huga:
#     print("huga", h)
#     huga.append(h+5)
# print(huga)

# 配列の要素を奇数と偶数に分ける処理
def calc(numbers):
    odd, even = [], []
    for number in numbers:
        if number % 2 == 0:
            even.append(number)
        else:
            odd.append(number)
    return even, odd

a, b = calc([1,2,3,4,5])

print(b)