import pygame
import random
from pygame import mixer  # для музыки
import os  # понадобится для сохранение наибольшего счёта

from spritesheet import *
from bird_enemy import *
from platforms import *
from constants import *
from enemies import *

# Инициализация библиотеки
pygame.init()
mixer.init()

# задаём размеры экрана, чтобы не было рамок, можно прописать flags = pygame.NOFRAME
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# прописываем название окошка
pygame.display.set_caption('Jungle Jump')
icon = pygame.image.load('Assets/icon.png')
pygame.display.set_icon(icon)

# создаём файл для записи и чтения наибольшего результата
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# определение шрифта
font_small = pygame.font.SysFont('Silkcscreen', 30)
font_big = pygame.font.SysFont('Silkcscreen', 43)

# загрузка изображений
jumpy_image = pygame.image.load('Assets/frog.png').convert_alpha()
bg_image = pygame.image.load('Assets/bg_crop.jpg').convert_alpha()
platform_image = pygame.image.load('Assets/grass_platform.png').convert_alpha()

#анимация птицы
bird_sheet_img = pygame.image.load('Assets/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)

# Загрузка изображений врагов
enemy_images = [
    pygame.image.load('Assets/trap.png').convert_alpha(),
    pygame.image.load('Assets/fat_frog.png').convert_alpha(),
    pygame.image.load('Assets/dark_frog.png').convert_alpha()
]

# функция вывода текста на экран
def draw_text(text, font, text_col, x, y):
    ing = font.render(text, True, text_col)
    screen.blit(ing, (x, y))

# функция для вывода информационной панели
def draw_panel():
    pygame.draw.rect(screen, GREEN, (0, 0, SCREEN_WIDTH, 30))
    pygame.draw.line(screen, WHITE, (0,30), (SCREEN_WIDTH,30), 2)
    draw_text('SCORE: ' + str(score), font_small, WHITE, 30, 7)

# функция для рисования фона
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0, 0 + bg_scroll))
    screen.blit(bg_image, (0, - 800 + bg_scroll))

'''- - - - - - - - - - - - - - - - - - - - - - - КЛАСС ИГРОКА - - - - - - - - - - - - - - - - - - - '''
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(jumpy_image, (65, 65))  # Размер игрока
        self.width = 55  # ширина рамки
        self.height = 65  # высота рамки
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0  # скорость в направлении у
        # переворачиваем игрока в зависимости от того, в какую сторону он двигается
        self.flip = False
        self.spring_jump = False

    def move(self):
        # сбросить переменные
        scroll = 0
        dx = 0
        dy = 0

        # обработка нажатия клавиш
        key = pygame.key.get_pressed()
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            dx = -7  # скорость перемещения
            self.flip = False # переворачиваем персонажа
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            dx = 7
            self.flip = True

        # гравитация
        self.vel_y += GRAVITY  # скорость перемещения будет увеличиваться с каждой итерацией
        dy += self.vel_y

        # проверка на наличие коллизий (столкновений), чтобы игрок не выходил за пределы экрана
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # проверка столкновений с платформами
        for platform in platform_group:
            # проверяем столкновения только по у, т.к столкновение с х не имеет значения
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): #прогнозируем перемещение границ игрока
            # проверка, что игрок находится над платформой
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:  #проверяем, падает ли игрок вниз
                        self.rect.bottom = platform.rect.centery # приравниваем рамку игрока к рамке платформы
                        dy = 0
                        self.vel_y = -25
                        jump_fx.play()  # музыка
                        if p_dis == 1:
                            platform.kill()

        for spring in spring_group:
            if spring.rect.colliderect(self.rect):
                self.vel_y = -50  # Высокий прыжок от пружинки
                spring_fx.play()
                self.spring_jump = True  # Игрок прыгает от пружины
                spring.kill()

        # проверяет, если игрок отскочил в верхнюю часть экрана
        if self.rect.top <= SCROLL_THRESH:
            # если игрок прыгает
            if self.vel_y < 0:
                scroll = -dy  # dy - это скорость перемещения игрока. Поэтому, если он движется вверх, то экран - вниз

        # сбрасываем spring_jump, если игрок на платформе или падает
        if self.vel_y > 0:
            self.spring_jump = False

        # обновление положения рамки (границ игрока)
        self.rect.x += dx
        self.rect.y += dy + scroll  # + scroll, чтобы игрок не перепрыгивал границу прокрутки

        # обновление маски
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x-7, self.rect.y)) # подгоняем рамку под позицию игрока
        #pygame.draw.rect(screen, WHITE, self.rect, 2)  # Рамка, определяющая границы игрока
'''- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'''

# экземпляр игрока
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

# создание группы спрайтов
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
static_enemy_group = pygame.sprite.Group()
spring_group = pygame.sprite.Group()

