import random
import pygame
import math
from Class import Player, Enemy, Bullet, Particle, PowerUp, Randomize
# from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Images\\ufo.png")
pygame.display.set_icon(icon)

background = pygame.image.load("Images\\Background.png")
Velocity = 2
n = 0
Flipbackgorund = pygame.transform.flip(background, False, True)

Yno = [-600, 0]

player = Player(370, 480)
RedHeart = pygame.image.load("Images\\RedHeart.png")

enemy = []
EnemySpeedX = 1
EnemySpeedY = 0.15
n = 0
NumberOfEnemy = 5

bullet = []
reload = False
NumberOfBullet = 10
RemainingBullet = NumberOfBullet
reloadImg = pygame.image.load("Images\\bullet.png")
l = 0
ReloadSpeed = 25

particle = []

powerup = []
BulletAdd = 10
ReloadIncrease = 3

font = pygame.font.Font("freesansbold.ttf", 32)
score_value = 0

GameOver = False
gameoverfont = pygame.font.Font("freesansbold.ttf", 64)


def isCollision(X1, Y1, X2, Y2, Value):
    distance = math.sqrt((math.pow(X2 - X1, 2)) + (math.pow(Y2 - Y1, 2)))
    if distance < Value:
        return True
    else:
        return False


def isEnemyCollision(X1, Y1, X2, Y2):
    if abs(X1 - X2) >= 50 or abs(Y1 - Y2) >= 50:
        Value = 30
    else:
        Value = 48
    distance = math.sqrt((math.pow(X2 - X1, 2)) + (math.pow(Y2 - Y1, 2)))
    if distance < Value:
        return True
    else:
        return False


def NotOverlap(X1=0, X2=736, Y1=60, Y2=200):
    Endloop = True
    CheckEndloop = False
    RandomIntX = 0
    RandomIntY = 0
    while Endloop:
        RandomIntX = random.randint(X1, X2)
        RandomIntY = random.randint(Y1, Y2) * -1
        CheckEndloop = False
        for i in enemy:
            nCollision = isCollision(RandomIntX, RandomIntY, i.EnemyX, i.EnemyY, 75)
            if nCollision:
                CheckEndloop = True
                break
        if not CheckEndloop:
            Endloop = False

    return RandomIntX, RandomIntY


# def nNotOverlap():
#     Endloop = True
#     X = False
#     RandomIntX = 0
#     RandomIntY = random.randint(50, 200)
#
#     while Endloop:
#         X = False
#         RandomIntX = random.randint(0, 736)
#         for i in enemy:
#             if i.EnemyX - 80 <= RandomIntX <= i.EnemyX + 80:
#                 X = True
#                 break
#         if not X:
#             Endloop = False
#         else:
#             if i.EnemyY - 80 <= RandomIntY <= i.EnemyY + 80:
#                 Endloop = False
#
#     Endloop = True
#
#     # while Endloop:
#     #     Y = False
#     #     RandomIntY = random.randint(50, 200)
#     #     for i in enemy:
#     #         if i.EnemyY - 64 <= RandomIntY <= i.EnemyY + 64:
#     #             Y = True
#     #             break
#     #     if not Y:
#     #         Endloop = False
#
#     return RandomIntX, RandomIntY


def IncreaseNumOfEnemy():
    X, Y = NotOverlap()
    enemy.append(Enemy(X, Y, EnemySpeedX, EnemySpeedY))


def DefineEnemyDeceleration():
    for i in enemy:
        i.EnemyDeceleration = i.EnemyYChange / (50 * random.randint(1, 4))


def Teleport(Y):
    X1, Y1 = NotOverlap(0, 736, round(Y - 50), round(Y + 50))
    return X1, Y1


def Reload():
    global reload, l, RemainingBullet, NumberOfBullet
    if reload:
        l += 1
        if l == ReloadSpeed:
            l = 0
            RemainingBullet += 1
            if RemainingBullet >= NumberOfBullet:
                reload = False


def ShowParticle():
    for i in particle:
        if i.Size >= i.MaxSize:
            particle.remove(i)
        elif i.Timer == i.MaxTimer:
            i.Show(screen)
            i.Size += 5
            i.Timer = 1
        else:
            i.Show(screen)
            i.Timer += 1


def AddPowerUp(X, Y):
    global BulletAdd, ReloadIncrease
    ran = Randomize((100 - BulletAdd * 5 - ReloadIncrease * 10, BulletAdd * 5, ReloadIncrease * 10))
    if ran == 2:
        BulletAdd -= 1
    elif ran == 3:
        ReloadIncrease -= 1
    powerup.append(PowerUp(X + 33, Y + 33, ran))


def ShowPowerUp():
    for i in powerup:
        i.Show(screen)
        i.Y += 4
        if i.Y >= 660:
            powerup.remove(i)


