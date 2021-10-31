import random
import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Template")
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
