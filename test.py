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

loop = True

bg_color = black
out_wall_color = gray

# 壁のブロックごとに色を変えるかどうか
color_change = 0

# ステージの大きさ
wh = 16 * 2 - 1

stage_min_w = wh
stage_max_w = wh*2
stage_min_h = wh
stage_max_h = wh*2

# ひとマスの大きさ
tile_size = 15

stage_w = random.randrange(stage_min_w, stage_max_w+1, 2) #小さすぎると壁が少なすぎる
stage_h = random.randrange(stage_min_h, stage_max_h+1, 2) #小さすぎると壁が少なすぎる

player_color = white

player_x = 0
player_y = 0

goal_color = colors[2]

goal_x = stage_w-1
goal_y = stage_h-1

is_goal = False

# 壁の最短の長さ
wall_min_length = 17

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
                        hoges = [[walls[0], walls[1]+1], [walls[0], walls[1]-1], [walls[0]+1, walls[1]], [walls[0]-1, walls[1]]]

                        for hoge in hoges:    

                            if hoge in wall_list and not hoge in wall_connect_list:
                                wall_connect_list.append(hoge)

                    for walls in wall_connect_list:
                        wall_length[walls[1]][walls[0]] = len(wall_connect_list)

                    if len(wall_connect_list) < wall_min_length:
                        change = True
                        count = 0

                        for walls in wall_connect_list:

                            if walls[0]%2==1 and walls[1]%2==1:
                                hoges = [[walls[0], walls[1]+1], [walls[0], walls[1]-1], [walls[0]+1, walls[1]], [walls[0]-1, walls[1]]]

                                for hoge in hoges:

                                    if not hoge in wall_list and not hoge in wall_ng_list and not hoge in wall_candidate:

                                        if 0 < hoge[0] and hoge[0] < stage_w-1 and 0 < hoge[1] and hoge[1] < stage_h-1:
                                            wall_candidate.append(hoge)
                                    
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
                                hoges = [[reaches[0], reaches[1]+1], [reaches[0], reaches[1]-1], [reaches[0]+1, reaches[1]], [reaches[0]-1, reaches[1]]]

                                for hoge in hoges:
                                                
                                    if not hoge in wall_list and not hoge in can_reach:

                                        if 0 <= hoge[0] and hoge[0] <= stage_w-1 and 0 <= hoge[1] and hoge[1] <= stage_h-1:
                                            can_reach.append(hoge)

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
                                
                                del wall_list[-1]

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
                        hoges = []
                        hoges.append([not walls[1] == stage_h-1, [walls[0], walls[1]+1]])
                        hoges.append([not walls[1] == 0, [walls[0], walls[1]-1]])
                        hoges.append([not walls[0] == stage_w-1, [walls[0]+1, walls[1]]])
                        hoges.append([not walls[0] == 0, [walls[0]-1, walls[1]]])

                        for hoge in hoges:
                        
                            # 端じゃない場合処理をする
                            if not hoge[1][1] == stage_h-1:

                                # 対象のマスが壁でない、かつ、到達できると分かっていない場合、自分のマス+1の番号を振る
                                if hoge[1] in wall_list and not hoge[1] in wall_connect_list:
                                    wall_connect_list.append(hoge[1])
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
                            hoges = []
                            hoges.append([wall_facing_list[inner_rand][0]==1, [wall_facing_list[inner_rand][0]-1, wall_facing_list[inner_rand][1]]])
                            hoges.append([wall_facing_list[inner_rand][0]==stage_w-2, [wall_facing_list[inner_rand][0]+1, wall_facing_list[inner_rand][1]]])
                            hoges.append([wall_facing_list[inner_rand][1]==1, [wall_facing_list[inner_rand][0], wall_facing_list[inner_rand][1]-1]])
                            hoges.append([wall_facing_list[inner_rand][1]==stage_h-2, [wall_facing_list[inner_rand][0], wall_facing_list[inner_rand][1]+1]])
                            br = False

                            for hoge in hoges:

                                if hoge[0]:
                                    wall_list.append(hoge[1])
                                    wall_connect_list.append(hoge[1])
                                    br = True
                                    break
                            
                            if br:
                                break
                    
                    for walls in wall_connect_list:
                        wall_length[walls[1]][walls[0]] = len(wall_connect_list)
                        finish_wall.append(walls)

    print("root_test")

    can_reach = [[player_x, player_y]]
    cant_reach = []

    for cans in can_reach:
        hoges = [[cans[0], cans[1]+1], [cans[0], cans[1]-1], [cans[0]+1, cans[1]], [cans[0]-1, cans[1]]]

        for hoge in hoges:

            if not hoge in can_reach and 0 <= hoge[0] and hoge[0] <= stage_w-1 and 0 <= hoge[1] and hoge[1] <= stage_h-1:

                if not hoge in wall_list:
                    can_reach.append(hoge)

    # 壁に色をつける
    print("coloring")
    finish_wall = []

    for i in range(stage_h):

        for j in range(stage_w):
            inner_x = j
            inner_y = (stage_h-1)-i

            if inner_x%2 == 1 and inner_y%2 == 1 and not [inner_x, inner_y] in finish_wall:
                wall_connect_list = [[inner_x, inner_y]]

                for walls in wall_connect_list:
                    hoges = [[walls[0], walls[1]+1], [walls[0], walls[1]-1], [walls[0]+1, walls[1]], [walls[0]-1, walls[1]]]

                    for hoge in hoges:

                        if hoge in wall_list and not hoge in wall_connect_list:
                            wall_connect_list.append(hoge)

                for walls in wall_connect_list:
                    wall_color[walls[1]][walls[0]] = colors[wall_cluster_num % len(colors)]
                    finish_wall.append(walls)
                
                wall_cluster_num += color_change

    # ゴールの位置を決める
    print("put goal")
    goal_x = can_reach[-1][0]
    goal_y = can_reach[-1][1]
    print(goal_x, goal_y)

    test = False

