from os import path

# Settings / options
WIDTH = 600
HEIGHT = 400
FPS = 60
TITLE = "plat"
FONT_NAME = "arial"
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet.png"
SETTINGS_FILE = "config.txt"

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 15

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50,HEIGHT * 3 / 4, 100, 20),
                 (125, HEIGHT - 350, 100, 20),
                 (350, 200, 100, 20),
                 (400, 0, 100, 20),
                 (200, -200, 100, 20),
                 (0, -400, 100, 20),
                 (250, -550, 100, 20),
                 (400, -450, 100, 20)]

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (0, 155, 155)
BGCOLOR = LIGHTBLUE
COLORKEY = (0,128,128)
BG2 = (97,95,84)

class changeSettings:
    def __init__(self):
        self.settingsList = []
        self.read()

    def read(self):
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, SETTINGS_FILE),'r') as f:
            self.file = f.readlines()
            for lines in self.file:
                startIndex = lines.find('<')
                endIndex = lines.find('>')
                if startIndex != -1:
                    self.settingsList.append(lines[startIndex+1:endIndex])

    def chooseBindings(self, option = 1):
        bindings = []
        if option == 1:
            start = 1
            while start <= 3:
                bindings.append(self.settingsList[start])
                start += 1
        if option == 2:
            start = int(self.settingsList[0]) + 1
            while start <= 6:
                bindings.append(self.settingsList[start])
                start += 1
        if option == 3:
            start = int(self.settingsList[0]) * 2 + 1
            while start <= 9:
                bindings.append(self.settingsList[start])
                start += 1
        return bindings


c = changeSettings()
print(c.chooseBindings(2))
