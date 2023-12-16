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

def restartCondition():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_y]:
        return True
    else:
        return False

def pauseKey():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p]:
        return True
    else:
        return False


def delayMiliSeconds(tA,ml1,v,tmS,temp):#Aproximation to Miliseconds in base to Ticks
    actualTime = pygame.time.get_ticks()
    sucess = False

    if tA[0] != 0:
        if actualTime > tA[0]:
            v[0] = (actualTime - tA[0])/1000
            ml1[0] += v[0]
            mili2 = int(ml1[0]*1000)
            #print(mili2)

            if (tmS[0] <= temp):
                tmS[2] = mili2

            tmS[0] = tmS[2] - tmS[1]
        
            if tmS[0]>=temp:
                #print("Pasaron ",temp," milisegundos")
                tmS[0] = 0
                tmS[1] = tmS[2]
                sucess = True

    tA[0] = actualTime

    return sucess  
    