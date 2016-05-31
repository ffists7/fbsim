'''
Work notes:
10. Edit hit messages to read something like B1's hit landed and did X damage!
12. Max stamina for next round is capped at regen'd e.g if current SP (with regen) is 120 then max sp for nex round is 120
'''

import pygame
from pygame.locals import *
import round
from random import randint
import hud
import roundSplash
import postMatch

class fight:

    def __init__(self, B1, B2):
        self.screen = pygame.display.set_mode((1024,768))

        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        self.background = self.background.convert()

        self.events = []

        self.activeRound = round.round()
        #self.activeRound.setB1(B1)
        #self.activeRound.setB2(B2)
        self.activeRound.B1 = B1
        self.activeRound.B2 = B2
        self.currentRoundNumber = 1
        self.max_rounds = 3
        self.fight_winner = None

        self.message_queue_length = 10

        barWidth = self.screen.get_size()[0]/2 - 50
        self.hud = hud.hud(statusBarWidth=barWidth)

    def __enter__(self):
        return self

    def __exit__(self, *err):
        return




    def input(self):
        event = pygame.event.wait()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                return "CONTINUE"
            if event.key == K_ESCAPE:
                return "QUIT"
        return None



    def updateMessageQueue(self):
        #Manage message queue
        if len(self.events) <= self.message_queue_length:
            self.events.append(self.activeRound.MSGturnResult)
        else:
            self.events.pop(0)
            self.events.append(self.activeRound.MSGturnResult)


    def nextRound(self):
        self.currentRoundNumber = self.currentRoundNumber + 1
        if self.currentRoundNumber <= self.max_rounds and self.activeRound.status != "KO":
            temp1=self.activeRound.B1
            temp2=self.activeRound.B2
            self.activeRound = round.round(self.currentRoundNumber)
            self.activeRound.setB1(temp1.NAME, temp1.AGL, temp1.END,temp1.STR,temp1.INT, temp1.HPmax, temp1.HPcurrent, temp1.SPcurrent, temp1.imgDir)
            self.activeRound.setB2(temp2.NAME, temp2.AGL, temp2.END,temp2.STR,temp2.INT, temp2.HPmax, temp2.HPcurrent, temp2.SPcurrent, temp2.imgDir)
            #Reset event queue
            self.events = []
            self.newRoundSplash(self.currentRoundNumber)

            return "START"
        else:
            if self.activeRound.winner == None:
                self.events.append("Match ended in a draw!")
            else:
                self.events.append(self.activeRound.winner.NAME+" won the match!")
            self.updateMessageQueue()
            return "END"

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
        font = pygame.font.SysFont("Arial", 12)
        text = font.render("Test", True, (255,255,255))

        self.screen.blit(self.background, (0,0))
        #Draw event queue
        self.drawFight()
        self.drawHUD()

        pygame.display.flip()


    def drawFight(self):
        self.screen.blit(self.activeRound.background, (0,0))
        self.screen.blit(self.activeRound.B1.sprites[self.activeRound.B1.currentSpriteKey],(0,0))

    def drawHUD(self):
        self.drawEventWindow()
        self.drawStatusBars()
        self.drawTime()

    def drawTime(self):
        timeRendered = self.hud.timeFont.render(self.activeRound.timestamp(),True , (255,255,255))
        tx = self.hud.screenWidth/2 - timeRendered.get_size()[0]/2
        ty = 2
        self.screen.blit(timeRendered, (tx,ty))

        roundText = "Round "+ str(self.activeRound.round_number)
        roundRendered = self.hud.roundFont.render(roundText, True , (255,255,255))
        rx = self.hud.screenWidth/2 - timeRendered.get_size()[0]/2
        ry = self.hud.HPBarMaxB1Dim.y + self.hud.SPBarMaxB1Dim.y - 2
        self.screen.blit(roundRendered, (rx,ry))


    def drawStatusBars(self):
        B1HPpct = self.activeRound.B1.HPcurrent/self.activeRound.B1.HPmax
        B2HPpct = self.activeRound.B2.HPcurrent/self.activeRound.B2.HPmax
        B1SPpct = self.activeRound.B1.SPcurrent/self.activeRound.B1.SPmax
        B2SPpct = self.activeRound.B2.SPcurrent/self.activeRound.B2.SPmax

        #Update status bar dimeniosns with current values
        self.hud.updateHPBars(B1HPpct,B2HPpct)
        self.hud.updateSPBars(B1SPpct,B2SPpct)

        #Draw status bar backgrounds
        pygame.draw.rect(self.screen,self.hud.HPBarMaxColor, self.hud.HPBarMaxB1Dim)
        pygame.draw.rect(self.screen,self.hud.HPBarMaxColor, self.hud.HPBarMaxB2Dim)
        pygame.draw.rect(self.screen,self.hud.SPBarMaxColor, self.hud.SPBarMaxB1Dim)
        pygame.draw.rect(self.screen,self.hud.SPBarMaxColor, self.hud.SPBarMaxB2Dim)

        #Draw current status bars
        pygame.draw.rect(self.screen,self.hud.HPBarCurrentColor, self.hud.HPBarCurrentB1Dim)
        pygame.draw.rect(self.screen,self.hud.HPBarCurrentColor, self.hud.HPBarCurrentB2Dim)
        pygame.draw.rect(self.screen,self.hud.SPBarCurrentColor, self.hud.SPBarCurrentB1Dim)
        pygame.draw.rect(self.screen,self.hud.SPBarCurrentColor, self.hud.SPBarCurrentB2Dim)

        #Draw names
        B1name = self.hud.nameFont.render(self.activeRound.B1.NAME, True, (255,255,255))
        self.screen.blit(B1name, (0+self.hud.nameMargin,40))

        B2name = self.hud.nameFont.render(self.activeRound.B2.NAME, True, (255,255,255))
        self.screen.blit(B2name, (self.screen.get_size()[0]-B2name.get_size()[0]-self.hud.nameMargin,40))

    def drawEventWindow(self):
        #pygame.draw.rect(self.screen, self.hud.eventWindowColor, self.hud.eventWindowDim)
        self.screen.blit(self.hud.eventWindowSurface, (0,self.hud.screenHeight/4*3))
        if len(self.events) > 0:
            x= self.hud.eventWindowDim.x + 10
            y = self.hud.eventWindowDim.y + 10
            for event in self.events:
                text = self.hud.eventWindowFont.render(event, True, (255,255,255))
                self.screen.blit(text, (x,y))
                y = y + self.hud.eventWindowFont.size(event)[1]


    def newRoundSplash(self, RN=0):
        status = "CONTINUE"
        splash = roundSplash.roundSplash(RN)
        while status != "QUIT":
            status = splash.input()
            splash.draw()


    def postMatchSplash(self):
        status = "CONTINUE"
        splash = postMatch.postMatch(self.activeRound.winner)
        while status != "QUIT":
            status = splash.input()
            splash.draw()

class game:
    game_status = None
    match_status = None
    game = None

    def __init__(self):
        self.game_status = "CONTINUE"

    def __enter__(self):
        return self

    def __exit__(self, *err):
        return

    def main(self,B1,B2):
        self.game = fight(B1,B2)
        self.game.newRoundSplash(self.game.currentRoundNumber)
        self.game.draw()

        while self.game_status != "QUIT":
            self.game_status = self.game.input()
            if self.match_status != "END" and self.game_status == "CONTINUE":
                self.match_status = self.game.update()
                if self.match_status == "CONTINUE":
                    self.game.draw()
            if self.match_status == "END":
                self.fight_winner = self.game.activeRound.winner
                self.game.postMatchSplash()
                self.game_status = "QUIT"
