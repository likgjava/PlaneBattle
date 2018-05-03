import random
import sys
import time

import pygame
from pygame.locals import *

# 窗口宽度
WINDOW_WIDTH = 300  # 512
# 窗口高度
WINDOW_HEIGHT = 450  # 768
# 敌人飞机数量
ENEMY_PLANE_COUNT = 3
# 敌人飞机
enemy_planes = []
# 得分
score = 0


class UIElement:
    """界面元素"""

    window = None  # 窗口对象

    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)
        self.x = x
        self.y = y

    def display(self):
        self.window.blit(self.img, (self.x, self.y))


class Map(UIElement):
    """地图"""

    pass


class Plane(UIElement):
    """飞机"""

    pass


class HeroPlane(Plane):
    """英雄飞机"""

    def __init__(self, img_path, x, y):
        super().__init__(img_path, x, y)
        self.bullets = []

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def display_bullets(self):
        """显示子弹"""
        deleted_bullets = []
        for bullet in self.bullets:
            # 飞出窗口
            if bullet.y < -31:
                deleted_bullets.append(bullet)
            else:
                # 判断是否击中敌机
                for enemy_plane in enemy_planes:
                    is_hit = bullet.is_hit_plane(enemy_plane)
                    if is_hit:
                        global score
                        score += 1
                        deleted_bullets.append(bullet)
                        enemy_plane.y = WINDOW_HEIGHT + 1
                        break
                    else:
                        bullet.display()
                        bullet.move()

        for del_bullet in deleted_bullets:
            self.bullets.remove(del_bullet)

    def fire(self):
        bullet = Bullet("res/bullet_1.png", self.x + 60 - 10, self.y - 30)
        self.bullets.append(bullet)


class EnemyPlane(Plane):
    """敌人飞机"""

    def move(self):
        self.y += 5
        if self.y > WINDOW_HEIGHT:
            self.x = random.randint(0, WINDOW_WIDTH - 100)
            self.y = random.randint(-150, -31)
            self.img = pygame.image.load("res/img-plane_%d.png" % random.randint(1, 7))


class Bullet(UIElement):
    """子弹"""

    def move(self):
        self.y -= 5

    def is_hit_plane(self, enemy_plane):
        """判断是否击中了敌机"""
        bullet_rect = Rect(self.x, self.y, 20, 31)
        enemy_rect = Rect(enemy_plane.x, enemy_plane.y, 100, 68)
        # 判断两个矩形是否相交，相交返回True, 否则返回False
        return pygame.Rect.colliderect(bullet_rect, enemy_rect)


def main():
    # 初始化pygame库，让计算机硬件准备
    pygame.init()

    # 创建窗口
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    UIElement.window = window

    # 创建地图
    map = Map("res/img_bg_level_1.jpg", 0, 0)

    # 英雄飞机
    hero_plane = HeroPlane("res/hero2.png", 100, 300)

    # 敌人飞机
    for _ in range(ENEMY_PLANE_COUNT):
        enemy_plane = EnemyPlane("res/img-plane_%d.png" % random.randint(1, 7), random.randint(0, WINDOW_WIDTH - 100),
                                 random.randint(-150, -31))
        enemy_planes.append(enemy_plane)

    # 加载自定义字体，返回字体对象
    font_obj = pygame.font.Font("res/SIMHEI.TTF", 30)

    while True:
        # 显示地图
        map.display()

        # 显示英雄飞机
        hero_plane.display()

        # 显示子弹
        hero_plane.display_bullets()

        # 显示敌人飞机
        for enemy_plane in enemy_planes:
            enemy_plane.move()
            enemy_plane.display()

        # 显示得分
        text_obj = font_obj.render("得分：%d" % score, 1, (255, 255, 255))
        window.blit(text_obj, (10, 10))

        # 刷新窗口
        pygame.display.update()

        # 获取新事件
        for event in pygame.event.get():
            # 1. 鼠标点击关闭窗口事件
            if event.type == QUIT:
                print("点击关闭窗口按钮")
                sys.exit()  # 关闭程序

            # 2. 键盘按下事件
            if event.type == KEYDOWN:
                # 判断用户按键
                if event.key == K_SPACE:
                    hero_plane.fire()

        # 获取键盘的长按事件
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a] or pressed_keys[K_LEFT]:
            hero_plane.move_left()
        if pressed_keys[K_d] or pressed_keys[K_RIGHT]:
            hero_plane.move_right()

        time.sleep(0.02)


if __name__ == '__main__':
    main()
