from pygame import display, image, event, init
from pygame.locals import *
import round
from random import randint
import hud
from os import path
import menuList
import select
import fight

class mainMenu:
    screen = None
    background = None
    mlist = None

    def __init__(self):
        init()
        self.screen = display.set_mode((1024,768))
        self.background = image.load(path.join("img","MENU.png"))
        self.background.convert()

        self.mlist = menuList.menuList(x = self.screen.get_size()[0]/2,
                                        y = self.screen.get_size()[1]/2,
                                        margin_y = 10)
        self.mlist.addMenuItem("New Fight")
        self.mlist.addMenuItem("Quit")
        self.mlist.setActive(self.mlist.currentIndex)

    def update(self, status):
        if status == "UP":
            self.mlist.cycleUp()
            return
        if status == "DOWN":
            # Move cursor down
            self.mlist.cycleDown()
            return
        if status == "SEL":
            selection =  self.mlist.items[self.mlist.currentIndex].text
            if selection == "Quit":
                return "QUIT"
            if selection == "New Fight":
                return "NEW"
        return

    def draw(self):
        self.screen.blit(self.background,(0,0))
        y = self.mlist.y
        for item in self.mlist.items:
            x = self.mlist.x - item.rendered.get_size()[0]/2
            self.screen.blit(item.rendered, (x,y))
            y = y + self.mlist.margin_y + item.rendered.get_size()[1]
        display.flip()
        return

    def input(self):
        evt = event.wait()
        if evt.type == KEYDOWN:
            if evt.key == K_SPACE:
                return "SEL"
            if evt.key == K_ESCAPE:
                return "QUIT"
            if evt.key == K_DOWN:
                return "DOWN"
            if evt.key == K_UP:
                return "UP"
        return None




def main():
    menu_status = "CONTINUE"
    menu = mainMenu()

    while menu_status != "QUIT":
        menu_status = menu.input()
        menu_status = menu.update(menu_status)
        if menu_status == "NEW":
                selection = select.select()
                B1, B2 = selection.main()
                active = fight.game()
                active.main(B1,B2)
        menu.draw()


if __name__ == '__main__':
    main()
