import pygame
import random

# initialize the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("images/ufo.png"))

# background
background = pygame.image.load("images/background.gif")

# player
playerImg = pygame.image.load("images/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = pygame.image.load("images/enemy.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemySpeed = 0.2
enemyX_change = enemySpeed
enemyY_change = 40


# player function
def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy function
def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# game loop
running = True
while running:

    # screen background
    screen.fill((17, 0, 26))
    screen.blit(background, (-85, 0))

    for event in pygame.event.get():

        # check for QUIT to exit game
        if event.type == pygame.QUIT:
            running = False

        # check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.1
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    # set player boundary control
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
        
    # enemy movement
    enemyX += enemyX_change
        
    # set enemy boundary control
    if enemyX <= 0:
        enemyX_change = enemySpeed
        enemyY += enemyY_change
    elif enemyX >= 736:
        enemyX_change = -enemySpeed
        enemyY += enemyY_change


    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
