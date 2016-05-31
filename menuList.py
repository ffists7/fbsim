from pygame import image, font, Surface
from os import path
import menuItem

class menuList:
    cursor = None

    def __init__(self, activeColor = (255,0,0), inactiveColor = (225,225,15),
                    x = 0, y = 0, margin_y = 0):
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.itemFont = font.SysFont("Arial",24, True)

        #These coordinates represent the CENTER TOP of a box surrounding the items
        self.x = x
        self.y = y

        self.items = []
        self.currentIndex = 0


        #Margin between menu items
        self.margin_y = margin_y
        return

    def setCursor(self,imgPath):
        if path.isfile(imgPath):
            self.cursor = image.load(imgPath)
            self.cursor.convert()
        return

    def addMenuItem(self, text):
        if isinstance(text, basestring):
            rendered = self.itemFont.render(text, True, self.inactiveColor)
            i = menuItem.menuItem(text,rendered)
            self.items.append(i)
        return

    def cycleUp(self):
        futureIndex = self.currentIndex - 1
        self.setInactive(self.currentIndex)
        if futureIndex < 0:
            self.currentIndex = len(self.items) - 1
        else:
            self.currentIndex = futureIndex
        self.setActive(self.currentIndex)

    def cycleDown(self):
        futureIndex = self.currentIndex + 1
        self.setInactive(self.currentIndex)
        if futureIndex > len(self.items) - 1:
            self.currentIndex = 0
        else:
            self.currentIndex = futureIndex
        self.setActive(self.currentIndex)

    def setInactive(self, index):
        target = self.items[index]
        target.rendered = rendered = self.itemFont.render(target.text, True, self.inactiveColor)

    def setActive(self, index):
        target = self.items[index]
        target.rendered = rendered = self.itemFont.render(target.text, True, self.activeColor)
