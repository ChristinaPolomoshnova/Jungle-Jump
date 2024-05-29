import pygame
import random

'''- - - - - - - - - - - - - - - - - - - - - - - - КЛАСС ПЛАТФОРМ - - - - - - - - - - - - - - - - - - - - - - - - - - '''
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving, dis):
        self.SCREEN_WIDTH = 550
        self.SCREEN_HEIGHT = 800
        platform_image = pygame.image.load('Assets/grass_platform.png').convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 15))  # определяем ширину(она будет всегда немного разной) и высоту платформы
        self.moving = moving
        self.dis = dis
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])  # задаём направление перемещения платформы
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()  # границы платформы
        self.rect.x = x
        self.rect.y = y

    # функция обновления платформ после прокрутки
    def update(self, scroll):

         # перемещение платформы из стороны в сторону, если это движущаяся платформа
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        # изменить направление платформы, если она дошла до края экрана
        if self.move_counter >= 180 or self.rect.left < 0 or self.rect.right > self.SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        # обновить вертикальное положение платформы
        self.rect.y += scroll

        # платформа исчезла с экрана
        if self.rect.top > self.SCREEN_HEIGHT:
            self.kill()

'''- - - - - - - - - - - - - - - - - - - - - - - - КЛАСС ПРУЖИНКИ - - - - - - - - - - - - - - - - - - - - - - - - - - '''
class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.SCREEN_HEIGHT = 800
        self.image = pygame.image.load("assets/spring.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# функция обновления пружинки после прокрутки
    def update(self, scroll):
        # обновить вертикальное положение платформы
        self.rect.y += scroll
        # пружинка исчезла с экрана
        if self.rect.top > self.SCREEN_HEIGHT:
            self.kill()
