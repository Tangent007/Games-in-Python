# slide puzzle

import pygame , sys , random
from pygame.locals import *

#create the constants (go ahead and experiment with different values)

BOARDWIDTH = 4 # number of col in the board
BOARDHEIGHT = 4 # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#       R   G   B
BLACK=(0,0,0)
WHITE =(255,255,255)
BRIGHTBLUE=(0,50,255)
DARKTURQUOISE=(3,54,73)
GREEN = (0,204,0)

BGCOLOR = DARKTURQUOISE
TILECOLOR=GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20
BUTTONCOLOR =WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH-(TILESIZE*(BOARDWIDTH-1)))/2)
YMARGIN = int((WINDOWHEIGHT-(TILESIZE*(BOARDHEIGHT-1)))/2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK,DISPLAYSURF,BASICFONT,RESET_SURF,RESET_RECT,NEW_SURF,NEW_RECT,SOLVE_SURF,SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Slide PuZZle')
    BASICFONT=pygame.font.Font('freesansbold.ttf',BASICFONTSIZE)

    # store the option buttons and their rectangles in options
    REST_SURF,REST_RECT = makeText('Reset', TEXTCOLOR,TILECOLOR,WINDOWWIDTH-120,WINDOWHEIGHT-90)
    NEW_SURF, NEW_RECT = makeText('New Game',TEXTCOLOR,TILECOLOR,WINDOWWIDTH-120,WINDOWHEIGHT-30)

    mainBoard , solutionSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStraightBoard() # a solved board is the same as the board in start state
    allMoves = [] # list of moves made from the solved configuration

    while True: # main game loop
        slideTo = None # the direction, if any a tile should slide
        msg = '' # contains the message to show in the upper left corner
        if mainBoard == SOLVEDBOARD:
            msg='Solved!'
            drawBoard(mainBoard,msg)

            checkForQuit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    spotx, spoty =getSpotClicked(mainBoard,event.pos[0],event.pos[1])
                    if(spotx,spoty) == (None,None):
                        # check if the user clicked on an option button 
                        if RESET_RECT.collidepoint(event.pos):
                            resetAnimation(mainBoard,allMoves) # clicked on the reset button
                            allMoves=[]
                        elif NEW_RECT.collidepoint(event.pos):
                            mainBoard,solutionSeq =generateNewPuzzle(80) # clicked on new game button
                            allMoves=[]
                        elif SOLVE_RECT.collidepoint(event.pos):
                            resetAnimation(mainBoard,solutionSeq+allMoves) # clicked on solve button
                            allMoves=[]
                    else :
                        # check if the clicked tile was next to the blank spot
                        blankx, blanky = getBlankPosition(mainBoard)
                        if spotx ==blankx+1 and spoty == blanky:
                            slideTo=LEFT
                        elif spotx ==blankx-1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky +1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky -1 :
                            slideTo = DOWN
                elif event.type ==KEYUP:
                    # check if the user pressed a key slide a tile
                    if event.key in(K_LEFT,K_a) and isValidMove(mainBoard,LEFT):
                        slideTo = LEFT
                    elif event.key in (K_RIGHT,K_d) and isValidMove(mainBoard,RIGHT):
                        slideTo = RIGHT
                    elif event.key in (K_UP,K_w) and isValidMove(mainBoard,UP):
                        slideTo = UP
                    elif event.key in (K_DOWN,K_s) and isValidMove(mainBoard,DOWN):
                        slideTo = DOWN
            if slideTo:
                slideAnimation(mainBoard,slideTo,'Click tile or press arrow keys to slide',8) # show slide on screen
                makeMove(mainBoard,slideTo)
                allMoves.append(slideTo) # record the slide
            pygame.display.update()
            FPSCLOCK.tick(FPS)