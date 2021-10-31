import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

class Constants:

    BOARD_WIDTH = 300
    BOARD_HEIGHT = 300
    DELAY = 100
    DOT_SIZE = 10
    MAX_RAND_POS = 27

class Board(Canvas):
    def __init__(self):
        super().__init__(width=Constants.BOARD_WIDTH, height=Constants.BOARD_HEIGHT,
            background="white", highlightthickness=0)

        self.initGame()
        self.pack()

    def initGame(self):
        self.x=50
        self.y=50
        self.fx=10
        self.fy=10
        self.doDrawing()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Constants.DELAY, self.onTimer)

    def doDrawing(self):
        '''self.create_text(30, 10, text="Score: {0}".format(self.score),
                         tag="score", fill="white")'''
        self.create_rectangle(80,80,self.x,self.y, fill = "red")

    def onKeyPressed(self, e):
        '''controls direction variables with cursor keys'''

        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY:
            self.x -= self.fx

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY:
            self.x += self.fx

        UP_CURSOR_KEY = "Up"
        if key == UP_CURSOR_KEY:
            self.y -= self.fy

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY:
            self.y += self.fy

    def onTimer(self):
        '''creates a game cycle each timer event '''
        self.doDrawing()
        self.after(Constants.DELAY, self.onTimer)


class Ball(Frame):

    def __init__(self):
        super().__init__()

        self.master.title('Snake')
        self.board = Board()
        self.pack()


def main():

    root = Tk()
    nib = Ball()
    root.mainloop()


if __name__ == '__main__':
    main()
