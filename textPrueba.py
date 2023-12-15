# Imports
import sys
import pygame
import math
from functions import Rotate



def delaySeconds(tS,aux,temp):
    tiempoActual = int(pygame.time.get_ticks() / 1000)
    cumple = False

    if aux[0] == tiempoActual:
        t = aux[0] - 1
        print("Segundo Actual:",t)

        if (tS[0] <= temp):
            tS[2] = t

        tS[0] = tS[2] - tS[1]
        
        if tS[0]>=temp:
            print("Pasaron ",temp," segundos")
            tS[0] = 0
            tS[1] = tS[2]
            cumple = True

        aux[0] += 1

    return cumple

def delayMiliSeconds(tA,ml1,v,tmS,temp):#Aproximation to Miliseconds in base to Ticks
    tiempoActual = pygame.time.get_ticks()
    cumple = False

    if tA[0] != 0:
        if tiempoActual > tA[0]:
            v[0] = (tiempoActual - tA[0])/1000
            ml1[0] += v[0]
            mili2 = int(ml1[0]*1000)
            print(mili2)

            if (tmS[0] <= temp):
                tmS[2] = mili2

            tmS[0] = tmS[2] - tmS[1]
        
            if tmS[0]>=temp:
                print("Pasaron ",temp," milisegundos")
                tmS[0] = 0
                tmS[1] = tmS[2]
                cumple = True

    tA[0] = tiempoActual

    return cumple        



# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))


letra = pygame.font.Font("Resources/Font/pixelmix.ttf",42)

pygame.key.set_repeat(10)

running = True

cambio = False

#Time in Seconds:
tSeconds = [0,0,0]
temp = 1 #temporizador para contar segundos
aux = [1]

#Time in Miliseconds
tmS = [0,0,0]
tempMili = 100
mili1 = [0]
tiempoAnterior = [0]
variacion=[0]

# Game loop.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    """
    if delaySeconds(tSeconds,aux,temp):
        screen.fill("white")
    else:
        screen.fill("black")
    """
    
    if delayMiliSeconds(tiempoAnterior,mili1,variacion,tmS,tempMili):
        screen.fill("white")
    else:
        screen.fill("black")
    
    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()