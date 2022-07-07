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

SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 50
ARRAY_WIDTH = SCREEN_WIDTH//BLOCK_WIDTH #30
ARRAY_HEIGHT = SCREEN_HEIGHT//BLOCK_HEIGHT  #20
obstacles_pos = [(2,2), (3,3), (4,4), (5,5), (10,10)] ##coordinates of obstacles
charge_pos = [(3,5), (6,4)]    ##cordinates of charging stations
##if implementing array
use_array = True  ##set to false to use list of obstacle and charging point coordinates instead
array_map = [[0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [2,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]  ##2 for charging_station, 1 for obstacles
START = (1,1)
DEST = (29,19)
LIVES = 3
hit = False 
hit_interval = 750 ##minimum time between rock collisions
enemy_interval = 1000 ##minimum time between new enemies spawning


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
                random.randint(SCREEN_WIDTH + 5, SCREEN_WIDTH + 20),
                random.randint(0, 29) * BLOCK_HEIGHT, ##reduces enemy overlap
            )
        )
        self.speed = random.randint(1,3)
        
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
        

class Charge(pygame.sprite.Sprite):
    def __init__(self):
        super(Charge, self).__init__()
        self.surf = pygame.image.load("charging_station.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)

        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("fishy.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (START[1] * BLOCK_WIDTH + BLOCK_WIDTH/2, START[0] * BLOCK_HEIGHT + BLOCK_HEIGHT/2)
            )
        self.speed = 5
        self.distance_travelled = 0
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
            self.distance_travelled += 1
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
            self.distance_travelled += 1
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            self.surf = pygame.image.load("fishy_2.png").convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.distance_travelled += 1
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            self.surf = pygame.image.load("fishy.png").convert()
            self.surf.set_colorkey((0,0,0), RLEACCEL)
            self.distance_travelled += 1
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

def draw_grid():
    global use_array, array
    if use_array == False:
        temp_width = 0
        temp_height = 0
        for i in range(0, SCREEN_WIDTH, BLOCK_WIDTH):
            for j in range (0, SCREEN_HEIGHT, BLOCK_HEIGHT):
                if((temp_width, temp_height) in obstacles_pos):
                    new_obstacle = Obstacle()
                    new_obstacle.rect = new_obstacle.surf.get_rect(
                        center = (
                            temp_width * BLOCK_WIDTH + BLOCK_WIDTH/2,
                            temp_height * BLOCK_HEIGHT + BLOCK_HEIGHT/2,
                            )
                    )
                    obstacles.add(new_obstacle)
                    all_sprites.add(new_obstacle)
                elif((temp_width, temp_height) in charge_pos):
                    new_charge = Charge()
                    new_charge.rect = new_charge.surf.get_rect(
                        center = (
                            temp_width * BLOCK_WIDTH + BLOCK_WIDTH/2,
                            temp_height * BLOCK_HEIGHT + BLOCK_HEIGHT/2,
                            )
                    )
                    charging_stations.add(new_charge)
                    all_sprites.add(new_charge)
                temp_width += 1
            temp_height += 1
            temp_width = 0
    else:
        for i in range(ARRAY_HEIGHT):
            for j in range (ARRAY_WIDTH):
                if (array_map[i][j] == 1):
                    new_obstacle = Obstacle()
                    new_obstacle.rect = new_obstacle.surf.get_rect(
                        center = (
                            i * BLOCK_HEIGHT + BLOCK_HEIGHT/2,
                            j * BLOCK_WIDTH + BLOCK_WIDTH/2,  ##possibly wrong might need to switch
                            )
                    )
                    obstacles.add(new_obstacle)
                    all_sprites.add(new_obstacle)
                elif (array_map[i][j] == 2):
                    new_charge = Charge()
                    new_charge.rect = new_charge.surf.get_rect(
                        center = (
                            i * BLOCK_HEIGHT + BLOCK_HEIGHT/2,
                            j * BLOCK_WIDTH + BLOCK_WIDTH/2,
                            )
                    )
                    charging_stations.add(new_charge)
                    all_sprites.add(new_charge)
                        

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
bg = pygame.image.load("bg.png")
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, enemy_interval) ##add new enemy every 1000 milliseconds
checkrock = pygame.USEREVENT + 2
pygame.time.set_timer(checkrock, hit_interval)


player = Player()

enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
charging_stations = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
    
draw_grid()    
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
    if pygame.sprite.spritecollideany(player,charging_stations): #recharge
        player.distance_travelled = 0
        
    ##check proximity
    ##for enemy in enemies:
       ## if math.dist(player.rect.center, enemy.rect.center) <= 100:
            ##running = False
            
    ##maximum number of moves player can make before running out of fuel         
    if player.distance_travelled >= 500:
        player.kill()
        running = False
        
    if LIVES == 0:
        player.kill()
        running = False
        
    pygame.display.flip()

pygame.quit()
