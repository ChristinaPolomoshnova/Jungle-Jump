import pygame
from pygame import mixer  # для музыки

# Инициализация библиотеки
pygame.init()
mixer.init()

# задаём размеры экрана, чтобы не было рамок, можно прописать flags = pygame.NOFRAME
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 800

# устанавливаем частоту кадров
clock = pygame.time.Clock()
FPS = 60

# игровые переменные
SCROLL_THRESH = 200  # порог прокрутки
GRAVITY = 1
MAX_PLATFORMS = 10
scroll = 0  # определяет, насколько сдвинется экран
bg_scroll = 0
game_over = False
score = 0
fade_counter = 0 # счётчик затухания

# определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (116, 157, 127)

# загрузка музыки и звуков
pygame.mixer.music.load('Assets/music.mp3')
pygame.mixer.music.set_volume(0.6)  # громкость в процентном соотношении от исходой
pygame.mixer.music.play(-1, 0.0) # чтобы музыка играла бесконечно прописываем -1

jump_fx = pygame.mixer.Sound('Assets/jump.mp3')
jump_fx.set_volume(0.5)

death_fx = pygame.mixer.Sound('Assets/death.mp3')
death_fx.set_volume(0.5)

death_bird_fx = pygame.mixer.Sound('Assets/bird_death.mp3')
death_bird_fx.set_volume(0.5)

flying_bird_fx = pygame.mixer.Sound('Assets/flying_bird.mp3')
flying_bird_fx.set_volume(0.5)

spring_fx = pygame.mixer.Sound('Assets/spring.mp3')
spring_fx.set_volume(0.5)
