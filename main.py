import pygame
import random

from pygame import mixer

PLAYER_SPEED = 0.4
# ENEMY_SPEED = random.uniform(0.15, 0.3)
MISSILE_SPEED = 0.5

# initialize the pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.image.load("resources/ufo.png"))

# background
background = pygame.image.load("resources/background.gif")
mixer.music.load("resources/spaceship-cruising-ufo-7176.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.2)

# player
playerImg = pygame.image.load("resources/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Create Rects for collision detection
player_rect = playerImg.get_rect()
player_rect.topleft = (playerX, playerY)

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_rects = []
num_of_enemies = 6

# create enemies in list
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("resources/enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.uniform(0.15, 0.3))
    enemyY_change.append(60)

    # Create Rects for collision detection
    enemy_rect = enemyImg[i].get_rect()
    enemy_rect.topleft = (enemyX[i], enemyY[i])
    enemy_rects.append(enemy_rect)

# missile
missileImg = pygame.image.load("resources/missile.png")
missileX = 0
missileY = 480
missileX_change = 0
missileY_change = MISSILE_SPEED
missile_state = "ready"

missile_rect = missileImg.get_rect()
missile_rect.topleft = (missileX, missileY)

# explosion
explosionImg = pygame.image.load("resources/explode.png")
explodeX = 0
explodeY = 0
explosion_timer = 0

# score
score_value = 0
score_font = pygame.font.Font("resources/Kiona-Regular.ttf", 24)

# game over
game_over_font = pygame.font.Font("resources/Kiona-Regular.ttf", 64)


# game functions
def show_score():
    score_text = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score_text, (20, 20))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (220, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missileImg, (x + 16, y + 10))


def explosion(x, y):
    screen.blit(explosionImg, (x, y))


# game loop
running = True
while running:

    # screen background
    screen.fill((17, 0, 26))
    screen.blit(background, (-95, 0))

    for event in pygame.event.get():

        # check for QUIT to exit game
        if event.type == pygame.QUIT:
            running = False

        # check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                playerX_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missileX = playerX
                    fire_missile(missileX, missileY)
                    missile_sound = mixer.Sound("resources/laser.wav")
                    missile_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # player movement
    playerX += playerX_change

    # Update Rect positions
    player_rect.topleft = (playerX, playerY)
    missile_rect.topleft = (missileX, missileY)

    # set player boundary control
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # game over
        if enemy_rects[i].colliderect(player_rect):
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            explosion_sound = mixer.Sound("resources/player_explode.mp3")
            explosion_sound.play()
            explosion_timer = 240
            explodeX = playerX
            explodeY = playerY
            playerY = 2000
            game_over()
            break

        # move enemy
        enemyX[i] += enemyX_change[i]

        # set enemy boundary control
        if enemyX[i] <= 0:
            enemyX_change[i] = abs(enemyX_change[i])
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]

        enemy_rects[i].topleft = (enemyX[i], enemyY[i])

        # enemy hit detection
        if missile_rect.colliderect(enemy_rects[i]):
            explosion_sound = mixer.Sound("resources/enemy_explode.mp3")
            explosion_sound.play()
            explosion_timer = 240
            explodeX = enemyX[i]
            explodeY = enemyY[i]
            missileY = 520
            missile_state = "ready"
            score_value += 1
            # restart enemy
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            enemy_rects[i].topleft = (enemyX[i], enemyY[i])
            enemyX_change[i] = enemyX_change[i] * 1.5  # increase enemy speed each respawn

        enemy(enemyX[i], enemyY[i], i)

    # explosion management
    if explosion_timer > 0:
        explosion(explodeX, explodeY)
        explosion_timer -= 1

    # missile movement
    # reset missile
    if missileY <= 0:
        missileY = 480
        missile_state = "ready"

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY -= missileY_change

    player(playerX, playerY)
    show_score()
    pygame.display.update()
