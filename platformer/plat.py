import random
import pygame

from settings import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

running = True
while running:
    # sync FPS
    clock.tick(FPS)
    # Process input(Event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update

    #render / draw
    screen.fill(BLACK)
    #AFTER drawing everything
    pygame.display.flip()

pygame.quit()
