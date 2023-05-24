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

global_x = 0
global_y = 0

# sample1.py
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

# sample2.py
def press(key):
    global global_x
    global global_y
    global button
    try:
        #print('アルファベット {0} が押されました'.format(key.char))
        if "{0}".format(key.char) == "a":
            global_x += 1
        print(global_x, global_y)
    except AttributeError:
        if "{0}".format(key) == "Key.up":
            button["up"] = True
        if "{0}".format(key) == "Key.down":
            button["down"] = True
        if "{0}".format(key) == "Key.right":
            button["right"] = True
        if "{0}".format(key) == "Key.left":
            button["left"] = True

def release(key):
    # print('{0} が離されました'.format(key))
    # if key == keyboard.Key.esc:     # escが押された場合
    #     return False    # listenerを止める
    global button
    try:
        #print('アルファベット {0} が押されました'.format(key.char))
        if "{0}".format(key.char) == "a":
            global_x += 1
        print(global_x, global_y)
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

while True:
    if button["up"]:
        global_y += 1
    elif button["down"]:
        global_y -= 1
    elif button["right"]:
        global_x += 1
    elif button["left"]:
        global_x -= 1
    os.system('cls')
    print(global_x, global_y)
    time.sleep(0.05)
    

os.system('cls')

# time.sleep(1)

# os.system('cls')
# print("□■□□")
# print("□□□□")
# print("□□□□")
# print("□□□□")
# time.sleep(1)

# os.system('cls')
# print("□□□□")
# print("□■□□")
# print("□□□□")
# print("□□□□")
# time.sleep(1)

# os.system('cls')
# print("□□□□")
# print("□□□□")
# print("□■□□")
# print("□□□□")
# time.sleep(1)

# os.system('cls')
# print("□□□□")
# print("□□□□")
# print("□□□□")
# print("□■□□")
# time.sleep(1)

# os.system('cls')