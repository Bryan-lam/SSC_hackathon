import os
import pygame
from raph_submission import shortest_path
from map_sample import MAP2 as MAP
from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'

ROW = len(MAP[0])
COL = len(MAP)
START_COLOR = (255, 0, 0, 64)
END_COLOR = (0, 255, 0)
WALL_COLOR = (150, 150, 150)
ENERGY_COLOR = (255, 128, 0)
TEXT_COLOR = (255, 255, 255)

PLAYER_IMAGE = "assets/fish.png"
BACKGROUND_IMAGE = "assets/background.jpg"
WALL_IMAGES = ["assets/rock_1.png", "assets/rock_2.png",
               "assets/rock_3.png", "assets/rock_4.png"]
OBSTACLE_IMAGES = ["assets/clam_1.png", "assets/clam_2.png"]


class GameState():
    def __init__(self):
        self.playerPos = Vector2(0, 0)
        self.lastPlayerPos = self.playerPos
        self.worldSize = Vector2(ROW, COL)
        self.stepCount = 0

    def setPlayerPos(self, pos):
        self.playerPos = pos

    def update(self, moveCommand):
        self.playerPos += moveCommand

        x = int(self.playerPos.x)
        y = int(self.playerPos.y)

        if x < 0 or x >= ROW or y < 0 or y >= COL or MAP[y][x] == 3:
            self.playerPos -= moveCommand
            return

        self.lastPlayerPos = self.playerPos - moveCommand
        if x < 0:
            x = 0
        elif x >= ROW:
            x = ROW - 1

        elif y < 0:
            y = 0
        elif y >= COL:
            y = COL - 1

        if MAP[y][x] == 4:
            self.stepCount += 2
        elif MAP[y][x] == 5:
            self.stepCount += 0.5
        else:
            self.stepCount += 1


class UserInterface():
    def __init__(self):
        pygame.init()

        self.gameState = GameState()
        self.cellSize = Vector2(32, 32)

        self.windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode(
            (int(self.windowSize.x), int(self.windowSize.y)))

        self.playerTexture = pygame.image.load(PLAYER_IMAGE)
        self.background = pygame.transform.scale(pygame.image.load(
            BACKGROUND_IMAGE), (int(self.windowSize.x), int(self.windowSize.y)))
        self.obstacles = []
        for obstacle in OBSTACLE_IMAGES:
            self.obstacles.append(pygame.transform.scale(pygame.image.load(
                obstacle), (int(self.cellSize.x), int(self.cellSize.y))))
        self.walls = []
        for wall in WALL_IMAGES:
            self.walls.append(pygame.transform.scale(pygame.image.load(
                wall), (int(self.cellSize.x), int(self.cellSize.y))))

        self.moveCommand = Vector2(0, 0)
        self.window.blit(self.background, (0, 0))
        self.genMap()
        self.updatePlayer()

        initialPos = Vector2(0, 0)  # get start pos
        for y in range(COL):
            for x in range(ROW):
                if MAP[y][x] == 1:
                    initialPos = Vector2(x, y)
                    break

        self.gameState.setPlayerPos(initialPos)

        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        self.moveCommand = Vector2(0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.moveCommand = Vector2(1, 0)
                elif event.key == pygame.K_LEFT:
                    self.moveCommand = Vector2(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.moveCommand = Vector2(0, 1)
                elif event.key == pygame.K_UP:
                    self.moveCommand = Vector2(0, -1)
                self.updatePlayer()

    def updatePlayer(self):
        self.gameState.update(self.moveCommand)

        if self.gameState.playerPos != self.gameState.lastPlayerPos:
            self.updateCell(int(self.gameState.lastPlayerPos.x),
                            int(self.gameState.lastPlayerPos.y), True)

        spritePoint = self.gameState.playerPos.elementwise()*self.cellSize
        self.window.blit(pygame.transform.scale(
            self.playerTexture, (int(self.cellSize.x), int(self.cellSize.y))), spritePoint)

        pygame.display.update()

        self.checkEnd(int(self.gameState.playerPos.x),
                      int(self.gameState.playerPos.y),)

    def genMap(self):
        for y in range(COL):
            for x in range(ROW):
                self.updateCell(x, y, False)

    def updateCell(self, x, y, isMove):
        currentPos = MAP[y][x]
        pos = Vector2(x, y).elementwise()*self.cellSize
        rect = pygame.Rect(
            int(pos.x), int(pos.y), int(self.cellSize.x), int(self.cellSize.y))

        if isMove and currentPos == 0:
            self.window.blit(self.background, pos, rect)
        elif currentPos == 1:
            pygame.draw.rect(self.window, START_COLOR, rect)
        elif currentPos == 2:
            pygame.draw.rect(self.window, END_COLOR, rect)
        elif currentPos == 3:
            random = (x * y + y % len(WALL_IMAGES)) % len(WALL_IMAGES)
            self.window.blit(self.walls[random], pos)
        elif currentPos == 4:
            self.window.blit(self.background, pos, rect)
            random = (x * y + y % len(OBSTACLE_IMAGES)) % len(OBSTACLE_IMAGES)
            self.window.blit(self.obstacles[random], pos)
        elif currentPos == 5:
            pygame.draw.rect(self.window, ENERGY_COLOR, rect)

    def checkEnd(self, x, y):
        if MAP[y][x] == 2:
            text = pygame.font.SysFont(
                'arial', 45).render(str(self.gameState.stepCount) + " steps", 1, TEXT_COLOR)
            self.window.blit(text, (self.windowSize.x/2 - text.get_width() /
                                    2, self.windowSize.y/2 - text.get_height()/2))
            pygame.display.update()

            print("You win! Step count:", self.gameState.stepCount)
            pygame.time.delay(2000)
            self.running = False

    def run(self, isStudent):
        while self.running:
            if isStudent:
                self.processInput()
                commands = shortest_path(MAP, Vector2(1, 0), Vector2(-1, 0),
                                         Vector2(0, 1), Vector2(0, -1))
                for step in commands:
                    self.moveCommand = step
                    self.updatePlayer()
                    pygame.time.delay(75)
                    self.clock.tick(60)
                return
            self.processInput()
            self.clock.tick(60)


userInterface = UserInterface()
userInterface.run(True)

# print(shortest_path(MAP,))

pygame.quit()