min_length = stage_w * stage_h

for i in range(stage_h):

    for j in range(stage_w):

        if wall_length[(stage_h-1)-i][j] < min_length and not wall_length[(stage_h-1)-i][j] == 0:
            min_length = wall_length[(stage_h-1)-i][j]

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
        hoges = ["up", "down", "right", "left"]

        for hoge in hoges:

            if "{0}".format(key) == "Key." + hoge:

                if not button[hoge]:
                    unique[hoge] = True

                button[hoge] = True

def release(key):
    global player_x
    global player_y
    global button
    global unique

    try:
        #print('アルファベット {0} が押されました'.format(key.char))
        if "{0}".format(key.char) == "a":
            button["a"] = False

    except AttributeError:
        hoges = ["up", "down", "right", "left"]

        for hoge in hoges:

            if "{0}".format(key) == "Key." + hoge:
                button[hoge] = False

listener = keyboard.Listener(
    on_press=press,
    on_release=release)
listener.start()

################################処理################################

def main():
    # global player_x, player_y, is_goal, stage_w, stage_h, tile_size, wall_list

    pygame.init()
    pygame.display.set_caption("maze")
    screen = pygame.display.set_mode((800, 600))

    while True:

        # 背景
        screen.fill(bg_color)

        # # 長方形
        # pygame.draw.rect(screen, wall_color[(stage_h-1)-i][j], ((j+1)*tile_size, (i+1)*tile_size, tile_size, tile_size))

        # # 多角形
        # pygame.draw.polygon(screen, goal_color, [[(goal_x+1/2 +1)*tile_size, ((stage_h-1-goal_y) +1)*tile_size], [(goal_x+1 +1)*tile_size, ((stage_h-1-goal_y)+1/2 +1)*tile_size], [(goal_x+1/2 +1)*tile_size, ((stage_h-1-goal_y)+1 +1)*tile_size], [(goal_x +1)*tile_size, ((stage_h-1-goal_y)+1/2 +1)*tile_size]])

        # # 円
        # pygame.draw.circle(screen, player_color, ((player_x+1)*tile_size + tile_size/2, ((stage_h-1-player_y)+1)*tile_size + tile_size/2), tile_size/2)

        # 描画
        pygame.display.update()

        # イベントを処理する --- (*5)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                pass

        # #1push1処理
        # hoges = []
        # hoges.append(["up", not [player_x, player_y+1] in wall_list, 0, 2])
        # hoges.append(["down", not [player_x, player_y-1] in wall_list, 0, -2])
        # hoges.append(["right", not [player_x+1, player_y] in wall_list, 2, 0])
        # hoges.append(["left", not [player_x-1, player_y]in wall_list, -2, 0])

        # for hoge in hoges:

        #     if unique[hoge[0]] and hoge[1]:
        #         player_x += hoge[2]
        #         player_y += hoge[3]
                
        #         if player_x < 0 or stage_w-1 < player_x or player_y < 0 or stage_h-1 < player_y:
        #             player_x -= hoge[2]
        #             player_y -= hoge[3]

        if unique["q"]:
            break

        for uni in unique.keys():
            unique[uni] = False

        # time.sleep(0.1)

        # if player_x == goal_x and player_y == goal_y:
        #     is_goal = True
        #     break

if __name__ == '__main__':
    main()

if is_goal:
    print("goal!!!!")
    time.sleep(3)
