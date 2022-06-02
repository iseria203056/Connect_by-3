import copy
from time import sleep 
import numpy as np
'''
 /////////////////////////////////// 
     // CS4386 Semester B, 2021-2022 
     // Assignment 1 
     // Name: Wong Chi Ho 
     // Student ID: 55703476  
     ///////////////////////////////////
'''
class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.count = 0
        self.score=0
        self.targetDepth=3



        
    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name
    def get_isAI(self):
        return self.isAI
    def get_symbole(self):
        return self.symbole
    def get_score(self):
        return self.score
    def add_score(self,score):
    	self.score+=score
    
    def empty_cells(self,state):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell is None:
                    cells.append([x, y])

        return cells

    def checkscore(self,state,step,minMix): # get the score of  such action
        sX=step[0]
        sY=step[1]
        state[sX][sY]=self.symbole
        count=0
        gain=0

        for x in state[sX][sY:]:
            if x is not None:
                count+=1
            else:
                break

        for x in state[sX][sY::-1]:
            if x is not None:
                count+=1
            else:
                break
        count-=1
        if count == 3:
            gain+=3
        elif count == 6:
            gain+=6
        count =0
        for y in state[sX:]:
            if y[sY] is not None:
                count+=1
            else:
                break
        for y in state[sX::-1]:
            if y[sY] is not None:
                count+=1
            else:
                break
        count-=1
        if count == 3:
            gain+=3
        elif count==6:
            gain+=6
        state[sX][sY]=None
        return minMix*gain
        
    def minimax(self,state,maxTurn,depth,score): #get min max action
        bestScore = None
        count=0
        step=[]
        seq=[]


        if depth == self.targetDepth:           #target depth
            for x, row in enumerate(state):
                for y, cell in enumerate(row):
                    if cell is None:
                        stepScore = self.checkscore(state,[x,y],maxTurn)
                        #print("locate",x,y,"score ",stepScore ,"depth : ",depth)
                        
                        if maxTurn == 1:
                            if bestScore is None or bestScore<stepScore:
                                bestScore=stepScore
                                count=1
                                step=[[x,y]]
                        
                            elif bestScore == stepScore:
                                count+=1
                                step.append([x,y])

                        else:
                            if bestScore is None or bestScore>stepScore:
                                bestScore=stepScore
                                count=1
                                step=[[x,y]]
                            elif bestScore == stepScore:
                                count+=1
                                step.append([x,y])

            return {"score":bestScore,"number":count,"move":step}
            # recurtion in not target depth
        for x, row in enumerate(state):    # loop in the game board   
            for y, cell in enumerate(row):
                if cell is None:
                    stepScore = self.checkscore(state,[x,y],maxTurn)
                    subState=copy.deepcopy(state)
                    subState[x][y]='O'
                    subset=self.minimax(subState,maxTurn*-1,depth+1,stepScore)
                    if subset["score"] is not None:
                        stepScore+=subset["score"]
                    
                    #print("locate",x,y,"score ",stepScore ,"depth : ",depth)
                    if maxTurn == 1:
                        if bestScore is None or bestScore<stepScore: # update best action with better action
                            bestScore=stepScore
                            count=1
                            step=[[x,y]]
                            seq=[subset['number']]
                        elif bestScore == stepScore:                 # update best action with same action
                            count+=1
                            step.append([x,y])
                            seq.append(subset['number'])
                    else:
                        if bestScore is None or bestScore>stepScore:
                            bestScore=stepScore
                            count=1
                            step=[[x,y]]
                            seq=[subset['number']]


                        elif bestScore == stepScore:
                            count+=1
                            step.append([x,y])
                            seq.append(subset['number'])


                else:
                    continue

        return {"score":bestScore,"number":count,"move":step,"seq":seq}


    def get_move(self,state, player):
        # state is a ndarray
        # player is a player object (not need to use)
        
        if(self.count>=20):     #editing for the time limit
            self.targetDepth=5 # improve the performance
        elif(self.count>=22):
            self.targetDepth=7

        temp=self.minimax(copy.deepcopy(state), 1, 1, 0)
        res=temp['move'][np.argmin(temp['seq'])]# reduce the oppotunity such opponity can get the best score
        self.count+=2
        return res


    
