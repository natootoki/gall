import os
import time
import keyboard
import pynput
from pynput import mouse, keyboard

button = {}
button["q"] = False
button["up"] = False
button["down"] = False
button["right"] = False
button["left"] = False

unique = {}
unique["q"] = False
unique["up"] = False
unique["down"] = False
unique["right"] = False
unique["left"] = False

loop = True

player = "◆"

global_x = 0
global_y = 0

x_min = 0
x_max = 7

y_min = 0
y_max = 7

# マウス系フラグ制御
def move(x, y):
    print('マウスポインターは {0} へ移動しました'.format((x, y)))

def click(x, y, button, pressed):
    print('{2} が {0} された座標： {1}'.format(
        'Pressed' if pressed else 'Released',(x, y), button))
    if not pressed:     # クリックを離したら
        return False    # Listenerを止める

def scroll(x, y, dx, dy):
    print('{0} スクロールされた座標： {1}'.format(
        'down' if dy < 0 else 'up',(x, y)))

mouse_listener = mouse.Listener(
    on_move=move,
    on_click=click,
    on_scroll=scroll)
#mouse_listener.start()

# キーボード系フラグ制御
def press(key):
    global global_x
    global global_y
    global button
    global unique
    try:
        #print('アルファベット {0} が押されました'.format(key.char))
        if "{0}".format(key.char) == "q":
            if not button["q"]:
                unique["q"] = True
            button["q"] = True
    except AttributeError:
        if "{0}".format(key) == "Key.up":
            if not button["up"]:
                unique["up"] = True
            button["up"] = True
        if "{0}".format(key) == "Key.down":
            if not button["down"]:
                unique["down"] = True
            button["down"] = True
        if "{0}".format(key) == "Key.right":
            if not button["right"]:
                unique["right"] = True
            button["right"] = True
        if "{0}".format(key) == "Key.left":
            if not button["left"]:
                unique["left"] = True
            button["left"] = True

def release(key):
    # print('{0} が離されました'.format(key))
    # if key == keyboard.Key.esc:     # escが押された場合
    #     return False    # listenerを止める
    global global_x
    global global_y
    global button
    global unique
    try:
        #print('アルファベット {0} が押されました'.format(key.char))
        if "{0}".format(key.char) == "a":
            button["a"] = False
    except AttributeError:
        if "{0}".format(key) == "Key.up":
            button["up"] = False
        if "{0}".format(key) == "Key.down":
            button["down"] = False
        if "{0}".format(key) == "Key.right":
            button["right"] = False
        if "{0}".format(key) == "Key.left":
            button["left"] = False

listener = keyboard.Listener(
    on_press=press,
    on_release=release)
listener.start()

#処理
#1push1処理
while loop:
    if unique["up"]:
        global_y += 1
    elif unique["down"]:
        global_y -= 1
    elif unique["right"]:
        global_x += 1
    elif unique["left"]:
        global_x -= 1
    elif unique["q"]:
        loop = False

    unique["up"] = False
    unique["down"] = False
    unique["right"] = False
    unique["left"] = False
    unique["q"] = False

    if global_x < x_min:
        global_x = x_min
    elif global_x > x_max:
        global_x = x_max

    if global_y < y_min:
        global_y = y_min
    elif global_y > y_max:
        global_y = y_max
    os.system('cls')
    # print(global_x, global_y)
    
    #ステージ描画
    for i in range(8):
        for j in range(7):
            if global_x == j and global_y == 7-i:
                print(player, end="")
            else:    
                print("□", end="")
        if global_x == 7 and global_y == 7-i:
            print(player)
        else:
            print("□")
    
    time.sleep(0.05)
    

os.system('cls')

# os.system('cls')