import pygame
from pygame.locals import *
import sys, random

# 変数の初期化
maze_w = 31 # 迷路の列数
maze_h = 23 # 迷路の行数
maze = [] # 迷路データ
tile_w = 16
px = 1 # プレイヤーの座標
py = 1

# 色を定義
black = (0, 0, 0)
red = (255, 0, 0)

def main():
    # ゲームの初期化処理
    global px, py
    pygame.init()
    pygame.display.set_caption("maze game")
    screen = pygame.display.set_mode((tile_w*maze_w,tile_w*maze_h))

    # ゲームのメインループ --- (*3)
    while True:
        # 背景
        screen.fill(black)
        # 長方形
        pygame.draw.rect(screen, red, (0, 0, 32, 32))
        # 円
        pygame.draw.circle(screen, red, (32, 32), 16)
        # 描画
        pygame.display.update()
        # イベントを処理する --- (*5)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                print("hello!")
if __name__ == '__main__':
    main()
