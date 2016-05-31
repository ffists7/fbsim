from pygame import Rect, font, Color, Surface, SRCALPHA

class hud:

    def __init__(self, statusBarWidth=100, hpBarHeight=25, spBarHeight=10,
        screenWidth=1024, screenHeight=768, HPBarMaxColor=(50,20,20),
        SPBarMaxColor=(100,100,100), HPBarCurrentColor=(155,20,20),
        SPBarCurrentColor=(200,200,200), eventWindowColor = (20,20,20,200), nameMargin = 10):

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.statusBarWidth = statusBarWidth

        self.HPBarMaxB1Dim = Rect(0,0,self.statusBarWidth,hpBarHeight)
        self.SPBarMaxB1Dim = Rect(0,hpBarHeight,self.statusBarWidth,spBarHeight)
        self.HPBarMaxB2Dim = Rect(self.screenWidth-self.statusBarWidth,0,self.statusBarWidth,hpBarHeight)
        self.SPBarMaxB2Dim = Rect(self.screenWidth-self.statusBarWidth,hpBarHeight,self.statusBarWidth,spBarHeight)

        self.HPBarCurrentB1Dim = Rect(0,0,self.statusBarWidth,hpBarHeight)
        self.SPBarCurrentB1Dim = Rect(0,hpBarHeight,self.statusBarWidth,spBarHeight)
        self.HPBarCurrentB2Dim = Rect(self.screenWidth-self.statusBarWidth,0,self.statusBarWidth,hpBarHeight)
        self.SPBarCurrentB2Dim = Rect(self.screenWidth-self.statusBarWidth,hpBarHeight,self.statusBarWidth,spBarHeight)

        self.HPBarMaxColor = HPBarMaxColor
        self.SPBarMaxColor = SPBarMaxColor
        self.HPBarCurrentColor = HPBarCurrentColor
        self.SPBarCurrentColor = SPBarCurrentColor

        self.nameMargin = nameMargin

        #self.timeDim = Rect(x,y,Width,Height)

        self.eventWindowDim = Rect(0,self.screenHeight/4*3,self.screenWidth,self.screenHeight)
        self.eventWindowSurface = Surface((int(self.screenWidth),int(self.screenHeight/4)), flags=SRCALPHA)
        self.eventWindowSurface.fill(eventWindowColor)
        self.eventWindowSurface.convert_alpha()
        self.eventWindowTextPos = (10,0)
        self.events = []

        self.timeDim = None


        self.eventWindowColor = eventWindowColor #Color(eventWindowColor[0],eventWindowColor[1],eventWindowColor[2],eventWindowColor[3],)

        self.nameFont = font.SysFont("Arial",12)
        self.timeFont = font.SysFont("Arial",20)
        self.roundFont = font.SysFont("Arial",12)
        self.eventWindowFont = font.SysFont("Arial",12)

    def updateHPBars(self, B1HPpercent, B2HPpercent):
        B1HPCurrentWidth = B1HPpercent * self.statusBarWidth
        B2HPCurrentWidth = B2HPpercent * self.statusBarWidth
        self.HPBarCurrentB1Dim.left = self.statusBarWidth-B1HPCurrentWidth
        self.HPBarCurrentB1Dim.width = B1HPCurrentWidth
        self.HPBarCurrentB2Dim.width = B2HPCurrentWidth


    def updateSPBars(self, B1SPpercent, B2SPpercent):
        B1SPCurrentWidth = B1SPpercent * self.statusBarWidth
        B2SPCurrentWidth = B2SPpercent * self.statusBarWidth

        self.SPBarCurrentB1Dim.left = self.statusBarWidth-B1SPCurrentWidth
        self.SPBarCurrentB1Dim.width = B1SPCurrentWidth
        self.SPBarCurrentB2Dim.width = B2SPCurrentWidth
