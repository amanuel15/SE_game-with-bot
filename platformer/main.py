import random
import pygame as pg
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        # initialize game window ...
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption("Template")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.waiting = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE),'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # load sound
        self.snd_dir = path.join(self.dir, 'snd')

    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.paused = False
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(path.join(self.snd_dir, 'Theme Song.wav'))
        self.run()

    def run(self):
        # Game Loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            # sync FPS
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
                self.draw()
            elif self.paused:
                self.show_pause_screen()
        pg.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # Check if player hits a platform and snap to it
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.pos.x < hits[0].rect.right + 5 and \
                    self.player.pos.x > hits[0].rect.left - 5:
                    if self.player.pos.y < hits[0].rect.bottom:
                        self.player.pos.y = hits[0].rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                        #self.player.falling = False

        # Scrolling when player reachs 1/4 of the screen
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if self.player.rect.top <= HEIGHT /4 and not hits:
            self.score += 10
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
        if self.player.rect.bottom >= HEIGHT * 0.92 and not hits:
            self.score -= 5
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)

    def events(self):
        # Game Loop - events
        # Process input(Event)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                if self.score > self.highscore:
                    self.highscore = self.score
                    with open(path.join(self.dir, HS_FILE), 'w') as f:
                        f.write(str(self.highscore))
            if event.type == pg.KEYDOWN:
                k=pg.K_SPACE
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_ESCAPE:
                    self.paused = not  self.paused
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 14, WHITE, WIDTH/2, 5)
        # Double buffer
        pg.display.flip()

    def show_start_screen(self):
        # Game splash/start screen
        self.screen.fill(BG2)
        self.draw_text("High SCore: " + str(self.highscore), 22 , WHITE, WIDTH / 2, 5)
        # buttons play, settings and exit
        self.button("Play", WIDTH / 2 - 75, HEIGHT / 4, 150, 50, BGCOLOR, RED, 75, btn="play")
        self.button("Settings", WIDTH / 2 - 75, HEIGHT / 2, 150, 50, BGCOLOR, RED, 75, btn="settings")
        self.button("Exit", WIDTH / 2 - 75, HEIGHT * 3 / 4, 150, 50, BGCOLOR, RED, 75, btn="exit")
        #self.paused = False
        # animate mouse hover over buttons
        pg.display.flip()
        #self.wait_for_key()

    def show_pause_screen(self):
        while self.paused:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = not  self.paused
            self.screen.fill(BGCOLOR)
            self.button("Resume", WIDTH / 2 - 75, HEIGHT / 4, 150, 50, BLUE, RED, 75, btn="resume")
            self.button("Main menu", WIDTH / 2 - 75, HEIGHT / 2, 150, 50, BLUE, RED, 75, btn="mainMenu")
            self.button("Exit", WIDTH / 2 - 75, HEIGHT * 3 / 4, 150, 50, BLUE, RED, 75, btn="exit")
            pg.display.flip()

    def show_settings_screen(self):
        while self.waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.wait_for_key()
            self.screen.fill(BGCOLOR)
            self.button("Audio", WIDTH / 2 - 75, HEIGHT / 4, 150, 50, BLUE, RED, 75, btn="audio")
            self.button("Key Bindings", WIDTH / 2 - 100, HEIGHT / 2, 200, 50, BLUE, RED, 100, btn="keyBindigs")
            self.button("Difficulty", WIDTH / 2 - 75, HEIGHT * 3 / 4, 150, 50, BLUE, RED, 75, btn="difficulty")
            pg.display.flip()

    def show_audio_screen(self):
        while self.waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.show_settings_screen()
            self.screen.fill(BGCOLOR)
            self.button("ON", WIDTH / 2 - 75, HEIGHT / 4, 150, 50, BLUE, RED, 75, btn="on")
            self.button("OFF", WIDTH / 2 - 75, HEIGHT / 2, 150, 50, BLUE, RED, 75, btn="off")
            pg.display.flip()

    def show_difficulty_screen(self):
        while self.waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.show_settings_screen()
            self.screen.fill(BGCOLOR)
            self.button("Easy", WIDTH / 2 - 75, HEIGHT / 4, 150, 50, BLUE, RED, 75, btn="easy")
            self.button("Hard", WIDTH / 2 - 75, HEIGHT / 2, 150, 50, BLUE, RED, 75, btn="hard")
            pg.display.flip()

    def show_keybindings_screen(self):
        while self.waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.show_settings_screen()
            self.screen.fill(BGCOLOR)
            self.button("Default", WIDTH / 2 - 75, HEIGHT / 4, 150, 50, BLUE, RED, 75, btn="combo")
            pg.display.flip()

    def show_go_screen(self):
        # Game Over/continue
        pass

    def wait_for_key(self):
        self.waiting = True
        while self.waiting:
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.running = False
                    quit()
                self.show_start_screen()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def button(self, text, x, y, width, height, color, hover_color, xOffset, btn = None):
        mousePos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        # adds interactive button features like redirecting and hover
        if x + width > mousePos[0] > x and y + height > mousePos[1] > y:
            pg.draw.rect(self.screen, color,(x, y,width,height))
            if click[0] == 1 and btn != None:
                if btn == "exit":
                    pg.quit()
                    quit()

                if btn == "settings":
                    self.show_settings_screen()

                if btn == "play":
                    self.waiting = False
                    if self.paused:
                        self.paused = False
                        self.new()

                if btn == "mainMenu":
                    self.paused = False
                    self.waiting = True
                    self.wait_for_key()

                if btn == "resume":
                    self.paused = not self.paused

                if btn == "audio":
                    self.show_audio_screen()

                if btn == "difficulty":
                    self.show_difficulty_screen()

                if btn == "off":
                    self.show_settings_screen()

                if btn == "on":
                    self.show_settings_screen()

                if btn == "easy":
                    self.show_settings_screen()

                if btn == "hard":
                    self.show_settings_screen()

        else:
            pg.draw.rect(self.screen, hover_color,(x, y,width,height))
        # place a text onto the buttons
        self.draw_text(text, 36, BLACK, x + xOffset, y)

g = Game()
g.show_start_screen()
while g.running:
    g.wait_for_key()
    g.new()

pg.quit()
