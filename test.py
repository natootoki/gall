### インポート
import sys
import pygame
from pygame.locals import *

import random
 
### 定数
WIDE   = 800  # 画面横サイズ
HIGHT  = 600  # 画面縦サイズ
R_SIZE = 20   # 円半径
W_TIME = 10   # 待ち時間

square_size = 64

square_num_x = 8
square_num_y = 8

board_x = WIDE/2 - square_num_x * square_size/2
board_y = HIGHT/2 - square_num_y * square_size/2

# 色を定義
black = (0, 0, 0)
gray = (127, 127, 127)
white = (255, 255, 255)
# 赤橙黄緑青藍紫
colors = [(255, 0, 0), (255, 165, 0), (255, 241, 0), (0, 128, 0), (30, 144, 255), (15, 84, 116), (192, 48, 192)]

### 画面初期化
pygame.init()
surface = pygame.display.set_mode((WIDE, HIGHT))
 
### 変数初期化
x = WIDE/2    # 横座標
y = HIGHT/2   # 縦座標

target_square_num_x = max(0, min(int((x-board_x)//square_size), square_num_x-1))
target_square_num_y = max(0, min(int((y-board_y)//square_size), square_num_y-1))

black_list = [[3, 4], [4, 3]]
white_list = [[3, 3], [4, 4]]

turn = 0

black_skip = False
white_skip = False

black_player = False
white_player = False

### マウスカーソル表示
pygame.mouse.set_visible(True)
 
### マウスカーソル初期位置
pygame.mouse.set_pos((x, y))
 
### 無限ループ
while True:

    font = pygame.font.SysFont('arial', 60)

    # text = font.render("Hello World", True, (255,255,255), (0,255,0))
    text = font.render(str((target_square_num_x, target_square_num_y)), True, (255,255,255), None)

    ### 画面描画
    surface.fill((0,0,0))
    surface.blit(text, (0,0))

    # 石を置ける場所を洗い出す処理
    can_put_square = []

    for i in range(square_num_y):

        for j in range(square_num_x):

            # 石が置かれていないマスには石を置ける可能性がある
            if not [j, i] in black_list and not [j, i] in white_list:
                # 敵の石の隣には石を置ける可能性がある
                hoges = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
                is_my_stone = False

                # 敵の石の延長線上に、敵の石に接するように自分の石が置かれていれば石を置ける
                for hoge in hoges:
                    check_square_num = 1

                    if turn%2==0 and [j+hoge[0], i+hoge[1]] in white_list:
                        is_put_enemy = True

                        for k in range(2, max(square_num_x, square_num_y)):
                            check_square_num += 1

                            if [j+hoge[0]*check_square_num, i+hoge[1]*check_square_num] in white_list:
                                pass

                            elif [j+hoge[0]*check_square_num, i+hoge[1]*check_square_num] in black_list:
                                is_my_stone = True
                                break

                            else:
                                break
                    
                    if turn%2==1 and [j+hoge[0], i+hoge[1]] in black_list:

                        for k in range(2, max(square_num_x, square_num_y)):
                            check_square_num += 1

                            if [j+hoge[0]*check_square_num, i+hoge[1]*check_square_num] in black_list:
                                pass

                            elif [j+hoge[0]*check_square_num, i+hoge[1]*check_square_num] in white_list:
                                is_my_stone = True
                                break

                            else:
                                break

                if is_my_stone:    
                    can_put_square.append([j, i])

    if (not black_player and turn%2==0) or (not white_player and turn%2==1):
        if len(can_put_square)>0:
            npc_put = random.randrange(len(can_put_square))

            # 先手なら黒を置く
            if turn%2==0:
                black_list.append([can_put_square[npc_put][0], can_put_square[npc_put][1]])
                print(str(turn), "black", str([can_put_square[npc_put][0], can_put_square[npc_put][1]]))

            # 後手なら白を置く
            elif turn%2==1:
                white_list.append([can_put_square[npc_put][0], can_put_square[npc_put][1]])
                print(str(turn), "white", str([can_put_square[npc_put][0], can_put_square[npc_put][1]]))

            # 石をひっくり返す処理
            hoges = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
            is_my_stone = False
            reverse_stone = []

            # 敵の石の延長線上に、敵の石に接するように自分の石が置かれていればひっくり返る
            for hoge in hoges:
                check_square_num = 1
                reverse_stone_cantidate = []

                if turn%2==0 and [black_list[-1][0]+hoge[0], black_list[-1][1]+hoge[1]] in white_list:
                    reverse_stone_cantidate.append([black_list[-1][0]+hoge[0], black_list[-1][1]+hoge[1]])

                    for k in range(2, max(square_num_x, square_num_y)):
                        check_square_num += 1

                        if [black_list[-1][0]+hoge[0]*check_square_num, black_list[-1][1]+hoge[1]*check_square_num] in white_list:
                            reverse_stone_cantidate.append([black_list[-1][0]+hoge[0]*check_square_num, black_list[-1][1]+hoge[1]*check_square_num])

                        elif [black_list[-1][0]+hoge[0]*check_square_num, black_list[-1][1]+hoge[1]*check_square_num] in black_list:

                            for cand in reverse_stone_cantidate:
                                reverse_stone.append(cand)

                            reverse_stone_cantidate = []
                            break

                        else:
                            reverse_stone_cantidate = []
                            break
                
                if turn%2==1 and [white_list[-1][0]+hoge[0], white_list[-1][1]+hoge[1]] in black_list:
                    reverse_stone_cantidate.append([white_list[-1][0]+hoge[0], white_list[-1][1]+hoge[1]])

                    for k in range(2, max(square_num_x, square_num_y)):
                        check_square_num += 1

                        if [white_list[-1][0]+hoge[0]*check_square_num, white_list[-1][1]+hoge[1]*check_square_num] in black_list:
                            reverse_stone_cantidate.append([white_list[-1][0]+hoge[0]*check_square_num, white_list[-1][1]+hoge[1]*check_square_num])

                        elif [white_list[-1][0]+hoge[0]*check_square_num, white_list[-1][1]+hoge[1]*check_square_num] in white_list:

                            for cand in reverse_stone_cantidate:
                                reverse_stone.append(cand)

                            reverse_stone_cantidate = []
                            break
                            
                        else:
                            reverse_stone_cantidate = []
                            break
            
            for rev in reverse_stone:
                if turn%2==0:
                    white_list.remove(rev)
                    black_list.append(rev)
                if turn%2==1:
                    black_list.remove(rev)
                    white_list.append(rev)
            reverse_stone = []

            if turn%2==0:
                black_skip = False
            else:
                white_skip = False

            turn += 1

    # 打つ手が無い時のスキップ処理
    if len(can_put_square) == 0:

        if not black_skip or not white_skip:

            if turn%2==0:
                print(str(turn), "black skip")
                black_skip = True
                if black_skip and white_skip:
                    print("black ", str(len(black_list)))
                    print("white ", str(len(white_list))) 

            else:
                print(str(turn), "white skip")
                white_skip = True
                if black_skip and white_skip:
                    print("black ", str(len(black_list)))
                    print("white ", str(len(white_list))) 

            turn += 1

    # 長方形（盤面）
    pygame.draw.rect(surface, colors[0], (board_x, board_y, square_num_x*square_size, square_num_y*square_size))

    for cans in can_put_square:
        # 長方形（石を置けるマス）
        pygame.draw.rect(surface, colors[1], (board_x + cans[0]*square_size, board_y + cans[1]*square_size, square_size, square_size))

    for i in range(1, square_num_x):
        # 線（マス区切り線：縦）
        pygame.draw.line(surface, black, (board_x + square_size*i, board_y), (board_x + square_size*i, board_y + square_num_y*square_size), 3)

    for i in range(1, square_num_y):
        # 線（マス区切り線：横）
        pygame.draw.line(surface, black, (board_x, board_y + square_size*i), (board_x + square_num_x*square_size, board_y + square_size*i), 3)

    for bla in black_list:
        # 円（黒の石）
        pygame.draw.circle(surface, black, (board_x + (bla[0]+1/2)*square_size, board_y + (bla[1]+1/2)*square_size), R_SIZE, 0)
    
    for whi in white_list:
        # 円（白の石）
        pygame.draw.circle(surface, black, (board_x + (whi[0]+1/2)*square_size, board_y + (whi[1]+1/2)*square_size), R_SIZE, 3)

    pygame.display.update()
    pygame.time.wait(W_TIME)
 
    ### イベント取得
    for event in pygame.event.get():
 
        ### マウスイベント
        if event.type == MOUSEMOTION:
            ### マウス位置取得
            x,y = event.pos
            target_square_num_x = max(0, min(int((x-board_x)//square_size), square_num_x-1))
            target_square_num_y = max(0, min(int((y-board_y)//square_size), square_num_y-1))

        # クリックされたら
        if event.type == MOUSEBUTTONDOWN:

            if [target_square_num_x, target_square_num_y] in can_put_square:

                # 先手なら黒を置く
                if turn%2==0:
                    black_list.append([target_square_num_x, target_square_num_y])
                    print(str(turn), "black", str([target_square_num_x, target_square_num_y]))

                # 後手なら白を置く
                elif turn%2==1:
                    white_list.append([target_square_num_x, target_square_num_y])
                    print(str(turn), "white", str([target_square_num_x, target_square_num_y]))

                # 石をひっくり返す処理
                hoges = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
                is_my_stone = False
                reverse_stone = []

                # 敵の石の延長線上に、敵の石に接するように自分の石が置かれていればひっくり返る
                for hoge in hoges:
                    check_square_num = 1
                    reverse_stone_cantidate = []

                    if turn%2==0 and [target_square_num_x+hoge[0], target_square_num_y+hoge[1]] in white_list:
                        reverse_stone_cantidate.append([target_square_num_x+hoge[0], target_square_num_y+hoge[1]])

                        for k in range(2, max(square_num_x, square_num_y)):
                            check_square_num += 1

                            if [target_square_num_x+hoge[0]*check_square_num, target_square_num_y+hoge[1]*check_square_num] in white_list:
                                reverse_stone_cantidate.append([target_square_num_x+hoge[0]*check_square_num, target_square_num_y+hoge[1]*check_square_num])

                            elif [target_square_num_x+hoge[0]*check_square_num, target_square_num_y+hoge[1]*check_square_num] in black_list:

                                for cand in reverse_stone_cantidate:
                                    reverse_stone.append(cand)

                                reverse_stone_cantidate = []
                                break

                            else:
                                reverse_stone_cantidate = []
                                break
                    
                    if turn%2==1 and [target_square_num_x+hoge[0], target_square_num_y+hoge[1]] in black_list:
                        reverse_stone_cantidate.append([target_square_num_x+hoge[0], target_square_num_y+hoge[1]])

                        for k in range(2, max(square_num_x, square_num_y)):
                            check_square_num += 1

                            if [target_square_num_x+hoge[0]*check_square_num, target_square_num_y+hoge[1]*check_square_num] in black_list:
                                reverse_stone_cantidate.append([target_square_num_x+hoge[0]*check_square_num, target_square_num_y+hoge[1]*check_square_num])

                            elif [target_square_num_x+hoge[0]*check_square_num, target_square_num_y+hoge[1]*check_square_num] in white_list:

                                for cand in reverse_stone_cantidate:
                                    reverse_stone.append(cand)

                                reverse_stone_cantidate = []
                                break
                                
                            else:
                                reverse_stone_cantidate = []
                                break
                
                for rev in reverse_stone:
                    if turn%2==0:
                        white_list.remove(rev)
                        black_list.append(rev)
                    if turn%2==1:
                        black_list.remove(rev)
                        white_list.append(rev)
                reverse_stone = []

                if turn%2==0:
                    black_skip = False
                else:
                    white_skip = False
                turn += 1

        # キーが押されたら
        if event.type == KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == K_a:
                black_list = [[3, 4], [4, 3]]
                white_list = [[3, 3], [4, 4]]

                turn = 0

                black_skip = False
                white_skip = False
            if event.key == K_1:
                black_player = not black_player
            if event.key == K_2:
                white_player = not white_player
 
        ### 終了処理
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