# создание стартовой платформы
platform = Platform(SCREEN_WIDTH // 2 - 48, SCREEN_HEIGHT - 80, 90, False, False)
platform_group.add(platform)

'''- - - - - - - - - - - - - - - - - - - - - - - - - - - - ИГРОВОЙ ЦИКЛ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -'''
run = True
while run:

    clock.tick(FPS)

    if game_over == False:

        # запускаем возможность перемещения
        scroll = jumpy.move()

        # отрисовка фона
        bg_scroll += scroll
        if bg_scroll >= 800:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # генерация платформ
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(65, 80)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)  # отнимаем ширину платформы, чтобы она не ушла за пределы экрана
            p_y = platform.rect.y - random.randint(80, 120)  #берёт координату предыдущей платформы по у
            p_type = random.randint(1, 3)
            p_dis = False
            p_moving = False
            p_jumping = False

            # добавление исчезновения у некоторых платформ
            if score > 10 and random.randint(0, 1000) > 600:
                p_dis = True

            # генерация пружинки на платформах
            if p_type != 1 and random.randint(0, 1000) > 900 and score > 300:
                temp_spring = Spring(0, 0)
                spring_x = p_x + (p_w // 2) - (temp_spring.image.get_width() // 2)
                spring_y = p_y - temp_spring.image.get_height()
                spring = Spring(spring_x, spring_y)
                spring_group.add(spring)

            if p_type == 1 and score > 500:
                p_moving = True

            else:
                p_moving = False

            platform = Platform(p_x, p_y, p_w, p_moving, p_dis)
            platform_group.add(platform)

            # генерация врагов на платформах
            if len(static_enemy_group) == 0:
                for platform in platform_group:
                    if random.randint(0, 1000) > 800 and score > 600 and not (p_moving):
                        temp_static_enemy = Enemy(0, 0, enemy_images)
                        static_enemy_x = p_x + (p_w // 2) - (temp_static_enemy.image.get_width() // 2)
                        static_enemy_y = p_y - temp_static_enemy.image.get_height()
                        static_enemy = Enemy(static_enemy_x, static_enemy_y, enemy_images)
                        static_enemy_group.add(static_enemy)

        # обновить платформы
        platform_group.update(scroll)
        spring_group.update(scroll)
        static_enemy_group.update(scroll)

        # генерация врагов
        if len(enemy_group) == 0 and score >= 1500:
            enemy_bird = Enemy_bird(SCREEN_WIDTH, 80, bird_sheet, 2.5)
            flying_bird_fx.play()
            enemy_group.add(enemy_bird)

        # обновление врагов
        enemy_group.update(scroll, SCREEN_WIDTH)

        # обновление счёта
        if scroll > 0:
            score += scroll

        # отрисовка черты с рекордом
        pygame.draw.line(screen, WHITE, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
        draw_text('HIGH SCORE', font_small, WHITE, SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH - 20)


        # отрисовка спрайтов
        # группа спрайтов в пайгейм автоматически обновляется, так что не нужно отдельно прописывать метод рисования
        platform_group.draw(screen)
        enemy_group.draw(screen)
        spring_group.draw(screen)
        static_enemy_group.draw(screen)
        jumpy.draw()

        # отрисовка панели с счётом
        draw_panel()

        # проверка завершения игры
        if jumpy.rect.top > SCREEN_HEIGHT: # игрок опустился ниже рамки экрана
            game_over = True
            death_fx.play()


        # проверка столкновений с врагами
        if not jumpy.spring_jump: # проверка на иммунитет в прыжке от пружинки
            if pygame.sprite.spritecollide(jumpy, enemy_group, False): # если прямоугольные рамки столкнутся, то
                if pygame.sprite.spritecollide(jumpy, enemy_group, False, pygame.sprite.collide_mask): # будет проверка на столкновение по маске
                    for enemy_bird in enemy_group:
                        if pygame.sprite.collide_mask(jumpy, enemy_bird):
                            # если игрок прыгает сверху, то он отталкивается
                            if jumpy.rect.bottom < enemy_bird.rect.centery:
                                enemy_bird.kill()
                                death_bird_fx.play()
                                jumpy.vel_y = -25
                                jump_fx.play()
                            # иначе - умирает
                            else:
                                game_over = True
                                death_fx.play()


            if pygame.sprite.spritecollide(jumpy, static_enemy_group, False): # если прямоугольные рамки столкнутся, то
                if pygame.sprite.spritecollide(jumpy, static_enemy_group, False, pygame.sprite.collide_mask): # будет проверка на столкновение по маске
                    for static_enemy in static_enemy_group:
                        if pygame.sprite.collide_mask(jumpy, static_enemy):
                            # если игрок прыгает сверху, то он отталкивается
                            if jumpy.rect.bottom < static_enemy.rect.centery:
                                static_enemy.kill()
                                death_fx.play()
                                jumpy.vel_y = -25
                                jump_fx.play()
                            # иначе - умирает
                            else:
                                game_over = True
                                death_fx.play()

    else:
        #прописываем затухание
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 15
            for y in range(0, 6, 2):
                pygame.draw.rect(screen, BLACK, (0, y*133, fade_counter, SCREEN_HEIGHT/6))  # верхний прямоугольник
                pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - fade_counter, (y+1)*133, SCREEN_WIDTH, SCREEN_HEIGHT/6))  # нижний прямоугольник

        else:
            draw_text('GAME OVER', font_big, WHITE, 185,300)
            draw_text('SCORE: ' + str(score), font_big, WHITE, 185, 350)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_big, WHITE, 60, 400)

            # обновление рекорда
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # сбросить настройки переменных
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                # сбросить врагов
                enemy_group.empty()
                static_enemy_group.empty()
                # изменить положение игрока
                jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                # перезагрузка платформ
                platform_group.empty()
                spring_group.empty()
                # создание стартовой платформы
                platform = Platform(SCREEN_WIDTH // 2 - 48, SCREEN_HEIGHT - 80, 90, False, False)
                platform_group.add(platform)


    for event in pygame.event.get():  # прописываем цикл для перебора всевозможых событий
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # обновление рекорда
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            run = False

    # обновляем изображение в окошке
    pygame.display.update()

pygame.quit()
