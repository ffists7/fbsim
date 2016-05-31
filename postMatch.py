from pygame import display, image, font, event
from os import path
from pygame.locals import *
from random import randint

class postMatch:
    def __init__(self, winner):
        #self.screen = pygame.display.set_mode((1024,768))
        #self.background = pygame.image.load(path.join("img","RING.png"))
        self.screen = display.set_mode((1024,768))
        self.background = image.load(path.join("img","RING.png"))
        self.background = self.background.convert()
        self.winner = winner.sprite_win
        self.winner = self.winner.convert_alpha()

        self.message = winner.NAME+" wins!"
        #self.FONTmessage = pygame.font.SysFont("Arial",72, True)
        self.FONTmessage = font.SysFont("Arial",72, True)
        self.Mx = self.screen.get_size()[0]/2
        self.My = self.screen.get_size()[1]/2

    def input(self):
        #event = pygame.event.wait()
        evt = event.wait()
        if evt.type == KEYDOWN:
            if evt.key == K_SPACE:
                return "QUIT"
        return None



    def update(self):
        status = None
        if self.activeRound.status != "END" and self.activeRound.status !="KO":
            self.activeRound.nextTurn()
            self.updateMessageQueue()
            status = "CONTINUE"
        else:
            status = self.nextRound()
        return status


    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.winner, (0,0))
        self.drawMessage()
        #pygame.display.flip()
        display.flip()


    def drawMessage(self):
        text = self.FONTmessage.render(self.message, True, (255,255,255))
        x = self.Mx - text.get_width()/2
        y = self.My - text.get_height()
        self.screen.blit(text, (x,y))




def main():
    status = "CONTINUE"
    #pygame.init()
    splash = postMatch(1)
    while status != "QUIT":
        status = splash.input()
        splash.draw()

if __name__ == '__main__':
    main()
