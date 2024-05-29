import pygame
import random

class Enemy_bird(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)
        # определение переменных движения
        self.animation_list = []
        self.frame_index = 0

        self.update_time = pygame.time.get_ticks()  # время обновления кадров

        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

        # загрузка изображения из электронной таблицы
        animation_steps = 7
        for animation in range(animation_steps):
            image = sprite_sheet.get_image(animation, 68, 68, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False) # переворачиваем по х, игнорируя поворот по у
            image.set_colorkey((0, 0, 0)) # необходимо для сохранения прозрачности
            self.animation_list.append(image)

        # нужно выбрать начальное изображение и создать из него прямоугольник
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direction == 1:
            self.rect.x = -100
            self.rect.y = y
        else:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = y

    def update(self, scroll, SCREEN_WIDTH):
        # обновление анимации
        ANIMATION_COOLDOWN = 65 # обновление кадра раз в 65 миллисекунд

        # обновить изображение в зависимости от текущего кадра
        self.image = self.animation_list[self.frame_index]

        # проверка на то, прошло ли достаточно времени с момента последнего обновления
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # если aнимация закончилась, то нужно вернуться к началу
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0


        # переместить врага
        self.rect.x += self.direction * 3
        self.rect.y += scroll


        # проверка на исчезновение с экрана
        if self.rect.right == 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
