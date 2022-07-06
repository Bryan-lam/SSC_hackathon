import pygame
import random
import math

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    )

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 900
LIVES = 3
hit = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        type = random.randint(0,1)
        if type == 0:
            self.surf = pygame.image.load("clam_1.png").convert()
        elif type == 1:
            self.surf = pygame.image.load("clam_2.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1,1)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        type = random.randint(0,3)
        if type == 0:
            self.surf = pygame.image.load("rock_1.png").convert()
        elif type == 1:
            self.surf = pygame.image.load("rock_2.png").convert()
        elif type == 2:
            self.surf = pygame.image.load("rock_3.png").convert()
        else:
            self.surf = pygame.image.load("rock_4.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(100, SCREEN_WIDTH),
                random.randint(70,SCREEN_HEIGHT),
            )
        )
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("fishy.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.surf = pygame.image.load("fishy_2.png").convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.surf = pygame.image.load("fishy.png").convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
bg = pygame.image.load("bg.png")
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000) ##add new enemy every 250 milliseconds
checkrock = pygame.USEREVENT + 2
pygame.time.set_timer(checkrock, 1000)

player = Player()

enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


for i in range(6):
    new_obstacle = Obstacle()
    obstacles.add(new_obstacle)
    all_sprites.add(new_obstacle)
    
all_sprites.add(player) 

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        elif event.type == checkrock:
            hit = False
                

    pressed_keys = pygame.key.get_pressed()
    
    player.update(pressed_keys)
    enemies.update()

    screen.blit(bg, (0,0))
    ##display all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    ##check for collisions
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running = False
    if pygame.sprite.spritecollideany(player,obstacles):
        if hit == False:
            LIVES = LIVES - 1
            hit = True
    ##check proximity
    for enemy in enemies:
        if math.dist(player.rect.center, enemy.rect.center) <= 100:
            running = False
    if LIVES == 0:
        player.kill()
        running = False
        
    pygame.display.flip()

pygame.quit()
