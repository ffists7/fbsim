import pygame
from os import path
from pygame.locals import *
from random import randint

class roundSplash:
    def __init__(self, RN = 1):
        self.screen = pygame.display.set_mode((1024,768))

        self.background = pygame.image.load(path.join("img","ROUND.png"))
        self.background = self.background.convert()

        self.roundNumber = RN
        self.FONTroundNumber = pygame.font.SysFont("Arial",100, True)
        self.RNx = self.screen.get_size()[0]/2 - 8
        self.RNy = 60

        self.message = "Press SPACE to continue."
        self.FONTmessage = pygame.font.SysFont("Arial",18, True)
        self.Mx = self.screen.get_size()[0]/2
        self.My = self.screen.get_size()[1] - 25

    def input(self):
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                return "QUIT"
        return None



    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.drawRoundNumber()
        self.drawMessage()
        pygame.display.flip()


    def drawRoundNumber(self):
        text = self.FONTroundNumber.render(str(self.roundNumber), True, (50,50,50))
        x = text.get_width() / 2
        self.screen.blit(text, (self.RNx - x,self.RNy))

    def drawMessage(self):
        text = self.FONTmessage.render(self.message, True, (255,255,255))
        x = self.Mx - text.get_width()/2
        y = self.My - text.get_height()
        self.screen.blit(text, (x,y))


def main():
    status = "CONTINUE"
    pygame.init()
    splash = roundSplash(1)
    while status != "QUIT":
        status = splash.input()
        splash.draw()

if __name__ == '__main__':
    main()
