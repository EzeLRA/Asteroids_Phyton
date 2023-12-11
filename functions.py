import pygame
from cmath import pi
import math

def Rotate(pos,posC,da):
    dx = pos[0] - posC[0] 
    dy = pos[1] - posC[1]
    r = math.sqrt(dx*dx + dy*dy)
    a = math.atan2(dy,dx)
    a -= da / 180 * pi

    pos[0] = posC[0] + r * math.cos(a)
    pos[1] = posC[1] + r * math.sin(a)


def exitGame(key):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        key[0] = True

def revive():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        return True
    else:
        return False
    