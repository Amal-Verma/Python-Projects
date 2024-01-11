import pygame
import random


def Randomize(List):
    Sum = 0
    for i in List:
        Sum += i

    RandomNum = random.randint(0, Sum)
    MinValue = 0
    MaxValue = 0
    for i in range(0, len(List)):
        if (i - 1) < 0:
            MinValue = 0
        else:
            MinValue = List[i - 1]

        if i > len(List):
            MaxValue = Sum + 10
        else:
            MaxValue = MaxValue + List[i]

        if MinValue <= RandomNum <= MaxValue:
            return i + 1


class Bullet:
    def __init__(self, ):
        self.bulletImg = pygame.image.load("Images\\bullet.png")
        self.bulletX = 0
        self.bulletY = 0
        self.bulletY_change = 10
        self.bullet_state = "ready"

    def Show(self, screen):
        screen.blit(self.bulletImg, (self.bulletX + 15, self.bulletY + 10))


class Player:
    def __init__(self, PlayerX, PlayerY):
        self.PlayerImg = pygame.image.load("Images\\spaceship.png")
        self.PlayerX = PlayerX
        self.PlayerY = PlayerY
        self.PlayerXChange = 0
        self.PlayerYChange = 0
        self.PlayerSpeed = 4
        self.RemainingHp = 3
        self.MaxCoolDownTime = 60
        self.CoolDownTime = 0
        self.ShowBool = True

    def Show(self, screen):
        if self.ShowBool:
            screen.blit(self.PlayerImg, (self.PlayerX, self.PlayerY))


class Enemy:
    def __init__(self, EnemyX, EnemyY, EnemySpeedX, EnemySpeedY):
        self.EnemyX = EnemyX
        self.EnemyY = EnemyY
        RandomType = Randomize((50, 30, 20))
        self.EnemyType = RandomType
        self.HP = RandomType
        self.DefaultHP = RandomType
        if RandomType == 1:
            self.EnemyImg = pygame.image.load("Images\\Enemy1.png")
            self.EnemySpeed = 2
            self.HP = 2
            self.DefaultHP = 2
            self.Score = 1
        elif RandomType == 2:
            self.EnemyImg = pygame.image.load("Images\\Enemy2.png")
            self.EnemySpeed = 5
            self.HP = 1
            self.DefaultHP = 1
            self.Score = 3
        elif RandomType == 3:
            self.HP = 3
            self.DefaultHP = 3
            self.EnemyImg = pygame.image.load("Images\\Enemy3.png")
            self.EnemySpeed = 1
            self.Score = 5

        RandomNum = random.randint(0, 1)

        if RandomNum == 0:
            self.Direction = 1
        else:
            self.Direction = -1

        self.EnemyXChange = EnemySpeedX * self.EnemySpeed * self.Direction
        self.EnemyYChange = EnemySpeedY * self.EnemySpeed
        self.EnemyDeceleration = 0

    def Show(self, screen):
        screen.blit(self.EnemyImg, (self.EnemyX, self.EnemyY))


class Particle:
    def __init__(self, X, Y, Type):
        self.X = X
        self.Y = Y
        self.Type = Type
        self.Size = 0
        self.MaxSize = 50
        self.Timer = 0
        self.MaxTimer = 1
        self.XTemp = X
        self.YTemp = Y
        self.ImgTemp = ""
        if Type == 1:
            self.Img = pygame.image.load("Images/Particle2.png")
        elif Type == 2:
            self.Img = pygame.image.load("Images/Particle1.png")

    def Show(self, screen):
        Temp = self.Size * 2 + 1
        self.ImgTemp = pygame.transform.scale(self.Img, (Temp, Temp))
        screen.blit(self.ImgTemp, (self.X - self.Size, self.Y - self.Size))


class PowerUp:

    def __init__(self, X, Y, Type):
        self.X = X - 24
        self.Y = Y - 24
        self.Type = Type
        self.SubType = 0
        if Type == 1:
            self.SubType = Randomize((30, 40))
            if self.SubType == 1:
                self.Img = pygame.image.load("Images\\RedHeart.png")
            elif self.SubType == 2:
                self.Img = pygame.image.load("Images\\Power up\\coin.png")
        elif Type == 2:
            self.Img = pygame.image.load("Images\\Power up\\Bulletadd.png")
        elif Type == 3:
            self.Img = pygame.image.load("Images\\Power up\\ReloadSpeed.png")

        self.Img = pygame.transform.scale(self.Img, (50, 50))

    def Show(self, screen):
        screen.blit(self.Img, (self.X, self.Y))

# player = Enemy(2, 3, 0, 0)
# print(player.playerImg)
# print(player.PlayerX)
# print(player.PlayerY)
# print(player.PlayerXChange)
# print(player.PlayerYChange)
# nOutput = []
# for i in range(1, 1000000):
#     nOutput.append(Randomize((10, 20, 30, 40)))
#
# print(nOutput.count(1))
# print(nOutput.count(2))
# print(nOutput.count(3))
# print(nOutput.count(4))
