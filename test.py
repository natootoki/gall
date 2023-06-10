import os
import time
import keyboard
import random

import pynput
from pynput import mouse, keyboard

import pygame
from pygame.locals import *
import sys, random

# 色を定義
black = (0, 0, 0)
red = (255, 0, 0)

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

stroke = True

loop = True

stage_min_w = 65
stage_max_w = 129
stage_min_h = 33
stage_max_h = 65
difficulty = 1 #採用する最低の難易度。1が最低

tile_size = 8

stage_w = random.randrange(stage_min_w, stage_max_w, 2) #小さすぎると壁が少なすぎる
stage_h = random.randrange(stage_min_h, stage_max_h, 2) #小さすぎると壁が少なすぎる
print("stage_w", stage_w)
print("stage_h", stage_h)

player = "◆"

player_x = 0
player_y = 0

goal = "★"

#goal_x = random.randrange(stage_w)
#goal_y = random.randrange(stage_h)

goal_x = stage_w-1
goal_y = stage_h-1


is_goal = False

wall = "■"
wall_num = max(1, stage_w * stage_h // 2 )

test = True
test_num = 0
while test:

    wall_list = []

    #フォーマット（固定の部分）を作る
    for i in range(stage_h):
        for j in range(stage_w):
            if i%2 == 1 and j%2 == 1:
                wall_list.append([j, (stage_h - 1) - i])

    #壁どうしが重ならないようにランダムに配置する
    # for i in range(wall_num):
    #     while True:
    #         temp_wall_x = random.randrange(stage_w)
    #         temp_wall_y = random.randrange(stage_h)
    #         if not [temp_wall_x, temp_wall_y] in wall_list and not [temp_wall_x, temp_wall_y] == [player_x, player_y] and not [temp_wall_x, temp_wall_y] == [goal_x, goal_y]:
    #             wall_list.append([temp_wall_x, temp_wall_y])
    #             break

    inner_x = random.randrange(stage_w)
    inner_y = random.randrange(stage_h)
    for i in range(stage_h):
        for j in range(stage_w):
            if not (stage_h-1)-i == stage_h-1 and not (stage_h-1)-i == 0 and not j == stage_w-1 and not j == 0:
                if not [j, (stage_h-1)-i -1] in wall_list and not [j, (stage_h-1)-i +1] in wall_list and not [j -1, (stage_h-1)-i] in wall_list and not [j +1, (stage_h-1)-i] in wall_list:
                    inner_x = j
                    inner_y = (stage_h-1)-i
                    while True:
                        connect = random.randrange(4)

                        if connect == 0 and not inner_y == stage_h-1:
                            wall_list.append([inner_x, inner_y +1])
                            break
                        elif connect == 1 and not inner_y == 0:
                            wall_list.append([inner_x, inner_y -1])
                            break
                        elif connect == 2 and not inner_x == stage_w-1:
                            wall_list.append([inner_x +1, inner_y])
                            break
                        elif connect == 3 and not inner_x == 0:
                            wall_list.append([inner_x -1, inner_y])
                            break

    can_reach = [[0] * stage_w for i in range(stage_h)]
    can_reach[player_x][player_y] = 1

    #print(can_reach)

    change = True

    while change:
        # time.sleep(0.5)
        change=False
        for i in range(stage_h):
            for j in range(stage_w):
                if can_reach[(stage_h-1)-i][j] >= 1 and (not (stage_h-1)-i == goal_y or not j == goal_x):
                    #print(j, (stage_h-1)-i)
                    if not (stage_h-1)-i == stage_h-1:

                        if not [j, ((stage_h-1)-i)+1] in wall_list and can_reach[((stage_h-1)-i)+1][j] == 0:
                            can_reach[((stage_h-1)-i)+1][j] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True

                    if not (stage_h-1)-i == 0:

                        if not [j, ((stage_h-1)-i)-1] in wall_list and can_reach[((stage_h-1)-i)-1][j] == 0:
                            can_reach[((stage_h-1)-i)-1][j] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True
                        
                    if not j == stage_w-1:

                        if not [j+1, (stage_h-1)-i] in wall_list and can_reach[(stage_h-1)-i][j+1] == 0:
                            can_reach[(stage_h-1)-i][j+1] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True
                        
                    if not j == 0:

                        if not [j-1, (stage_h-1)-i] in wall_list and can_reach[(stage_h-1)-i][j-1] == 0:
                            can_reach[(stage_h-1)-i][j-1] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True
                        
    # if can_reach[goal_y][goal_x] == 1:
    # if can_reach[goal_y][goal_x] >= 1 and can_reach[0][goal_x] >= 1 and can_reach[goal_y][0] >= 1 and can_reach[goal_y][goal_x] >= ((stage_w - 1) + (stage_h - 1)) * difficulty:
    if can_reach[goal_y][goal_x] >= ((stage_w - 1) + (stage_h - 1)) * difficulty:
        test = False
    else:
        test_num += 1
        if can_reach[goal_y][goal_x] >= 1:
            print(stage_w, stage_h, stage_w * stage_h, wall_num, can_reach[goal_y][goal_x], test_num)

# 最短の道のりだけ表示したい場合の処理
# wall_list = []
# for i in range(stage_h):
#     for j in range(stage_w):
#         wall_list.append([j, i])

# inner_x = goal_x
# inner_y = goal_y
# print("remove", inner_x, inner_y)
# wall_list.remove([inner_x, inner_y])

# for i in range(can_reach[goal_y][goal_x]):
#     if not inner_y == stage_h-1:
#         if can_reach[inner_y+1][inner_x] == can_reach[goal_y][goal_x]-i:
#             inner_y += 1
#             print("remove", inner_x, inner_y)
#             wall_list.remove([inner_x, inner_y])
#             continue
#     if not inner_y == 0:
#         if can_reach[inner_y-1][inner_x] == can_reach[goal_y][goal_x]-i:
#             inner_y -= 1
#             print("remove", inner_x, inner_y)
#             wall_list.remove([inner_x, inner_y])
#             continue
#     if not inner_x == stage_w-1:
#         if can_reach[inner_y][inner_x+1] == can_reach[goal_y][goal_x]-i:
#             inner_x += 1
#             print("remove", inner_x, inner_y)
#             wall_list.remove([inner_x, inner_y])
#             continue
#     if not inner_x == 0:
#         if can_reach[inner_y][inner_x-1] == can_reach[goal_y][goal_x]-i:
#             inner_x -= 1
#             print("remove", inner_x, inner_y)
#             wall_list.remove([inner_x, inner_y])
#             continue


#到達可能域だけ見たい場合にはコメント解除する
# loop = False

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

def main():
    global player_x, player_y, stroke, is_goal, stage_w, stage_h, tile_size, wall_list

    pygame.init()
    pygame.display.set_caption("maze")
    screen = pygame.display.set_mode((stage_w*tile_size, stage_h*tile_size))

    while True:

        # 背景
        screen.fill(black)
        # 長方形
        for i in range(stage_h):
            for j in range(stage_w):
                if player_x == j and player_y == (stage_h-1)-i:
                    # 円
                    pygame.draw.circle(screen, red, (j*tile_size + tile_size/2, i*tile_size + tile_size/2), tile_size/2)
                elif goal_x == j and goal_y == (stage_h-1)-i:
                    pygame.draw.polygon(screen, red, [[(j+1/2)*tile_size, i*tile_size], [(j+1)*tile_size, (i+1/2)*tile_size], [(j+1/2)*tile_size, (i+1)*tile_size], [j*tile_size, (i+1/2)*tile_size]])
                elif [j, (stage_h-1)-i] in wall_list:
                    # 長方形
                    pygame.draw.rect(screen, red, (j*tile_size, i*tile_size, tile_size, tile_size))
        # 描画
        pygame.display.update()
        # イベントを処理する --- (*5)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                print("hello!")

        #1push1処理
        if unique["up"] and not [player_x, player_y+1] in wall_list:
            player_y += 1
            stroke = True

        if unique["down"] and not [player_x, player_y-1] in wall_list:
            player_y -= 1
            stroke = True

        if unique["right"] and not [player_x+1, player_y] in wall_list:
            player_x += 1
            stroke = True

        if unique["left"] and not [player_x-1, player_y] in wall_list:
            player_x -= 1
            stroke = True

        if unique["q"]:
            break

        unique["up"] = False
        unique["down"] = False
        unique["right"] = False
        unique["left"] = False
        unique["q"] = False

        #端っこ判定x
        if player_x < 0:
            player_x = 0
        elif player_x > stage_w-1:
            player_x = stage_w-1

        #端っこ判定y
        if player_y < 0:
            player_y = 0
        elif player_y > stage_h-1:
            player_y = stage_h-1

        #ステージ描画
        # if stroke:
        
        #     os.system('cls')
        #     # print(player_x, player_y)
            
        #     for i in range(stage_h):
        #         for j in range(stage_w):
        #             if player_x == j and player_y == (stage_h-1)-i:
        #                 print(player, end="")
        #             elif goal_x == j and goal_y == (stage_h-1)-i:
        #                 print(goal, end="")
        #             elif [j, (stage_h-1)-i] in wall_list:
        #                 print(wall, end="")
        #             else:    
        #                 print("□", end="")
        #         print("")
            
            print(can_reach[goal_y][goal_x], stage_w, stage_h)
            stroke = False

        time.sleep(0.05)

        if player_x == goal_x and player_y == goal_y:
            is_goal = True
            break

if __name__ == '__main__':
    main()

os.system('cls')

if is_goal:
    print("goal!!!!")
    time.sleep(3)

os.system('cls')

for i in range(stage_h):
    for j in range(stage_w): 
        if can_reach[(stage_h-1)-i][j] == 0:
            print("0", end="")
        else:
            print("1", end="")
    print("")

# os.system('cls')