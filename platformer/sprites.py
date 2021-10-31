# Sprite classes for game
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    # class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width , height):
        # grab on image out of a spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x, y, width, height))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.falling = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.double = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(11,20,40,72),
                                self.game.spritesheet.get_image(289,20,40,72)]
        # remove the color key / image background
        for frame in self.standing_frames:
            frame.set_colorkey(COLORKEY)
        self.walk_frames_r = [self.game.spritesheet.get_image(8,107,49,63),
                              self.game.spritesheet.get_image(81,107,49,63),
                              self.game.spritesheet.get_image(152,107,49,63),
                              self.game.spritesheet.get_image(219,107,49,63),
                              self.game.spritesheet.get_image(287,107,49,63),
                              self.game.spritesheet.get_image(348,107,49,63)]
        self.walk_frames_l = []
        # Flip the walk left animations
        for frame in self.walk_frames_r:
            frame.set_colorkey(COLORKEY)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame_r = self.game.spritesheet.get_image(202,181,38,80)
        self.jump_frame_r.set_colorkey(COLORKEY)
        self.jump_frame_l = pg.transform.flip(self.jump_frame_r, True, False)
        self.jump_frame_l.set_colorkey(COLORKEY)
        self.fall_frame_r = self.game.spritesheet.get_image(347,176,51,82)
        self.fall_frame_r.set_colorkey(COLORKEY)
        self.fall_frame_l = pg.transform.flip(self.fall_frame_r, True, False)
        self.fall_frame_l.set_colorkey(COLORKEY)

    def jump(self):
        # Jump from platforms only
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -=1
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -PLAYER_JUMP
            self.double = 2
        if self.double > 0:
            self.vel.y = -PLAYER_JUMP
            self.double -= 1

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # equation of motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.4:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # boundery of screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

    def animate(self):
        # handle animation of characters
        if self.vel.y > 0:
            self.falling = True
        if self.vel.y <= 0:
            self.falling = False
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 800:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # walking animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        # jumping animation
        if self.jumping and not self.falling:
            bottom = self.rect.bottom
            if self.vel.x > 0:
                self.image = self.jump_frame_r
            else:
                self.image = self.jump_frame_l
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        # falling animation
        if self.falling:
            bottom = self.rect.bottom
            if self.vel.x > 0:
                self.image = self.fall_frame_r
            else:
                self.image = self.fall_frame_l
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
        print(self.vel.y)

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
