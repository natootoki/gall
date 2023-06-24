### インポート
import sys
import pygame
from pygame.locals import *
 
### 定数
WIDE   = 640  # 画面横サイズ
HIGHT  = 400  # 画面縦サイズ
R_SIZE = 10   # 円半径
W_TIME = 10   # 待ち時間

square_size = 32

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
    # pygame.draw.circle(surface, (255,255,255), (x,y), R_SIZE, 0)
    # 長方形
    pygame.draw.rect(surface, colors[0], (board_x, board_y, square_num_x*square_size, square_num_y*square_size))
    for i in range(1, square_num_x):
        # 線
        pygame.draw.line(surface, black, (board_x + square_size*i, board_y), (board_x + square_size*i, board_y + square_num_y*square_size), 3)

    for i in range(1, square_num_y):
        # 線
        pygame.draw.line(surface, black, (board_x, board_y + square_size*i), (board_x + square_num_x*square_size, board_y + square_size*i), 3)
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
            print(x, y)
 
        ### 終了処理
        if event.type == QUIT:
            pygame.quit()
            sys.exit()