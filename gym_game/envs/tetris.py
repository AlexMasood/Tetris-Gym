import pygame
from .gameControl import GameControl
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
        self.changeModeText = self.font.render('Press "v" to change view mode', True, (255, 255, 0))
        self.mode = 0


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
                self.gameControl.score+=1
            board.addPlacedShapesToBoard(shape)
            self.gameControl.newShape = True
        self.gameControl.update()

    def evaluate(self):
        return self.gameControl.score + self.gameControl.emptySpaces()
    
    def observe(self):
        board = self.gameControl.getBoard()
        shape = self.gameControl.getShape()
        simpBoard = board.simplifyBoard(shape)
        return simpBoard

    def view(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_v:
                    self.mode += 1
                    self.mode = self.mode % 2
                    self.surface.fill((0,0,0))
                    self.surface.blit(self.changeModeText, (0,0))
                    pygame.display.flip()
        if (self.mode != 1):
            clearedRows = self.gameControl.getBoard().rowsCleared
            self.linesText = self.font.render('Lines:  '+str(clearedRows), True, (255,255,255))
            self.scoreText = self.font.render('Score:  '+str(self.gameControl.score), True, (255,255,255))
            self.levelText = self.font.render('Level:  '+str(self.gameControl.level), True, (255,255,255))


            width,height = self.gameControl.getBoard().getDimensions()
            self.surface.fill((0,0,0))
            self.gameControl.getBoard().drawBoard(self.surface)
            
            pygame.draw.rect(self.surface, (102,102,102), (width,0,150,height))
            self.surface.blit(self.nextText, (width + 35, 5))
            self.surface.blit(self.linesText, (width + 20, 150))
            self.surface.blit(self.scoreText, (width + 20, 170))
            self.surface.blit(self.levelText, (width + 20, 190))
            if(self.gameControl.getShape() != None):
                
                self.gameControl.getShape().drawNextShape(self.surface,width,height)
                self.gameControl.getShape().drawShape(self.surface)
            pygame.display.flip()
        
