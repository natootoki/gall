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
gray = (127, 127, 127)
white = (255, 255, 255)
# 赤橙黄緑青藍紫
colors = [(255, 0, 0), (255, 165, 0), (255, 241, 0), (0, 128, 0), (30, 144, 255), (15, 84, 116), (192, 48, 192)]

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

bg_color = black
out_wall_color = gray

color_change = 0

wh = 32 * 2 - 1
stage_min_w = wh
stage_max_w = wh
stage_min_h = wh
stage_max_h = wh
difficulty = 4/2 #採用する最低の難易度

tile_size = 15

stage_w = random.randrange(stage_min_w, stage_max_w+1, 2) #小さすぎると壁が少なすぎる
stage_h = random.randrange(stage_min_h, stage_max_h+1, 2) #小さすぎると壁が少なすぎる
print("stage_w", stage_w)
print("stage_h", stage_h)

player = "◆"
player_color = white

player_x = 0
player_y = 0

goal = "★"
goal_color = colors[2]

#goal_x = random.randrange(stage_w)
#goal_y = random.randrange(stage_h)

goal_x = stage_w-1
goal_y = stage_h-1

is_goal = False

wall = "■"
wall_num = max(1, stage_w * stage_h // 3 )
wall_min_length = 33
wall_color = [[0] * stage_w for i in range(stage_h)]
wall_cluster_num = 0

test = True
test_num = 0

#条件に合った迷路ができるまで生成とテストを繰り返す
while test:

    wall_list = []
    wall_length = [[0] * stage_w for i in range(stage_h)]
    wall_connect_list = []

    # フォーマット（固定の部分）を作る
    print("make format")

    for i in range(stage_h):

        for j in range(stage_w):

            if i%2 == 1 and j%2 == 1:
                wall_list.append([j, (stage_h - 1) - i])
                wall_length[(stage_h - 1) - i][j] = 1

    # 迷路を作る
    print("make maze")
    wall_ng_list = []
    change = True

    while change:
        change = False

        for i in range(stage_h):

            for j in range(stage_w):
                inner_x = j
                inner_y = (stage_h-1)-i

                if inner_x%2 == 1 and inner_y%2 == 1 and wall_length[inner_y][inner_x] < wall_min_length:
                    wall_connect_list = [[inner_x, inner_y]]
                    wall_candidate = []

                    for walls in wall_connect_list:
                                
                        if [walls[0], walls[1]+1] in wall_list and not [walls[0], walls[1]+1] in wall_connect_list:
                            wall_connect_list.append([walls[0], walls[1]+1])

                        if [walls[0], walls[1]-1] in wall_list and not [walls[0], walls[1]-1] in wall_connect_list:
                            wall_connect_list.append([walls[0], walls[1]-1])

                        if [walls[0]+1, walls[1]] in wall_list and not [walls[0]+1, walls[1]] in wall_connect_list:
                            wall_connect_list.append([walls[0]+1, walls[1]])

                        if [walls[0]-1, walls[1]] in wall_list and not [walls[0]-1, walls[1]] in wall_connect_list:
                            wall_connect_list.append([walls[0]-1, walls[1]])

                    for walls in wall_connect_list:
                        wall_length[walls[1]][walls[0]] = len(wall_connect_list)

                    if len(wall_connect_list) < wall_min_length:
                        change = True
                        count = 0

                        for walls in wall_connect_list:

                            if walls[0]%2==1 and walls[1]%2==1:

                                if not [walls[0], walls[1]+1] in wall_list and not [walls[0], walls[1]+1] in wall_ng_list and not [walls[0], walls[1]+1] in wall_candidate:

                                    if 0 < walls[0] and walls[0] < stage_w-1 and 0 < walls[1]+1 and walls[1]+1 < stage_h-1:
                                        wall_candidate.append([walls[0], walls[1]+1])
                                
                                if not [walls[0], walls[1]-1] in wall_list and not [walls[0], walls[1]-1] in wall_ng_list and not [walls[0], walls[1]-1] in wall_candidate:

                                    if 0 < walls[0] and walls[0] < stage_w-1 and 0 < walls[1]-1 and walls[1]-1 < stage_h-1:
                                        wall_candidate.append([walls[0], walls[1]-1])

                                if not [walls[0]+1, walls[1]] in wall_list and not [walls[0]+1, walls[1]] in wall_ng_list and not [walls[0]+1, walls[1]] in wall_candidate:

                                    if 0 < walls[0]+1 and walls[0]+1 < stage_w-1 and 0 < walls[1] and walls[1] < stage_h-1:
                                        wall_candidate.append([walls[0]+1, walls[1]])

                                if not [walls[0]-1, walls[1]] in wall_list and not [walls[0]-1, walls[1]] in wall_ng_list and not [walls[0]-1, walls[1]] in wall_candidate:

                                    if 0 < walls[0]-1 and walls[0]-1 < stage_w-1 and 0 < walls[1] and walls[1] < stage_h-1:
                                        wall_candidate.append([walls[0]-1, walls[1]])

                        if len(wall_candidate)>0:
                            inner_rand = random.randrange(len(wall_candidate))
                            wall_list.append([wall_candidate[inner_rand][0], wall_candidate[inner_rand][1]])                            

                            can_reach_left_to_right = False
                            can_reach = []

                            if wall_list[-1][0]%2==1:
                                can_reach.append([wall_list[-1][0]-1, wall_list[-1][1]])

                            elif wall_list[-1][1]%2==1:
                                can_reach.append([wall_list[-1][0], wall_list[-1][1]+1])

                            for reaches in can_reach:
                                            
                                if not [reaches[0], reaches[1]+1] in wall_list and not [reaches[0], reaches[1]+1] in can_reach:

                                    if 0 <= reaches[0] and reaches[0] <= stage_w-1 and 0 <= reaches[1]+1 and reaches[1]+1 <= stage_h-1:
                                        can_reach.append([reaches[0], reaches[1]+1])

                                if not [reaches[0], reaches[1]-1] in wall_list and not [reaches[0], reaches[1]-1] in can_reach:

                                    if 0 <= reaches[0] and reaches[0] <= stage_w-1 and 0 <= reaches[1]-1 and reaches[1]-1 <= stage_h-1:
                                        can_reach.append([reaches[0], reaches[1]-1])

                                if not [reaches[0]+1, reaches[1]] in wall_list and not [reaches[0]+1, reaches[1]] in can_reach:

                                    if 0 <= reaches[0]+1 and reaches[0]+1 <= stage_w-1 and 0 <= reaches[1] and reaches[1] <= stage_h-1:
                                        can_reach.append([reaches[0]+1, reaches[1]])

                                if not [reaches[0]-1, reaches[1]] in wall_list and not [reaches[0]-1, reaches[1]] in can_reach:

                                    if 0 <= reaches[0]-1 and reaches[0]-1 <= stage_w-1 and 0 <= reaches[1] and reaches[1] <= stage_h-1:
                                        can_reach.append([reaches[0]-1, reaches[1]])

                                if wall_list[len(wall_list)-1][0]%2==1:
                                    
                                    if [wall_list[-1][0]+1, wall_list[-1][1]] in can_reach:
                                        can_reach_left_to_right = True
                                        break

                                elif wall_list[-1][1]%2==1:

                                    if [wall_list[len(wall_list)-1][0], wall_list[-1][1]-1] in can_reach:
                                        can_reach_left_to_right = True
                                        break

                            if not can_reach_left_to_right:

                                if not [wall_list[-1][0], wall_list[-1][1]] in wall_ng_list:
                                    wall_ng_list.append([wall_list[-1][0], wall_list[-1][1]])
                                
                                # print("　×", wall_list[-1])
                                del wall_list[-1]

                            else:
                                pass
                                # print("　→", wall_list[-1])

    # 外壁に面している壁は1箇所だけつなげる
    print("out_wall_connect")
    finish_wall = []

    for i in range(stage_h):

        for j in range(stage_w):
            inner_x = j
            inner_y = (stage_h-1)-i

            # フォーマットの壁に対してのみ処理する
            if inner_x%2 == 1 and inner_y%2 == 1 and not [inner_x, inner_y] in finish_wall:
                wall_connect_list.append([inner_x, inner_y])
                change = True
                wall_connect_list = [[inner_x, inner_y]]

                while change:
                    change = False

                    # 到達できると分かっているマスに対して処理をする
                    for walls in wall_connect_list:
                        
                        # 下端じゃない場合処理をする
                        if not walls[1] == stage_h-1:
                            # 下のマスが壁でない、かつ、到達できると分かっていない場合、自分のマス+1の番号を振る
                            if [walls[0], walls[1]+1] in wall_list and not [walls[0], walls[1]+1] in wall_connect_list:
                                wall_connect_list.append([walls[0], walls[1]+1])
                                change = True

                        # 上端じゃない場合処理をする
                        if not walls[1] == 0:

                            if [walls[0], walls[1]-1] in wall_list and not [walls[0], walls[1]-1] in wall_connect_list:
                                wall_connect_list.append([walls[0], walls[1]-1])
                                change = True

                        # 右端じゃない場合処理をする
                        if not walls[0] == stage_w-1:

                            if [walls[0]+1, walls[1]] in wall_list and not [walls[0]+1, walls[1]] in wall_connect_list:
                                wall_connect_list.append([walls[0]+1, walls[1]])
                                change = True

                        # 左端じゃない場合処理をする
                        if not walls[0] == 0:

                            if [walls[0]-1, walls[1]] in wall_list and not [walls[0]-1, walls[1]] in wall_connect_list:
                                wall_connect_list.append([walls[0]-1, walls[1]])
                                change = True

                # 外壁に接しているかどうか判定する
                out_facing = False
                out_connect = False
                wall_facing_list = []

                for walls in wall_connect_list:

                    if walls[0]==1 or walls[0]==stage_w-2 or walls[1]==1 or walls[1]==stage_h-2:
                        out_facing = True
                        wall_facing_list.append([walls[0], walls[1]])

                    if walls[0]==0 or walls[0]==stage_w-1 or walls[1]==0 or walls[1]==stage_h-1:
                        out_connect = True
                        break
                
                if not out_connect and out_facing:

                    # 外壁に接しているマスをランダムに選択して伸ばす
                    while True:
                        inner_rand = random.randrange(len(wall_facing_list))

                        if wall_facing_list[inner_rand][0]%2==1 and wall_facing_list[inner_rand][1]%2==1:

                            if wall_facing_list[inner_rand][0]==1:
                                wall_list.append([wall_facing_list[inner_rand][0]-1, wall_facing_list[inner_rand][1]])
                                wall_connect_list.append([wall_facing_list[inner_rand][0]-1, wall_facing_list[inner_rand][1]])
                                # print("out_wall")
                                break

                            elif wall_facing_list[inner_rand][0]==stage_w-2:
                                wall_list.append([wall_facing_list[inner_rand][0]+1, wall_facing_list[inner_rand][1]])
                                wall_connect_list.append([wall_facing_list[inner_rand][0]+1, wall_facing_list[inner_rand][1]])
                                # print("out_wall")
                                break

                            elif wall_facing_list[inner_rand][1]==1:
                                wall_list.append([wall_facing_list[inner_rand][0], wall_facing_list[inner_rand][1]-1])
                                wall_connect_list.append([wall_facing_list[inner_rand][0], wall_facing_list[inner_rand][1]-1])
                                # print("out_wall")
                                break

                            elif wall_facing_list[inner_rand][1]==stage_h-2:
                                wall_list.append([wall_facing_list[inner_rand][0], wall_facing_list[inner_rand][1]+1])
                                wall_connect_list.append([wall_facing_list[inner_rand][0], wall_facing_list[inner_rand][1]+1])
                                # print("out_wall")
                                break
                    
                    for walls in wall_connect_list:
                        wall_length[walls[1]][walls[0]] = len(wall_connect_list)
                        wall_color[walls[1]][walls[0]] = colors[wall_cluster_num % len(colors)]
                        finish_wall.append(walls)
                    
                    wall_cluster_num += color_change

    print("root_test")

    can_reach = [[0] * stage_w for i in range(stage_h)]
    cant_reach = []
    can_reach[player_x][player_y] = 1

    # テスト進行中の間はループする。前の状態から変わらなくなったらテスト完了
    change = True
    max_reach = 1

    while change:
        change=False

        for i in range(stage_h):
            for j in range(stage_w):
                
                # 到達できると分かっているマスに対して処理をする
                if can_reach[(stage_h-1)-i][j] == max_reach:
                    
                    # 下端じゃない場合処理をする
                    if not (stage_h-1)-i == stage_h-1:
                        # 下のマスが壁でない、かつ、到達できると分かっていない場合、自分のマス+1の番号を振る
                        if not [j, ((stage_h-1)-i)+1] in wall_list and can_reach[((stage_h-1)-i)+1][j] == 0:
                            can_reach[((stage_h-1)-i)+1][j] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True

                    # 上端じゃない場合処理をする
                    if not (stage_h-1)-i == 0:

                        if not [j, ((stage_h-1)-i)-1] in wall_list and can_reach[((stage_h-1)-i)-1][j] == 0:
                            can_reach[((stage_h-1)-i)-1][j] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True

                    # 右端じゃない場合処理をする    
                    if not j == stage_w-1:

                        if not [j+1, (stage_h-1)-i] in wall_list and can_reach[(stage_h-1)-i][j+1] == 0:
                            can_reach[(stage_h-1)-i][j+1] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True

                    # 左端じゃない場合処理をする    
                    if not j == 0:

                        if not [j-1, (stage_h-1)-i] in wall_list and can_reach[(stage_h-1)-i][j-1] == 0:
                            can_reach[(stage_h-1)-i][j-1] = can_reach[((stage_h-1)-i)][j] + 1
                            change = True

        # 現在何マスまで探索が進んでいるのかを管理する
        max_column = []

        for i in range(stage_h):
            max_column.append(max(can_reach[i]))
    
        max_reach = max(max_column)

    for i in range(stage_h):

        for j in range(stage_w):
            inner_x = j
            inner_y = (stage_h-1)-i

            if inner_x%2==0 and inner_y%2==0 and not [inner_x, inner_y] in wall_list and can_reach[inner_y][inner_x] == 0:
                cant_reach.append([inner_x, inner_y])

    # 壁に色をつける
    for i in range(stage_h):

        for j in range(stage_w):
            inner_x = j
            inner_y = (stage_h-1)-i

            if inner_x%2 == 1 and inner_y%2 == 1:
                wall_connect_list = [[inner_x, inner_y]]

                for walls in wall_connect_list:
                            
                    if [walls[0], walls[1]+1] in wall_list and not [walls[0], walls[1]+1] in wall_connect_list:
                        wall_connect_list.append([walls[0], walls[1]+1])

                    if [walls[0], walls[1]-1] in wall_list and not [walls[0], walls[1]-1] in wall_connect_list:
                        wall_connect_list.append([walls[0], walls[1]-1])

                    if [walls[0]+1, walls[1]] in wall_list and not [walls[0]+1, walls[1]] in wall_connect_list:
                        wall_connect_list.append([walls[0]+1, walls[1]])

                    if [walls[0]-1, walls[1]] in wall_list and not [walls[0]-1, walls[1]] in wall_connect_list:
                        wall_connect_list.append([walls[0]-1, walls[1]])

                for walls in wall_connect_list:
                    wall_color[walls[1]][walls[0]] = colors[wall_cluster_num % len(colors)]
                    finish_wall.append(walls)
                
                wall_cluster_num += 1

    # ゴールの位置を決める
    for i in range(stage_h):

        for j in range(stage_w):

            if can_reach[(stage_h-1)-i][j] == max_reach:
                goal_y = (stage_h-1)-i
                goal_x = j

    # 最短ルートが指定の難易度よりも長ければ迷路テスト終了
    if can_reach[goal_y][goal_x] >= ((stage_w - 1) + (stage_h - 1)) * difficulty:
        test = False

    # 条件にあう迷路じゃない場合は迷路を作り直す
    else:
        test_num += 1
        print(((stage_w - 1) + (stage_h - 1)) * difficulty, "lost")

        if can_reach[goal_y][goal_x] >= 1:
            print(stage_w, stage_h, stage_w * stage_h, wall_num, max_reach, test_num)

    # test = False

# for i in range(stage_h):
#     for j in range(stage_w): 
#             print(wall_length[(stage_h-1)-i][j], end=",")
#     print("")

min_length = stage_w * stage_h

for i in range(stage_h):

    for j in range(stage_w):

        if wall_length[(stage_h-1)-i][j] < min_length and not wall_length[(stage_h-1)-i][j] == 0:
            min_length = wall_length[(stage_h-1)-i][j]

print(min_length)
print(can_reach[goal_y][goal_x], stage_w, stage_h)


# # 最短の道のりだけ表示したい場合の処理
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
    screen = pygame.display.set_mode(((stage_w + 2) * tile_size, (stage_h + 2) * tile_size))

    while True:

        # 背景
        screen.fill(bg_color)
        pygame.draw.rect(screen, out_wall_color, (0*tile_size, 0*tile_size, (stage_w+1)*tile_size, tile_size))
        pygame.draw.rect(screen, out_wall_color, ((stage_w+1)*tile_size, 0*tile_size, tile_size, (stage_h+1)*tile_size))
        pygame.draw.rect(screen, out_wall_color, (tile_size, (stage_h+1)*tile_size, (stage_w+1)*tile_size, tile_size))
        pygame.draw.rect(screen, out_wall_color, (0*tile_size, 1*tile_size, tile_size, (stage_h+1)*tile_size))

        for i in range(stage_h):

            for j in range(stage_w):

                if player_x == j and player_y == (stage_h-1)-i:
                    # 円
                    pygame.draw.circle(screen, player_color, ((j+1)*tile_size + tile_size/2, (i+1)*tile_size + tile_size/2), tile_size/2)

                elif goal_x == j and goal_y == (stage_h-1)-i:
                    pygame.draw.polygon(screen, goal_color, [[(j+1/2 +1)*tile_size, (i +1)*tile_size], [(j+1 +1)*tile_size, (i+1/2 +1)*tile_size], [(j+1/2 +1)*tile_size, (i+1 +1)*tile_size], [(j +1)*tile_size, (i+1/2 +1)*tile_size]])

                elif [j, (stage_h-1)-i] in wall_list:
                    # 長方形
                    pygame.draw.rect(screen, wall_color[(stage_h-1)-i][j], ((j+1)*tile_size, (i+1)*tile_size, tile_size, tile_size))
        # 描画
        pygame.display.update()

        # イベントを処理する --- (*5)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                pass

        #1push1処理
        if unique["up"] and not [player_x, player_y+1] in wall_list:
            player_y += 2
            stroke = True

        if unique["down"] and not [player_x, player_y-1] in wall_list:
            player_y -= 2
            stroke = True

        if unique["right"] and not [player_x+1, player_y] in wall_list:
            player_x += 2
            stroke = True

        if unique["left"] and not [player_x-1, player_y] in wall_list:
            player_x -= 2
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
            
        # print(can_reach[goal_y][goal_x], stage_w, stage_h)
        # stroke = False

        time.sleep(0.05)

        if player_x == goal_x and player_y == goal_y:
            is_goal = True
            break

if __name__ == '__main__':
    main()

# os.system('cls')

if is_goal:
    print("goal!!!!")
    time.sleep(3)

# os.system('cls')

# for i in range(stage_h):
#     for j in range(stage_w): 
#         if can_reach[(stage_h-1)-i][j] == 0:
#             print("0", end="")
#         else:
#             print("1", end="")
#     print("")

# for i in range(stage_h):
#     for j in range(stage_w): 
#             print(wall_length[(stage_h-1)-i][j], end="")
#     print("")

# print(wall_connect_list)

# os.system('cls')