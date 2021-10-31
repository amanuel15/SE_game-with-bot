import random
import pygame
import os

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"res/images")

font_name = pygame.font.match_font("Arial Black")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"normal.png"))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speedX = 0
        self.speedY = 0

    def update(self):
        self.speedX = 0
        self.speedY = 0
        keyStat = pygame.key.get_pressed()

        # Movement handling
        if keyStat[pygame.K_w]:
            self.speedY -= 3
            if keyStat[pygame.K_CAPSLOCK]:
                self.speedY *= 2
        if keyStat[pygame.K_s]:
            self.speedY += 3
            if keyStat[pygame.K_CAPSLOCK]:
                self.speedY *= 2
        if keyStat[pygame.K_a]:
            self.speedX -= 3
            if keyStat[pygame.K_CAPSLOCK]:
                self.speedX *= 2
        if keyStat[pygame.K_d]:
            self.speedX += 3
            if keyStat[pygame.K_CAPSLOCK]:
                self.speedX *= 2


        # Screen boundaries collision
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        self.rect.x += self.speedX
        self.rect.y += self.speedY

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:
    # sync FPS
    clock.tick(FPS)
    # Process input(Event)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #update
    all_sprites.update()

    #render / draw
    screen.fill(BLUE)
    all_sprites.draw(screen)


    draw_text(screen,str(clock), 18, WIDTH/2,5)

    #AFTER drawing everything
    pygame.display.flip()


pygame.quit()
