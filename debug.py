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




# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))


letra = pygame.font.Font("Resources/Font/pixelmix.ttf",42)

pygame.key.set_repeat(10)

running = True

#Bool estados
cambio2 = False
cambio = False


#Datos de tiempo:
seg = 0
minu = 0
horas = 0

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

    if delayMiliSeconds(tiempoAnterior,mili1,variacion,tmS,1000):
        seg += 1

    if seg>59:
        seg = 0
        minu += 1
    if minu>59:
        minu = 0
        horas += 1

    print("Horas:",horas,"Minutos:",minu,"Segundos:",seg)


    if cambio2 == False:
        pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient1.wav")
        pygame.mixer.music.play(-1)
        cambio2 = True

    keys = pygame.key.get_pressed()
    pulse = keys[pygame.K_SPACE] 

    SoundShoot = pygame.mixer.Sound("Resources/Sounds/actions/propultion.wav")

    if (pulse != cambio) and (pulse):
            
        SoundShoot.play(-1)

    elif (pulse != cambio) and not(pulse):
        pygame.mixer.Sound.stop(SoundShoot)
        
    cambio = pulse



    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()