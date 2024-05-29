import pygame
import random

'''- - - - - - - - - - - - - - - - - - - - - - - - КЛАСС ПРОТИВНИКА - - - - - - - - - - - - - - - - - - - - - - - '''
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_list):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(image_list)
        self.image = pygame.transform.scale(self.image, (65, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()