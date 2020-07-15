#T-drop (a tetris clone)


import pygame, sys, random, time
from pygame.locals import *


FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'


MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN =int((WINDOWWIDTH - BOARDWIDTH*BOXSIZE)/2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT*BOXSIZE)-5


#       R   G   B
WHITE = (255,255,255)
GRAY = (185,185,185)
BLACK = (0,0,0)
RED = (155,0,0)
LIGHTRED = (175,20,20)
GREEN = (0,155,0)
LIGHTGREEN = (20,175,20)
BLUE = (0,0,155) 
LIGHTBLUE = (20,20,175)
YELLOW = (155,155,0)
LIGHTYELLOW = (175,175,0)


BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color should have a light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                    '.....',
                    '..00.',
                    '.00..',
                    '.....'],
                    ['.....',
                    '..0..',
                    '..00.',
                    '...0.',
                    '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                    '.....',
                    '.00..',
                    '..00.',
                    '.....'],
                    ['.....',
                    '..0..',
                    '.00..',
                    '.0...',
                    '.....']]

I_SHAPE_TEMPLATE = [['..0..',
                    '..0..',
                    '..0..',
                    '..0..',
                    '.....'],
                    ['.....',
                    '......',
                    '0000.',
                    '.....',
                    '.....']]

O_SHAPE_TEMPLATE = [['.....',
                    '.....',
                    '.00..',
                    '.00..',
                    '.....']]

J_SHAPE_TEMPLATE = [['.....',
                    '.0...',
                    '.000.',
                    '.....',
                    '.....'],
                    ['.....',
                    '..00.',
                    '..0..',
                    '..0..',
                    '.....'],
                    ['.....',
                    '.....',
                    '.000.',
                    '...0.',
                    '.....'],
                    ['.....',
                    '..0..',
                    '..0..',
                    '.00..',
                    '.....']]


L_SHAPE_TEMPLATE = [['.....',
                    '...0.',
                    '.000.',
                    '.....',
                    '.....'],
                    ['.....',
                    '..0..',
                    '..0..',
                    '..00.',
                    '.....'],
                    ['.....',
                    '.....',
                    '.000.',
                    '.0...',
                    '.....'],
                    ['.....',
                    '.00..',
                    '..0..',
                    '..0..',
                    '.....']]

T_SHAPE_TEMPLATE = [['.....',
                    '..0..',
                    '.000.',
                    '.....',
                    '.....'],
                    ['.....',
                    '..0..',
                    '..00.',
                    '..0..',
                    '.....'],
                    ['.....',
                    '.....',
                    '.000.',
                    '..0..',
                    '.....'],
                    ['.....',
                    '..0..',
                    '.00..',
                    '..0..',
                    '.....']]

SHAPES = {'S':S_SHAPE_TEMPLATE,
        'Z':Z_SHAPE_TEMPLATE,
        'J':J_SHAPE_TEMPLATE,
        'L':L_SHAPE_TEMPLATE,
        'I':I_SHAPE_TEMPLATE,
        'O':O_SHAPE_TEMPLATE,
        'T':T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF - pygame.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansnold.ttf',18)
    BIGFONT = pygame.font.Font('freesansbold.ttf',100)
    pygame.displayt.set_caption('T-Drop')

    showTextScreen('T-drop')

    while True:
        if random.randint(0,1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        
        pygame.mixer.music.play(-1,0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no moving variable
    movingRight = False
    movingLeft = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True: # main game loop
        if fallingPiece == None:
            # no falling piece in play, so start a new piece at the top
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # reset last fall time

            if not isValidPosition(board, fallingPiece):
                return # can't fit a new piece in the board, so game over
            
        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYUP:
                if (event.key == K_p):
                    # pausing the game
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('paused') # paused untill a key is pressed
                    pygame.mixer.music.play(-1,0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key ==K_LEFT or event.key == K_a):
                    movingLeft =False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False
            
            elif event.type == KEYDOWN:
                # moving the block sideways 
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjx=-1):
                    fallingPiece['x'] -=1
                    movingLeft =True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif(event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] +=1
                    movingLeft = False
                    movingRight = True
                    lastMoveSidewaysTime = time.time()

                
                # rotating the block (if there is room to rotate)
                