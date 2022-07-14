import pygame
import os
pygame.font.init()

from array_map import *
from submission import shortest_path

# ~~~
# VARIABLES
# ~~~

# technical
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fish Swimming Across Harbour")
FPS = 10                                        # smaller = slower

#main variable
fish_x = START_X
fish_y = START_Y
stepCount = 0

# aesthetics
BLACK = (0, 0, 0)
GREY = (100,100,100)
LIGHTGREY = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (200,0,0)
ORANGE = (200,100,0)
OCEAN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.jpg')), (WINDOW_WIDTH, WINDOW_HEIGHT))
FISH_IMAGE = pygame.image.load(
    os.path.join('Assets', 'fish.png'))
WINNER_FONT = pygame.font.SysFont('arial', 75)

# draw function
blockSize = 30                                  #Set the size of the grid block
map_width = blockSize*ARRAY_WIDTH;              # size of the map 
map_height = blockSize*ARRAY_HEIGHT;
middle_height = (WINDOW_HEIGHT-map_height)//2   # positioning the map at the center of the screen
middle_width = (WINDOW_WIDTH-map_width)//2
FISH = pygame.transform.scale(FISH_IMAGE, (blockSize, blockSize))           # Fish image in grid

# ~~~
# FUNCTIONS
# ~~~
def main():
    pygame.init()
    global fish_x, fish_y, stepCount
    CLOCK = pygame.time.Clock()

    # game loop
    run = True
    notArrived = True

    
    path = shortest_path(ARRAY, (START_X, START_Y), deadEnd, (DEST_X, DEST_Y), energyBlocks, obstacles)
    stepCount = len(path)
    count = 0
    print(path)
    
    while (run):
        # print(fish_x,fish_y);      #DEBUG
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if (notArrived):            # if fish is still moving
            # Position Updates from path
            fish_x = path[count][0]
            fish_y = path[count][1]

            # update count step
            if ((fish_x, fish_y) in obstacles):
                stepCount+=1
            elif ((fish_x, fish_y) in energyBlocks):
                stepCount-=0.5
            
            drawGrid()
            count+=1
            
            # Checking win condition
            if (DEST_X == fish_x and DEST_Y == fish_y):
                # print("Arrived at destination");    #DEBUG
                notArrived = False
                draw_outcome()

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
            # if (ARRAY[temp_width][temp_height] == 1):             # method to use array instead of set
            if ((temp_width,temp_height)in deadEnd):                # deadEnd
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
            elif ((temp_width,temp_height)in obstacles):            # obstacles
                pygame.draw.rect(SCREEN, GREY, rect, 0)
            elif ((temp_width,temp_height)in energyBlocks):         # energyBlocks
                pygame.draw.rect(SCREEN, ORANGE, rect, 0)
            elif (temp_width == DEST_X and temp_height == DEST_Y):  # destination
                pygame.draw.rect(SCREEN, RED, rect, 0)
            else:                                                   # free space
                pygame.draw.rect(SCREEN, LIGHTGREY, rect, 1)
            if (temp_width == fish_x and temp_height == fish_y):    # fish
                SCREEN.blit(FISH, (x,y))
            temp_width+=1
        temp_height+=1
        temp_width = 0
    pygame.display.update()

def draw_outcome():
    text = "Step Count: "+str(stepCount)
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    SCREEN.blit(draw_text, (WINDOW_WIDTH/2 - draw_text.get_width() /
                         2, WINDOW_HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

if __name__ == "__main__":
    main()
