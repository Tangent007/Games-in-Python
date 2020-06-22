#Memory puzzle


import pygame,sys,random
from pygame.locals import *

FPS=30 # frame per second
WINDOWWIDTH=640 # size of window's width
WINDOEHEIGHT=480 #size of window's height
REVEALSPEED=8 #speed boxes sliding reveals and covers
BOXSIZE=40 # size of box height and width in pixels
GAPSIZE=10 # size of gap between boxes in pixels
BOARDWIDTH=10 #number of column of icons
BOARDHEIGHT = 7 #nimber of rows of icons
assert(BOARDWIDTH*BOARDHEIGHT)%2==0,'Board need to have an even number of boxes for pair of matches.'
XMARGIN=int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
YMARGIN=int((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)

#       R   G   B
GRAY  =(100,100,100)
NAVYBLUE= (60, 60, 60)
WHITE   = (255,255,255)
RED     =(255,0,0)
GREEN   =(0,255,0)
BLUE    =(0,0,255)
YELLOW  =(255,255,0)
ORANGE  =(255,128,0)
PURPLE  =(255,0,255)
CYAN    =(0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS=(RED,GREEN,BLUE,YELLOW,ORANGE,PURPLE,CYAN)
ALLSHAPES=(DONUT,SQUARE,DIAMOND,LINES,OVAL)
assert len(ALLCOLORS)*len(ALLSHAPES)*2>= BOARDWIDTH*BOARDHEIGHT,"Board is too big for the number of shapes/colors defined."


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))

    mousex=0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('MemorY GamE')

    mainBoard =getRandomizedBoard()
    revealedBoxes = generatedRevealedBoxesData(False)

    firstSelection = None # stores the (x,y) of the first box clicked.

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: # main game loop
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        for event in pygame.event.get(): #event handling loop
            if event.type==QUIT or (event.type ==KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type ==MOUSEMOTION:
                mousex,mousey=event.pos
            elif event.type = MOUSEBUTTONUP:
                mousex,mousey =event.pos
                mouseClicked =True
        boxx,boxy=  getBoxAtPixel(mousex,mousey)
        if boxx != NOne and boxy != None:
            # the mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxb,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard,[(boxx,boxy)])
                revealedBoxes[boxx][boxy] =True # set the box as revealed
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx,boxy)
                else: # the current box was the second box clicked
                    # if ther is a match between the two icons
                    icon1shape,icon1color =getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                    icon2shape, icon2color =getShapeAndColor(mainBoard, boxx,boxy)
                    if icon1shape!=icon2shape or icon1color!=icon2color:
                        # icons dont match. recover up both selection
                        pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): # check if all pairs found
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        #reset the board
                        mainBoard = getRandomizedBoard()
                        revealBoxes = generateRevealBoxesData(False)

                        #111
