from math import floor, ceil
from random import randint, uniform
from pygame import image
from os import path

class boxer:
    def __init__(self, name="Jessica",agl=0, end=0, str=0, int=0, hp=0, hpC=None, strC=None, imgDir="01"):
            self.NAME=name

            if agl <= 100:
                self.AGL=agl
            else:
                self.AGL=100
            self.END=5
            self.STR=str
            self.INT=int

            self.HPmax=hp
            if hpC == None:
                self.HPcurrent=self.HPmax
            else:
                self.HPcurrent=hpC

            self.SPmax=str
            if strC == None:
                self.SPcurrent = self.SPmax
            else:
                self.SPcurrent=strC

            self.SPrechargeRate=floor(self.END/10)

            self.currentATTACK_TARGET = "None"
            self.currentATTACK="None"
            self.currentDEFENSE="None"

            self.imgDir = imgDir

            self.sprite_n= image.load(path.join("img","boxers", self.imgDir,"NEUTRAL.png"))
            self.sprite_jh= image.load(path.join("img","boxers", self.imgDir,"JAB_HIGH.png"))
            self.sprite_jl= image.load(path.join("img","boxers", self.imgDir,"JAB_LOW.png"))
            self.sprite_hh= image.load(path.join("img","boxers", self.imgDir,"HOOK_HIGH.png"))
            self.sprite_hl= image.load(path.join("img","boxers", self.imgDir,"HOOK_LOW.png"))
            self.sprite_ul= image.load(path.join("img","boxers", self.imgDir,"UPPER_LOW.png"))
            self.sprite_uh= image.load(path.join("img","boxers", self.imgDir,"UPPER_HIGH.png"))
            self.sprite_d= image.load(path.join("img","boxers", self.imgDir,"DODGE.png"))
            self.sprite_bh= image.load(path.join("img","boxers", self.imgDir,"BLOCK_HIGH.png"))
            self.sprite_bl= image.load(path.join("img","boxers", self.imgDir,"BLOCK_LOW.png"))
            self.sprite_win= image.load(path.join("img","boxers", self.imgDir,"WIN.png"))

            self.sprites={"N": self.sprite_n,
                          "JH":self.sprite_jh,
                          "JL":self.sprite_jl,
                          "HH":self.sprite_hh,
                          "HL":self.sprite_hl,
                          "UL":self.sprite_ul,
                          "UH":self.sprite_uh,
                          "D":self.sprite_d,
                          "BH":self.sprite_bh,
                          "BL":self.sprite_bl,
                          "W":self.sprite_win}
            self.currentSpriteKey = "N"

            #self.activeSprite = None

    def PREFIGHTregenStamina(self, stamina_override = 0):
        new_stamina = 0

        if stamina_override == 0:
            new_stamina = self.SPcurrent + self.SPrechargeRate
        else:
            new_stamina = self.SPcurrent + stamina_override
        if new_stamina < self.SPmax:
            self.SPcurrent = new_stamina
        else:
            self.SPcurrent = self.SPmax
        return


    def FIGHTnumberOfHits(self):
        return

    def FIGHThitPower(self, blockMultiplier = 1.0):
        dmgHP = ceil(uniform(0.5,1.1)*self.STR/4)
        attackMultiplier = 1
        targetMultiplier = 1

        if self.currentATTACK_TARGET == "HIGH":
            targetMultiplier = 1.25

        #apply attack multiplier
        if self.currentATTACK == "UPPERCUT":
            attackMultiplier = uniform(0.95,1.1)
        if self.currentATTACK == "JAB":
            attackMultiplier = uniform(0.85,1)
        if self.currentATTACK == "HOOK":
            attackMultiplier = uniform(0.75,0.95)

        #apply block multipliers
        dmgHP = dmgHP * blockMultiplier * attackMultiplier * targetMultiplier
        return ceil(dmgHP)

    def FIGHTdodgeSuccess(self, opponentAGL):
        '''Calculate whether or not dodge succeeds'''
        '''Future iterations will actually account for opponentAGL when calculating hit chance'''
        AGL_differntial = self.AGL - opponentAGL

        if AGL_differntial > 0:
        #AGL favors defender
            draw = randint(0,self.AGL)
            if draw > opponentAGL:
                return True
            else:
                return False
        elif AGL_differntial == 0:
        #equal AGL
            draw = randint(0,1)
            if draw == 0:
                return True
            else:
                return False
        else:
        #AGL favors attacker
            draw = randint(0, opponentAGL)
            if draw < self.AGL:
                self.currentSpriteKey = "D"
                return True
            else:
                self.currentSpriteKey = "N"
                return False



    def decreaseHP(self,attackPWR):
        newHP = self.HPcurrent - attackPWR
        if newHP > 0:
            self.HPcurrent = newHP
        else:
            self.HPcurrent = 0

    def FIGHTreceiveATTACK(self, attackPWR):
        #this is the fucntion that round should call to calculate damages
        if self.SPcurrent > 0:
            newSP = self.SPcurrent - attackPWR

            if newSP > 0:
                self.SPcurrent = newSP
            else:
                self.SPcurrent = 0
                #use remainder of HP damage to decrease HP
                self.decreaseHP(-newSP)
        else:
            self.decreaseHP(attackPWR)

    def FIGHTrechargeSP(self):
        if self.SPcurrent < self.SPmax:
            newSP =  self.SPcurrent + self.SPrechargeRate
            if newSP < self.SPmax:
                self.SPcurrent = newSP
            else:
                self.SPcurrent = self.SPmax

    def rechargeHP(self):
        return


    def setAttackSpriteKey(self):
        if self.currentATTACK_TARGET == "LOW":
           if self.currentATTACK == "UPPERCUT":
               self.currentSpriteKey = "UL"
           elif self.currentATTACK == "JAB":
               self.currentSpriteKey = "JL"
           elif self.currentATTACK == "HOOK":
               self.currentSpriteKey = "HL"
        else:
          if self.currentATTACK == "UPPERCUT":
              self.currentSpriteKey = "UH"
          elif self.currentATTACK == "JAB":
              self.currentSpriteKey = "JH"
          elif self.currentATTACK == "HOOK":
              self.currentSpriteKey = "HH"


    def setDefenseSpriteKey(self):
        if self.currentDEFENSE == "DODGE":
            self.currentSpriteKey = "D"
        elif self.currentDEFENSE == "LOW":
            self.currentSpriteKey = "BL"
        elif self.currentDEFENSE == "HIGH":
            self.currentSpriteKey = "BH"


    def selectAttackTarget(self):
        selection = randint(0,1)
        if selection == 0:
            self.currentATTACK_TARGET = "LOW"
        elif selection == 1:
            self.currentATTACK_TARGET = "HIGH"

    def selectAttack(self):
        selection = randint(0,2)
        if selection == 0:
            self.currentATTACK = "UPPERCUT"
        elif selection == 1:
            self.currentATTACK = "JAB"
        elif selection == 2:
            self.currentATTACK = "HOOK"

    def selectDefense(self):
        selection = randint(0,2)
        if selection == 0:
            self.currentDEFENSE = "LOW"
        elif selection == 1:
            self.currentDEFENSE = "HIGH"
        elif selection == 2:
            self.currentDEFENSE = "DODGE"
