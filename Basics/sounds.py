import pygame,sys
from pygame.locals import *

pygame.init()

displaysurf = pygame.display.set_mode((400,300))
pygame.display.set_caption('sound')
soundObj =pygame.mixer.Sound('beep1.ogg')
soundObj.play()
import time
time.sleep(1)
soundObj.stop()

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
