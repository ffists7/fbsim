from pygame import display, image, Surface, draw, event, font, Rect
from pygame.locals import *
from os import path
from random import randint
import boxer
import fight

class select:
    def __init__(self, RN = 1):
        self.screen = display.set_mode((1024,768))

        self.background = Surface((self.screen.get_width(), self.screen.get_height()))
        self.background.fill((0,0,100))
        self.background = self.background.convert()

        self.B1 = None
        self.B2 = None
        self.B3 = None
        self.B4 = None

        self.B1headshot = None
        self.B2headshot = None
        self.B3headshot = None
        self.B4headshot = None



        self.boxers = [self.B1, self.B2,self.B3,self.B4]
        self.headshots = [self.B1headshot,self.B2headshot,self.B3,self.B4]

        self.COLORcharBoxInactive  = (100,100,100)
        self.COLORselectionBox = (0,100,0)

        self.index=0

        self.B1selection=None
        self.B2selection=None

        self.FONTname = font.SysFont("Arial",48, True)
        self.FONTstats = font.SysFont("Arial",24, True)

        self.loadBoxers()

    def input(self):
        evt = event.wait()
        if evt.type == KEYDOWN:
            if evt.key == K_SPACE:
                return "SEL"
            if evt.key == K_LEFT:
                return "LEFT"
            if evt.key == K_RIGHT:
                return "RIGHT"
            if evt.key == K_ESCAPE:
                return "QUIT"
        return None

    def loadBoxers(self):
        with open("boxers") as boxers:
            for i in (1,2,3,4):
                line = boxers.readline()
                delim = ","
                attr = line.split(delim)
                dir = attr[6][:-1]
                self.boxers[i-1] = boxer.boxer(name=attr[0],agl=int(attr[1]),end=int(attr[2]),str=int(attr[3]),int=int(attr[4]),hp=int(attr[5]),imgDir = dir)

                self.headshots[i-1] = image.load(path.join("img","boxers",dir,"SEL_H.png"))
                self.headshots[i-1].convert()


    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.drawCharacterBoxes()
        self.drawName()
        self.drawStats()
        display.flip()

    def update(self, status):
          if status == "LEFT":
              self.moveIndex(-1)
              return "LEFT"
          if status == "RIGHT":
              self.moveIndex(1)
              return "RIGHT"
          if status == "SEL":
            if self.B1selection == None:
                self.B1selection = self.index
                self.COLORselectionBox = (100,0,0)
                self.moveIndex(1)
                return "SEL"
            else:
                self.B2selection = self.index
                return "QUIT"

    def moveIndex(self, amount):
        new_index = self.index + amount

        if new_index == self.B1selection and amount < 0:
            new_index = new_index - 1
        elif new_index == self.B1selection and amount > 0:
            new_index = new_index + 1

        if new_index < 0:
            self.index = 3
        elif new_index > 3:
            self.index = 0
        else:
            self.index = new_index



    def drawCharacterBoxes(self):
        width = 201
        margin = 44
        x = margin
        for z in (1,2,3,4):
            y = self.screen.get_height() - width - margin
            self.screen.blit(self.headshots[z-1], (x,y))
            draw.rect(self.background, self.COLORcharBoxInactive,Rect(x,y,width,width),5)
            x = x + width + margin

        x = margin *(self.index + 1) + self.index * width
        draw.rect(self.background, self.COLORselectionBox,Rect(x,y,width,width),5)
        if self.B1selection != None:
            x = margin *(self.B1selection + 1) + self.B1selection * width
            draw.rect(self.background, (0,100,0),Rect(x,y,width,width),5)
        if self.B2selection != None:
            x = margin *(self.B2selection + 1) + self.B2selection * width
            draw.rect(self.background, (100,0,0),Rect(x,y,width,width),5)


    def drawName(self):
        text = self.FONTname.render(self.boxers[self.index].NAME, True, (255,255,255))
        x = self.screen.get_width()/2 - text.get_width()/2
        y = 44
        self.screen.blit(text, (x,y))

    def drawStats(self):
        color = (255,255,255)
        labels=[self.FONTstats.render("AGL", True, color),
                self.FONTstats.render("END", True, color),
                self.FONTstats.render("STR", True, color),
                self.FONTstats.render("INT", True, color),
                self.FONTstats.render("HP", True, color)]



        agl = str(self.boxers[self.index].AGL)
        end = str(self.boxers[self.index].END)
        strength = str(self.boxers[self.index].STR)
        int = str(self.boxers[self.index].INT)
        hp  = str(self.boxers[self.index].HPmax)

        stats=[self.FONTstats.render(agl, True, color),
                self.FONTstats.render(end, True, color),
                self.FONTstats.render(strength, True, color),
                self.FONTstats.render(int, True, color),
                self.FONTstats.render(hp, True, color)]

        x = self.screen.get_width()/2 - labels[0].get_width()
        y = 144 #44
        x_stat = x + labels[0].get_width() + 15
        margin = labels[0].get_height()+ 10
        for i in (0,1,2,3,4):
            self.screen.blit(labels[i], (x,y))
            self.screen.blit(stats[i],(x_stat,y))
            y = y + margin



    def main(self):
        status = "CONTINUE"
        #init()
        prog = select()
        prog.draw()
        while status != "QUIT":
            status = prog.input()
            status = prog.update(status)
            prog.draw()
        return prog.boxers[prog.B1selection], prog.boxers[prog.B2selection]

if __name__ == '__main__':
    main()
