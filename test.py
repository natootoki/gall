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

stage_w = 24
stage_h = 12

player_x = 0
player_y = 0

goal = "★"

goal_x = stage_w-1
goal_y = stage_h-1

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
    global player_x
    global player_y
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
    global player_x
    global player_y
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

################################処理################################

while loop:

    #1push1処理
    if unique["up"]:
        player_y += 1

    if unique["down"]:
        player_y -= 1

    if unique["right"]:
        player_x += 1

    if unique["left"]:
        player_x -= 1

    if unique["q"]:
        loop = False

    unique["up"] = False
    unique["down"] = False
    unique["right"] = False
    unique["left"] = False
    unique["q"] = False

    if player_x < 0:
        player_x = 0
    elif player_x > stage_w-1:
        player_x = stage_w-1

    if player_y < 0:
        player_y = 0
    elif player_y > stage_h-1:
        player_y = stage_h-1

    os.system('cls')
    # print(player_x, player_y)
    
    #ステージ描画
    for i in range(stage_h):
        for j in range(stage_w):
            if player_x == j and player_y == (stage_h-1)-i:
                print(player, end="")
            elif goal_x == j and goal_y == (stage_h-1)-i:
                print(goal, end="")
            else:    
                print("□", end="")
        print("")
    
    time.sleep(0.05)

    if player_x == goal_x and player_y == goal_y:
        loop = False

os.system('cls')

# os.system('cls')