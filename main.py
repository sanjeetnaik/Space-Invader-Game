import pygame
import random
import math

# Initialize pygame
pygame.init()

# Create Screen
screen = pygame.display.set_mode((800, 600))

# Background Image

background = pygame.image.load('background_image.jpg')

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
# Player

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6

for i in range(0, num_of_enemies, 1):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# enemyImg = pygame.image.load('enemy.png')
# enemyX = random.randint(0, 736)
# enemyY = random.randint(50, 150)
# enemyX_change = 0.3
# enemyY_change = 40

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.5
bullet_state = 'ready'

score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

over_font = pygame.font.Font('freesansbold.ttf', 64)

testX = 10
testY = 10

def show_score(x,y):
    temp = font.render('Score : '+ str(score), True, (255,255,255))
    screen.blit(temp,(x,y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))  # for bullet to be at the centre of spaceship

def game_over_text():
    temp = over_font.render('GAME OVER ', True, (255, 255, 255))
    screen.blit(temp, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if (dist < 27):
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))

    # Background image

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT):
                playerX_change -= 0.3
            if (event.key == pygame.K_RIGHT):
                playerX_change += 0.3
            if (event.key == pygame.K_SPACE):
                if (bullet_state == 'ready'):
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if (event.type == pygame.KEYUP):

            if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                playerX_change = 0

    playerX += playerX_change

    if (playerX <= 0):
        playerX = 0
    elif (playerX >= 736):
        playerX = 736

    for i in range(num_of_enemies):

        #Game Over

        if(enemyY[i] > 440):
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if (enemyX[i] <= 0):
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif (enemyX[i] >= 736):
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collsision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if (collision == True):
            bulletY = 480
            bullet_state = 'ready'
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i],i)

    # Bullet movement

    if (bulletY <= 0):
        bullet_state = 'ready'
        bulletY = 480
    if (bullet_state == 'fire'):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(testX,testY)
    pygame.display.update()
