# /////////////////////////////////// 
# // CS4386 Semester B, 2021-2022 
# // Assignment 1 
# // Name: Leung Yiu Kwong 
# // Student ID: 56264368  
# /////////////////////////////////// 


import copy 
from math import inf as infinity
import game

class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole
        self.isAI = isAI
        self.score=0
        self.MAX_DEPTH=4

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
    
    def get_move(self,state,player):
        move=self.minimax(state, 0, 1)
        return move["bestMove"]

    def minimax(self,state,depth,isMax):
        
        bestScore = None
        bestMove = None

        if depth == self.MAX_DEPTH:
            return {"bestScore":bestScore,"bestMove":bestMove}

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell is None:
                    currPos = [x,y]
                    currScore = self.evaluateState(state,currPos,isMax)
                    tempState=copy.deepcopy(state)
                    tempState[x][y]='O'
                    scoreMove=self.minimax(tempState,depth+1,isMax*-1)

                    if scoreMove["bestScore"] is not None:
                        currScore+=scoreMove["bestScore"]

                    if isMax != 1:
                        if bestScore is None or bestScore>currScore:
                            bestScore=currScore
                            bestMove=currPos
                    else:
                        if bestScore is None or bestScore<currScore:
                            bestScore=currScore
                            bestMove=currPos

        return {"bestScore":bestScore,"bestMove":bestMove}

    def evaluateState(self,state,currPos,isMax):
        row=currPos[0]
        col=currPos[1]
        state[row][col]="O"
        totalScore = game.alignement(state, row, col)
        state[row][col]=None
        return totalScore*isMax      