import pygame
import os

from array_map import *
from submission import shortest_path
pygame.font.init()

# ~~~
# VARIABLES
# ~~~

# technical
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fish Swimming Across Harbour")
FPS = 10        # smaller = slower

#main variable
fish_x = START_X
fish_y = START_Y

# aesthetics
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (200,0,0)
BLUE = (0,0,200)
OCEAN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.jpg')), (WINDOW_WIDTH, WINDOW_HEIGHT))
FISH_IMAGE = pygame.image.load(
    os.path.join('Assets', 'fish.png'))

# draw function
blockSize = 30          #Set the size of the grid block
    # size of the map
map_width = blockSize*ARRAY_WIDTH;  
map_height = blockSize*ARRAY_HEIGHT;
    # positioning the map at the center of the screen
middle_height = (WINDOW_HEIGHT-map_height)//2
middle_width = (WINDOW_WIDTH-map_width)//2
    # Fish image in grid
FISH = pygame.transform.scale(FISH_IMAGE, (blockSize, blockSize))

# ~~~
# FUNCTIONS
# ~~~
def main():
    pygame.init()
    global fish_x, fish_y
    CLOCK = pygame.time.Clock()

    # game loop
    run = True
    notArrived = True

    
    path = shortest_path(ARRAY, (START_X, START_Y), obstacles, (DEST_X, DEST_Y))
    count = 0
    print(path)
    
    while (run):
        # print(fish_x,fish_y);      #DEBUG
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if (notArrived):        # if fish is still moving
            # Position Updates from path
            fish_x = path[count][0]
            fish_y = path[count][1]
            
            drawGrid()
            count+=1
            
            # Checking win condition
            if (DEST_X == fish_x and DEST_Y == fish_y):
                # print("Arrived at destination");    #DEBUG
                notArrived = False

def drawGrid():
    global fish_x, fish_y
    SCREEN.blit(OCEAN, (0,0))       # Refresh the Screen
    # will record the relative position
    temp_width = 0
    temp_height = 0
    # x and y are absolute positions on the screen
    # as we want to draw the map in the middle
    for x in range(middle_width, middle_width + map_width, blockSize):
        for y in range(middle_height, middle_height + map_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            if ((temp_width,temp_height)in obstacles):              # obstacle
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
            elif (temp_width == fish_x and temp_height == fish_y):  # fish
                SCREEN.blit(FISH, (x,y))
            elif (temp_width == DEST_X and temp_height == DEST_Y):  # destination
                pygame.draw.rect(SCREEN, RED, rect, 0)
            else:                                                   # free space
                pygame.draw.rect(SCREEN, WHITE, rect, 1)
            temp_width+=1
        temp_height+=1
        temp_width = 0
    pygame.display.update()

if __name__ == "__main__":
    main()
