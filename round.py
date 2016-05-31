import boxer
from random import randint
from pygame import image
from os import path

class round:

    def __init__(self,RN=1):
        self.B1 = None
        self.B2 = None
        self.attackingBoxer = randint(0,1)

        self.MSGturnResult = None
        self.status="START" #START,CONTINUE,END,KO

        self.attacker = None
        self.defender = None
        self.winner = None

        self.turn = 0
        self.round_number = RN


        self.round_duration=120
        self.secondsPerTurn=5
        self.maxRoundTurns=self.round_duration/self.secondsPerTurn

        self.background = image.load(path.join("img","RING.png"))
        self.background.convert()

    def setB1(self,name="Jessica",agl=50, end=50, str=50, int=50, hp=100,hpC=None,spC=None, imgDir="01"):
        self.B1 = boxer.boxer(name,agl, end, str, int, hp, hpC, spC, imgDir)

    def setB2(self,name="Mila",agl=50, end=50, str=50, int=50, hp=100,hpC=None,spC=None, imgDir="02"):
        self.B2 = boxer.boxer(name,agl, end, str, int, hp, hpC, spC, imgDir)


    def flip(self, binary):
        if binary == 0:
            result = 1
        elif binary == 1:
            result = 0
        else:
            #2 indicates error
            result = 2;
        return result

    def roundWinner(self, B1, B2):
        if B1.HPcurrent < B2.HPcurrent:
            return B2
        elif B1.HPcurrent > B2.HPcurrent:
            return B1
        else:
            return None

    def timestamp(self):
        #build a time stamp for the round's current time
        total_seconds =  self.turn * self.secondsPerTurn
        seconds = str(int(total_seconds % 60)).zfill(2)
        minutes = str(int(total_seconds / 60)).zfill(2)
        timestamp = minutes + ":" + seconds
        return timestamp

    def MSGhit(self, B1,B2, dam):
        return "["+self.timestamp()+"] "+ B1.NAME + " " + B1.currentATTACK +"s " + B1.currentATTACK_TARGET + " and connects with " +B2.NAME+" for "+ str(dam) +" damage!"

    def MSGhitBlocked(self, B1,B2, dam):
        return "["+self.timestamp()+"] "+ B1.NAME+ " " + B1.currentATTACK +"s " + B1.currentATTACK_TARGET + " but " +B2.NAME+" blocks! Hit does "+ str(dam) +" damage!"

    def MSGdodge(self, B1,B2):
        return "["+self.timestamp()+"] "+B1.NAME+" dodged "+ B2.NAME+"'s attack!"

    def nextTurn(self):
        '''
        Used by game logic to advance next turn.
        '''
        attacker = None
        defender = None

        if self.status == "START":
            self.startRound()
            return
        if self.status == "CONTINUE":
            if self.attackingBoxer == 0:
                attacker = self.B1
                defender = self.B2
            else:
                attacker = self.B2
                defender = self.B1

            #STAMINA REGEN PHASE
            attacker.FIGHTrechargeSP()

            #ATTACK PHASE
            attacker.selectAttack()
            attacker.selectAttackTarget()
            attacker.setAttackSpriteKey()
            defender.selectDefense()
            defender.setDefenseSpriteKey()

            dodge_succeed = False
            #attack logic
            if defender.currentDEFENSE == "DODGE":
                #roll for DODGE
                dodge_succeed = defender.FIGHTdodgeSuccess(attacker.AGL)
                self.MSGturnResult =  self.MSGdodge(defender,attacker)

            if not dodge_succeed:
                dam = 0
                if defender.currentDEFENSE == attacker.currentATTACK_TARGET:
                    #calculate penalized damage
                    dam = attacker.FIGHThitPower(0.5)
                    self.MSGturnResult =  self.MSGhitBlocked(attacker,defender, dam)
                else:
                    dam = attacker.FIGHThitPower()
                    self.MSGturnResult =  self.MSGhit(attacker,defender, dam)
                    #calculate full damage
                defender.FIGHTreceiveATTACK(dam)

            self.attackingBoxer = self.flip(self.attackingBoxer)

            #ROUND CHECK PHASE
            roundEnd = self.roundStatusCheck()

            if roundEnd:
                self.endRound()
            else:
                self.turn = self.turn + 1


    def startRound(self):
        startMessage = "Round "+str(self.round_number)+"! Fight!"
        self.status = "CONTINUE"
        self.B1.PREFIGHTregenStamina(15)
        self.B2.PREFIGHTregenStamina(15)
        self.MSGturnResult = startMessage

    def endRound(self):
        self.status = "END"
        #refill stamina


        self.winner = self.roundWinner(self.B1,self.B2)
        if self.winner.NAME != None:
            if self.B1.HPcurrent <= 0 or self.B2.HPcurrent <= 0:
                endMessage = "Round "+str(self.round_number)+" over! " + self.winner.NAME + " won by KO!"
                self.status = "KO"
            else:
                endMessage = "Round "+str(self.round_number)+" over! " + self.winner.NAME + " wins!"
        else:
            endMessage = "Round "+str(self.round_number)+" over! Round ended in a tie!"
        self.MSGturnResult = endMessage



    def roundStatusCheck(self):
        #Check round conditions to indicate if round ends.
        #Round ends if time runs out or someone is KO'd.
        timeUp = False
        boxer_KO = False

        if self.turn >= self.maxRoundTurns:
            timeUp = True
        if self.B1.HPcurrent <= 0 or self.B2.HPcurrent <= 0:
            boxer_KO = True

        if timeUp or boxer_KO:
            return True
        else:
            return False

'''
Sample driver code

r1 = round()

while r1.turn <= r1.maxRoundTurns and r1.B1.HPcurrent != 0 and r1.B2.HPcurrent != 0:
    r1.nextTurn()

    if r1.B1.HPcurrent != 0 or r1.B2.HPcurrent != 0:
        #round end
'''
