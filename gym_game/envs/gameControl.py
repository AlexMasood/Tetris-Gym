import pygame
from .board import Board
from .shape import Shape
class GameControl():
    def __init__(self):
        self.exitGame = False
        self.newShape = True
        #board and screen setup
        self.board = Board()
        self.width,self.height  = self.board.getDimensions()
        self.shape = Shape(self.width)
        
        self.loopNum = 0
        self.clearedRows = 0
        self.score = 0
        self.level = 0
        self.maxLoop = 5
    
    def resetGameControl(self):
        self.exitGame = False
        self.newShape = True
        self.board.resetBoard()
        self.shape.resetShape()
        self.loopNum = 0
        self.clearedRows = 0
        self.score = 0
        self.level = 0
        self.maxLoop = 5

    def getBoard(self):
        return self.board
    
    def getShape(self):
        return self.shape

    def setupScreen(self):
        width,height = self.board.getDimensions()
        pygame.display.set_mode((width+150,height))#100 represents the menu to the side of the game board
        screen = pygame.display.get_surface()
        return screen
    
    def emptySpaces(self):
        score = 0
        gameboard = self.board.board
        for row in gameboard:
            for block in row:
                if (block == 0):
                    score-=1
        return score
        
    def scorer(self,lines,level):
        if(lines == 1):
            print("line " +str(lines))
            return 40 * (level + 1)
        elif(lines == 2):
            print("line " +str(lines))
            return 100 * (level + 1)
        elif(lines == 3):
            print("line " +str(lines))
            return 300 * (level + 1)
        elif(lines == 4):
            print("line " +str(lines))
            return 1200 * (level + 1)
        else:
            return 0


    def update(self):
        if (self.newShape == True):
            self.shape.popShapeBag()
            self.shape.resetShape()
            self.newShape = False
        if(self.loopNum>self.maxLoop):#game loops until shape moves down
            self.loopNum = 0
            self.shape.moveShapeDown()
        self.loopNum+=1
        
        
        if(self.loopNum>self.maxLoop-1):
            if (self.board.collisionCheck(self.shape,0,1)):
                self.board.addPlacedShapesToBoard(self.shape)
                self.newShape = True
                self.loopNum = 0
        
        self.level = self.clearedRows//10
        self.score += self.scorer(self.board.rowCheck(),self.level)

        if(self.board.toppleCheck()):
            self.exitGame = True
            if (self.clearedRows>0):
                print("cleared rows"+str(self.clearedRows))

