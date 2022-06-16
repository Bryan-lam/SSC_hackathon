import pygame
import os
import random
pygame.font.init()

# ---
# Important variables
# ---
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Swimming Across Harbour")
FPS = 60

# Constants
WHITE = (255, 255, 255)
OBSTACLES_WIDTH, OBSTACLES_HEIGHT = 55, 40
WINNER_FONT = pygame.font.SysFont('arial', 100)

VEL = 2
Win = False
Lose = False


# ---
# Importing Art Assets
# ---
FISH_IMAGE = pygame.image.load(
    os.path.join('Assets', 'fish.png'))
FISH = pygame.transform.scale(
    FISH_IMAGE, (OBSTACLES_WIDTH, OBSTACLES_HEIGHT))
# Obstacles
CLAM_IMAGE = pygame.image.load(
    os.path.join('Assets', 'shell.png'))
CLAM = pygame.transform.scale(
    CLAM_IMAGE, (OBSTACLES_WIDTH, OBSTACLES_HEIGHT))
ROCK01_IMAGE = pygame.image.load(
    os.path.join('Assets', 'rock.png'))
ROCK01 = pygame.transform.scale(
    ROCK01_IMAGE, (OBSTACLES_WIDTH, OBSTACLES_HEIGHT))
# Background
OCEAN = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.jpg')), (WIDTH, HEIGHT))


# ---
# Static Objects
# ---
def randomPosition(screenWidth, screenHeight):
    randW = random.randint(0, screenWidth)
    randH = random.randint(0, screenHeight)
    return pygame.Rect(randW, randH, OBSTACLES_WIDTH, OBSTACLES_HEIGHT)

fish_rect = pygame.Rect((WIDTH-OBSTACLES_WIDTH)//2, (HEIGHT-OBSTACLES_HEIGHT), OBSTACLES_WIDTH, OBSTACLES_HEIGHT)
rock01_rect = randomPosition(WIDTH-OBSTACLES_WIDTH, HEIGHT-OBSTACLES_HEIGHT)
#rock01_rect = pygame.Rect((WIDTH-OBSTACLES_WIDTH)//2, (HEIGHT-OBSTACLES_HEIGHT)//2, OBSTACLES_WIDTH, OBSTACLES_HEIGHT) # test lose condition
clam_rect = randomPosition(WIDTH-OBSTACLES_WIDTH, HEIGHT-OBSTACLES_HEIGHT)

obstacles = [rock01_rect, clam_rect]

# ---
# Dynamic Objects
# ---
def fishAlgo(currentPos):
    currentPos.y -= 3

# Obstacles
def dynamicObs(currentPos):
    global VEL
    if currentPos.x + VEL >= WIDTH-currentPos.width:
        VEL = -(VEL)
    elif currentPos.x + VEL <= 0:
        VEL = -(VEL)
    currentPos.x += VEL

# ---
# WIN / LOSE
# ---
def handle_collision(fish_rect, obstacles):
    global Lose
    for obj in obstacles:
        if fish_rect.colliderect(obj):      # --- LOSE CONDITION ---
            Lose = True
            
def draw_outcome(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
# ---
# Main Functions5
# ---
def draw_window(fish_rect, clam_rect):
    global Win
    WIN.blit(OCEAN, (0, 0))     # BG

    # Obstacles
    WIN.blit(CLAM, (clam_rect.x, clam_rect.y))
    WIN.blit(ROCK01, (rock01_rect.x, rock01_rect.y))

    if (fish_rect.x <= 0):
        fish_rect.x = 0
    elif (fish_rect.x >= WIDTH):
        fish_rect.x = WIDTH
    if (fish_rect.y <= 0):      # --- WIN CONDITION ---
        fish_rect.y = 0
        Win = True
    WIN.blit(FISH, (fish_rect.x, fish_rect.y))  # Fish

    pygame.display.update()

def main():
    clock = pygame.time.Clock() #FPS

    # game loop
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            # Close window condition == quit game loop
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if Win:
            draw_outcome("You Win")
            break
        if Lose:
            draw_outcome("You Lose")
            break
        # Position Updates
        fishAlgo(fish_rect)
        dynamicObs(clam_rect)

        handle_collision(fish_rect, obstacles)
        
        draw_window(fish_rect, clam_rect)   # Draw Function
    main()

if __name__ == "__main__":
    main()
