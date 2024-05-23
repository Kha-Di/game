import pygame
import sys
import random
pygame.init()

WIDTH, HEIGHT = 1000, 800

class Wall:
    def __init__(self, x, y, w, h, img):
        self.rect = pygame.Rect(x, y, w, h)
        self.orig_img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.orig_img, (w, h)) 

    def draw(self):
        screen.blit(self.img, self.rect)

class Player:
    def __init__(self, x, y, w, h, img_path, walls):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img_path), (w, h))
        self.x_speed = 0
        self.y_speed = 0
        self.walls = walls

    def collide(self, obj):
        return self.rect.colliderect(obj.rect)

    def move(self):
        self.rect.x += self.x_speed
        for wall in self.walls:
            if self.collide(wall):
                self.rect.x -= self.x_speed


        self.rect.y += self.y_speed
        for wall in self.walls:
            if self.collide(wall):
                self.rect.y -= self.y_speed

    def draw(self):
        screen.blit(self.img, (self.rect.x, self.rect.y))

class Enemy:
    def __init__(self, x, y, w, h, img, speed, p1, p2, orient):
        self.rect = pygame.Rect(x, y, w, h)
        self.img = pygame.transform.scale(pygame.image.load(img), (w, h))
        self.speed = speed
        self.orient = orient
        self.p1 = p1
        self.p2 = p2

    def move(self):
        if self.orient == 'h':
            self.rect.x += self.speed
            if self.rect.x >= self.p2 or self.rect.x <= self.p1:
                self.speed *= -1

        else:
            self.rect.y += self.speed
            if self.rect.y >= self.p2 or self.rect.y <= self.p1:
                self.speed *= -1

    def draw(self):
        screen.blit(self.img, self.rect)
    
    def destroy(self):
        self.rect.x = 1000
        self.rect.y = 1000
        self.speed = 0

walls = []
lvl1 = []
lvl2 = []
lvl3 = []
with open('lvl1.txt', 'r') as map:
    row, col = 0,0
    for line in map.read().split('\n'):
        x = list(line)
        col = 0
        for i in x:
            if i == '1':
                lvl1.append(Wall(col * 25, row * 25, 25, 25, 'wall.jpg'))
            col += 1
        row += 1
with open ('lvl2.txt', 'r') as map:
    row, col = 0, 0
    for line in map.read().split('\n'):
        x = list(line)
        col = 0
        for i in x:
            if i == 1:
                lvl2.append(Wall(col * 25, row * 25, 25, 25, 'wall.jpg'))
            col += 1
        row += 1
# with open ('lvl3.txt', 'r') as map:
#     row, col = 0, 0
#     for line in map.read().split('\n'):
#         x = list(line)
#         col = 0
#         for i in x:
#             if i == 1:
#                 lvl3.append(Wall(col * 25, row * 25, 25, 25, 'wall.jpg'))
player = Player(20, 20, 50, 50, 'персонаж.jpg', lvl1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
gameState = 0

while True:
    screen.fill((255, 255, 255))
    if gameState == 0:
        walls = lvl1
        player.walls = walls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.x_speed = -5
                elif event.key == pygame.K_d:
                    player.x_speed = 5
                elif event.key == pygame.K_w:
                    player.y_speed = -5
                elif event.key == pygame.K_s:
                    player.y_speed = 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.x_speed = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player.y_speed = 0
                
        player.move()
        player.draw()
        for wall in lvl1:
            wall.draw()

        # if player.rect.x >=500:
        #     gameState = 1
        #     player.rect.x = 30
        #     player.rect.y = 30

    pygame.display.update()
    clock.tick(60)