def PowerUpCollision():
    global score_value, NumberOfBullet, ReloadSpeed
    for i in powerup:
        PCollision = isCollision(i.X, i.Y, player.PlayerX, player.PlayerY, 70)
        if PCollision:
            if i.Type == 1:
                if i.SubType == 1:
                    player.RemainingHp += 1
                elif i.SubType == 2:
                    score_value += 20
            elif i.Type == 2:
                NumberOfBullet += 1
            elif i.Type == 3:
                ReloadSpeed -= 5
            powerup.remove(i)


def ShowRemainingLives():
    X = 750
    Y = 10
    for i in range(player.RemainingHp):
        screen.blit(RedHeart, (X, Y))
        X -= 37


def ShowRemainingBullet():
    X = 0
    Y = 558
    for i in range(RemainingBullet):
        screen.blit(reloadImg, (X, Y))
        X += 16


def show_score():
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def gameover():
    over = gameoverfont.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (220, 250))


def ShowBackGround():
    global Velocity, n
    screen.blit(background, (0, Yno[0]))
    screen.blit(Flipbackgorund, (0, Yno[1]))
    # screen.blit(background, (0, Yno[2]))

    for i in range(len(Yno)):
        Yno[i] += Velocity
        if Yno[i] >= 600:
            Yno[i] = -600
    if GameOver:
        n += 1
        if n >= 10:
            n = 0
            if Velocity > 0:
                Velocity -= 0.5
            else:
                Velocity = 0


for i in range(NumberOfEnemy):
    IncreaseNumOfEnemy()

for i in range(NumberOfBullet):
    bullet.append(Bullet())

running = True

