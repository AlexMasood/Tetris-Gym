import pygame
from gameControl import GameControl
from pygame.constants import KEYDOWN
from board import Board
from shape import Shape
import random
import time
class Tetris:
    def __init__(self):
        pygame.init()
        #font setup
        self.font = pygame.font.SysFont(None, 24)
        self.nextText = self.font.render('Next', True, (255,255,255))
        self.gameControl = GameControl()
        self.surface = self.gameControl.setupScreen()
        self.linesText = self.font.render('Lines:  0', True, (255,255,255))
        self.scoreText = self.font.render('Score:  0', True, (255,255,255))
        self.levelText = self.font.render('Level:  0', True, (255,255,255))


    def action(self, action):
        shape = self.gameControl.getShape()
        board = self.gameControl.getBoard()
        if(action == 0):#move left
            if(not(board.collisionCheck(shape,-1,0)) and ((shape.x + shape.getLeftHeight(shape.getShapeData()))>0)):#check if legal
                    shape.moveShapeLeft()
        elif(action == 1):#move right
            if(not(board.collisionCheck(shape,1,0)) and ((shape.x - shape.getRightHeight(shape.getShapeData()))<10)):#check if legal
                shape.moveShapeRight()
        elif(action == 2):#rotate
            shape.setShapeData(shape.rotateShape(shape.getShapeData()))
            if(board.collisionCheck(shape,0,0)):#check if legal
                shape.setShapeData(shape.undoRotation(shape.getShapeData()))
            elif ((shape.x - shape.getRightHeight(shape.getShapeData()))>10) or ((shape.x + shape.getLeftHeight(shape.getShapeData()))<0):
                shape.setShapeData(shape.undoRotation(shape.getShapeData()))
        elif(action == 3):#hard drop
            while(not(board.collisionCheck(shape,0,1))):
                shape.moveShapeDown()
            board.addPlacedShapesToBoard(shape)
            self.gameControl.newShape = True

    def evaluate(self):
        pass
    
    def observer(self):
        pass

    def view(self):

        clearedRows = self.gameControl.getBoard().rowsCleared
        self.linesText = self.font.render('Lines:  '+str(clearedRows), True, (255,255,255))
        self.scoreText = self.font.render('Score:  '+str(self.gameControl.score), True, (255,255,255))
        self.levelText = self.font.render('Level:  '+str(self.gameControl.level), True, (255,255,255))


        width,height = self.gameControl.getBoard().getDimensions()
        self.surface.fill((0,0,0))
        self.gameControl.getBoard().drawBoard(self.surface)
        
        #self.gameControl.getShape().drawNextShape(self.surface,width,height)
        self.surface.blit(self.nextText, (width + 35, 5))
        self.surface.blit(self.linesText, (width + 20, 150))
        self.surface.blit(self.scoreText, (width + 20, 170))
        self.surface.blit(self.levelText, (width + 20, 190))
        if(self.gameControl.getShape() != None):
            pygame.draw.rect(self.surface, (102,102,102), (width,0,150,height))
            self.gameControl.getShape().drawNextShape(self.surface,width,height)
            self.gameControl.getShape().drawShape(self.surface)
        
        pygame.display.flip()


t = Tetris()
t.gameControl.update()
while True:
    t.action(random.randint(0,4))
    t.gameControl.update()
    t.view()

    