while running:
    screen.fill((0, 0, 0))

    # BackGround-----------------------------------------------------------
    ShowBackGround()
    # Event ---------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.PlayerXChange = player.PlayerSpeed * -1
            if event.key == pygame.K_RIGHT:
                player.PlayerXChange = player.PlayerSpeed
            if event.key == pygame.K_UP:
                player.PlayerYChange = player.PlayerSpeed * -1
            if event.key == pygame.K_DOWN:
                player.PlayerYChange = player.PlayerSpeed
            if event.key == pygame.K_SPACE:
                if not reload and RemainingBullet > 0 and not GameOver:
                    for i in bullet:
                        if i.bullet_state == "ready":
                            # bullet_sound = mixer.Sound("Sound\\Bullet.sfs")
                            # bullet_sound.play()
                            i.bullet_state = "fire"
                            i.bulletX = player.PlayerX
                            i.bulletY = player.PlayerY
                            RemainingBullet -= 1
                            break
            if event.key == pygame.K_r:
                if not reload and RemainingBullet != NumberOfBullet:
                    reload = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.PlayerXChange = 0

            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.PlayerYChange = 0

    # Player ---------------------------------------------------------------

    player.PlayerX += player.PlayerXChange
    player.PlayerY += player.PlayerYChange

    # print(player.PlayerX)
    # print(player.PlayerY)
    # print(player.PlayerXChange)
    # print(player.PlayerYChange)

    if player.PlayerX <= 0 and player.PlayerX != 2000:
        player.PlayerX = 0
    elif player.PlayerX >= 736 and player.PlayerX != 2000:
        player.PlayerX = 736

    if player.PlayerY <= 0 and player.PlayerY != 2000:
        player.PlayerY = 0
    elif player.PlayerY >= 536 and player.PlayerY != 2000:
        player.PlayerY = 536

    # Enemy ---------------------------------------------------------------

    for i in enemy:
        # n += 1

        # Game Over
        # PlayerCollision
        if not GameOver:
            if player.CoolDownTime == 0:
                PlayerEnemyCollision = isCollision(i.EnemyX, i.EnemyY, player.PlayerX, player.PlayerY, 70)
                if PlayerEnemyCollision:
                    player.RemainingHp -= 1
                    player.CoolDownTime = 1
                    player.ShowBool = False
                    DefineEnemyDeceleration()

            # EnemyReached

            if i.EnemyY >= 632:
                player.RemainingHp -= 1
                enemy.remove(i)
                IncreaseNumOfEnemy()
                DefineEnemyDeceleration()
        else:
            if i.EnemyY >= 670:
                enemy.remove(i)

        # Enemy Movement

        i.EnemyX += i.EnemyXChange
        i.EnemyY += i.EnemyYChange

        if i.EnemyX <= 0:
            i.EnemyX = 0
            i.EnemyXChange *= -1
            i.Direction *= -1
        elif i.EnemyX >= 736:
            i.EnemyX = 736
            i.EnemyXChange *= -1
            i.Direction *= -1

        # bullet collision

        for k in bullet:
            if k.bullet_state == "ready":
                continue
            collision = isCollision(i.EnemyX, i.EnemyY, k.bulletX, k.bulletY, 27)
            if collision:
                k.bullet_state = "ready"
                k.bulletY = 0
                k.bulletX = 0
                i.HP -= 1
                if i.EnemyType == 3 and i.HP > 0:
                    particle.append(Particle(i.EnemyX + 33, i.EnemyY + 33, 2))
                    i.EnemyX, i.EnemyY = Teleport(i.EnemyY)

                if i.HP == 0:
                    particle.append(Particle(i.EnemyX + 33, i.EnemyY + 33, 1))
                    nRandom = Randomize((15, 85))
                    if nRandom == 1:
                        AddPowerUp(i.EnemyX, i.EnemyY)
                    score_value += i.Score
                    enemy.remove(i)
                    IncreaseNumOfEnemy()
                    nRandom = Randomize((5, 95))
                    if nRandom == 1:
                        if len(enemy) <= 20:
                            EnemySpeedX += 0.005
                            EnemySpeedY += 0.0025
                            player.PlayerSpeed += 0.02
                            for j in bullet:
                                j.bulletY_change += 0.05
                            for j in enemy:
                                j.EnemyXChange = EnemySpeedX * j.EnemySpeed * j.Direction
                                j.EnemyYChange = EnemySpeedY * j.EnemySpeed
                            IncreaseNumOfEnemy()
        # # Enemy collision
        # for k in range(n, len(enemy)):
        #     if enemy[k].EnemyCollision != 0 and i.EnemyCollision != 0:
        #         continue
        #     EnemyCollision = isEnemyCollision(i.EnemyX, i.EnemyY, enemy[k].EnemyX, enemy[k].EnemyY)
        #     if EnemyCollision:
        #         i.EnemyXChange *= 1.2
        #         enemy[k].EnemyXChange *= 1.2
        #         i.EnemyCollision = 1
        #         enemy[k].EnemyCollision = 1
        #         if i.EnemyXChange < 0 and enemy[k].EnemyXChange < 0:
        #             if i.EnemyX <= enemy[k].EnemyX:
        #                 enemy[k].EnemyXChange *= -1
        #                 enemy[k].Direction *= -1
        #                 i.EnemyXChange -= 0.005
        #         elif i.EnemyXChange > 0 and enemy[k].EnemyXChange > 0:
        #             pass
        #         #     if i.EnemyX <= enemy[k].EnemyX:
        #         #         i.EnemyXChange *= -1
        #         #         i.Direction *= -1
        #         #         if enemy[k].EnemyXChange < 0:
        #         #             enemy[k].EnemyXChange -= 0.01
        #         #         else:
        #         #             enemy[k].EnemyXChange += 0.1
        #         #     elif i.EnemyX >= enemy[k].EnemyX:
        #         #         enemy[k].EnemyXChange *= -1
        #         #         enemy[k].Direction *= -1
        #         #         if i.EnemyXChange < 0:
        #         #             i.EnemyXChange += 0.1
        #         #             if EnemySpeedX * i.EnemySpeed * i.Direction - 1 < i.EnemyXChange:
        #         #                 EnemyXChange = EnemySpeedX * i.EnemySpeed * i.Direction - 1
        #         #         else:
        #         #             i.EnemyXChange += 0.01
        #         # else:
        #         i.EnemyXChange *= -1
        #         i.Direction *= -1
        #         enemy[k].EnemyXChange *= -1
        #         enemy[k].Direction *= -1

        i.Show(screen)

    # # Enemy Collision Reset-------------------------------------------------
    #
    # for i in enemy:
    #     if i.EnemyCollision == 25:
    #         i.EnemyCollision = 0
    #         i.EnemyXChange = EnemySpeedX * i.EnemySpeed * i.Direction
    #     elif i.EnemyCollision != 0:
    #         i.EnemyCollision += 1

    # Bullet ---------------------------------------------------------------
    if not GameOver:
        for i in bullet:
            if i.bullet_state == "fire":
                i.bulletY -= i.bulletY_change
                if i.bulletY <= -32:
                    i.bullet_state = "ready"
                    i.bulletX = 0
                    i.bulletY = 0
                else:
                    i.Show(screen)

        ShowRemainingBullet()
    # Power Collision-----------------------------------------------------
    PowerUpCollision()
    # Reload -------------------------------------------------------------
    Reload()
    # PlayerCoolDown------------------------------------------------------

    if player.CoolDownTime != 0 and not GameOver:
        if player.CoolDownTime != player.MaxCoolDownTime:
            player.CoolDownTime += 1
            if player.CoolDownTime % (player.MaxCoolDownTime / 4) == 0:
                player.ShowBool = False
            elif player.CoolDownTime % (player.MaxCoolDownTime / 4) == 9:
                player.ShowBool = True
        else:
            player.CoolDownTime = 0
            player.ShowBool = True

    # Game Over True

    if player.RemainingHp <= 0:
        GameOver = True
        for i in enemy:
            i.EnemyYChange += 0.04
            if round(abs(i.EnemyXChange * 100)) != 0:
                i.EnemyXChange = (abs(i.EnemyXChange) - abs(i.EnemyDeceleration)) * i.Direction
            else:
                i.EnemyXChange = 0
        player.ShowBool = False
        gameover()

    # Show ---------------------------------------------------------------
    show_score()
    ShowParticle()
    ShowPowerUp()
    ShowRemainingLives()
    player.Show(screen)
    pygame.display.update()
