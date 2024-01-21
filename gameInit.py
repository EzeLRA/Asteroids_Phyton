import random
from random import choice
import pygame
from classes import *
from functions import *


"""
Teclas:
W = Avanzar
Q = Giro Izquierda
E = Giro Derecha
R = Revivir
Y = Reiniciar partida
P = Pausa
ESC = Salida del juego
"""

#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
dt = 0

#Game Function Data:
exit = [False]
menuInicio = True
pauseCondition = False
#Fonts
fontType = pygame.font.Font("Resources/Font/pixelmix.ttf",18)
fontType2 = pygame.font.Font("Resources/Font/pixelmix.ttf",11)
fontType3 = pygame.font.Font("Resources/Font/pixelmix.ttf",30)
#Ignition States:
ignition = False

#Stages Ambient
StagesSound = [pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient1.wav"),pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient2.wav"),pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient3.wav"),pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient4.wav")]
Stage = 0
#Explosion
ExplosionSounds = [pygame.mixer.Sound("Resources/Sounds/colisions/explosion1.wav"),pygame.mixer.Sound("Resources/Sounds/colisions/explosion2.wav"),pygame.mixer.Sound("Resources/Sounds/colisions/explosion3.wav")]
#Data
actualLevel = 1
#Time Played
seg = 0
mins = 0 
hour = 0
#Parameters for miliseconds:
tmS = [0,0,0]
tempMili = 100
mili = [0]
beforeTime = [0]
variation=[0]

#Player Data:
angle = [0]
gravity = [0,0]
player_pos = [screen.get_width() / 2, screen.get_height() / 2]
shootButton = [False]
Ship1 = Ship(player_pos,angle,gravity)
ShipImpact = False #No se esta usando
points = 0
ShipLives = 3
destroyed = False
fragments = []

#Score Menu:
Menu1 = menuScores((screen.get_width() / 2),(screen.get_height() / 2)-150,screen)
inserted = False

#Bullets Data:
bullets = []
BulletImpact = False 

#Asteroids Data:
astCant = []
size1 = 15
size2 = 7

for i in range(5):
    Xpos1 = random.randrange(int((screen.get_width() / 2)+120),700,1)
    Ypos1 = random.randrange(int((screen.get_height() / 2)+120),700,1)
    Xpos2 = random.randrange(0,int((screen.get_width() / 2)-120),1)
    Ypos2 = random.randrange(0,int((screen.get_height() / 2)-120),1)

    astCant.append(Asteroid(size1,[Xpos1,Ypos1],True))
    astCant.append(Asteroid(size1,[Xpos2,Ypos2],True))
    astCant.append(Asteroid(size1,[Xpos2,Ypos1],True))
    astCant.append(Asteroid(size1,[Xpos1,Ypos2],True))

while menuInicio:
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menuInicio = False
            running = False

    exitGame(exit)
    if exit[0] == True:
        menuInicio = False
        running = False

    #Rehused key condition
    if restartCondition():
        menuInicio = False

    #Screen
    screen.fill("black")

    #Asteroids
    for i in range(len(astCant)):
        astCant[i].Draw(screen)
        astCant[i].Movements()
        astCant[i].escenaryLimit()

    #Title
    title = fontType3.render("Asteroid",True,"White")
    screen.blit(title,((screen.get_width() / 2)-85, (screen.get_height() / 2)-80))


    #Screen Clean
    pygame.display.flip()

    #FPS
    dt = clock.tick(60) / 1000





while running:
    
    #Events
    if (ShipLives > 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    exitGame(exit)
    if exit[0] == True:
        running = False

    #Screen
    screen.fill("black")

    #Escenary
    if delayMiliSeconds(beforeTime,mili,variation,tmS,1000) and not(destroyed):
        seg += 1

    if seg>59:
        seg = 0
        mins += 1
    if mins>59:
        mins = 0
        hour += 1
    
    #Avanze de las etapas de la partida 

    keys = pygame.key.get_pressed()
    pulse = keys[pygame.K_w]
    
    ignite = pygame.mixer.Sound("Resources/Sounds/actions/propultion.wav")

    if (pulse != ignition) and (pulse):
            
        ignite.play(-1)

    elif (pulse != ignition) and not(pulse):
        pygame.mixer.stop()
        
    ignition = pulse

    if astCant:
        if (len(astCant) > 15)and(Stage==0) :
            pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient1.wav")
            pygame.mixer.music.play(-1)
            Stage += 1
        elif (len(astCant) < 10)and(Stage==1) :
            pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient2.wav")
            pygame.mixer.music.play(-1)
            Stage += 1
        elif (len(astCant) < 5)and(Stage==2) :
            pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient3.wav")
            pygame.mixer.music.play(-1)
            Stage += 1
        elif (len(astCant) <= 2)and(Stage==3) :
            pygame.mixer.music.load("Resources/Sounds/ambient/suspenseAmbient4.wav")
            pygame.mixer.music.play(-1)
            Stage += 1

    #Ship
    if destroyed == False:
        Ship1.Movements()
        Ship1.escenaryLimit()
        Ship1.Draw(screen)
        Ship1.Shot(bullets,shootButton)
    
    #Colisiones de la nave
    if astCant and (destroyed == False):
        for i in range(len(astCant)):
            if Ship1.Impact(astCant[i]): #Refinar
                destroyed = True
                ShipLives -= 1
                Ship1.shipExplosion(fragments)
                #Explosion
                ExplosionSound2 = choice(ExplosionSounds)
                ExplosionSound2.play()

    #Desplazamiento de los fragmentos
    if fragments:
        fg = 0
        removed = False
        while (fg < len(fragments))and(removed==False):
            fragments[fg].Draw(screen)
            fragments[fg].Movements()
            if fragments[fg].escenaryLimit():
                fragments.pop(fg)
                removed=True
            fg += 1

    #Evento de reinicio de juego
    if (destroyed == True) and revive() and ShipLives > 0:
        destroyed = False
        angle = [0]
        gravity = [0,0]
        player_pos = [screen.get_width() / 2, screen.get_height() / 2]
        Ship1 = Ship(player_pos,angle,gravity)


    #Asteroids
    for i in range(len(astCant)):
        astCant[i].Draw(screen)
        astCant[i].Movements()
        astCant[i].escenaryLimit()


    #Bullets
    if bullets :
        for i in range(len(bullets)):
            bullets[i].Draw(screen)
            bullets[i].Movements()
        
        if bullets[0].escenaryLimit():
            bullets.pop(0)
    
    #Impacto misil con asteroide
    if bullets and astCant :
        itm1 = 0
        itm2 = 0
        pooped = False
        while (itm1 != len(bullets))and(bullets)and(pooped == False):
            
            while (itm2 != len(astCant))and(astCant)and(pooped == False):
                
                if (bullets[itm1].ImpactBullet(astCant[itm2])):
                    bullets.pop(itm1)
                    if astCant[itm2].stageIsPri == True:
                        for i in range(5):
                            astCant.append(Asteroid(size2,[astCant[itm2].x,astCant[itm2].y],False))
                    astCant.pop(itm2)

                    #Explosion sound
                    ExplosionSound1 = choice(ExplosionSounds)
                    ExplosionSound1.play()


                    pooped = True
                else:
                    itm2 += 1    
            itm2 = 0
            itm1 += 1

            if pooped:
                points += 1
    

    #Recarga de asteroides
    if not(astCant):
        Stage = 0
        actualLevel += 1
        for i in range(5):
            Xpos1 = random.randrange(int((screen.get_width() / 2)+120),700,1)
            Ypos1 = random.randrange(int((screen.get_height() / 2)+120),700,1)
            Xpos2 = random.randrange(0,int((screen.get_width() / 2)-120),1)
            Ypos2 = random.randrange(0,int((screen.get_height() / 2)-120),1)

            astCant.append(Asteroid(size1,[Xpos1,Ypos1],True))
            astCant.append(Asteroid(size1,[Xpos2,Ypos2],True))
            astCant.append(Asteroid(size1,[Xpos2,Ypos1],True))
            astCant.append(Asteroid(size1,[Xpos1,Ypos2],True))

    #Estadisticas
    score = fontType.render("Points: " + str(points),True,"White")
    screen.blit(score,(20,20))

    lives = fontType.render("Lives: " + str(ShipLives),True,"White")
    screen.blit(lives,(20,45))

    levelPlaying = fontType.render("Level: "+str(actualLevel),True,"White")
    screen.blit(levelPlaying,(220,20))

    timeStatus = fontType.render("Time: "+str(hour)+":"+str(mins)+":"+str(seg),True,"White")
    screen.blit(timeStatus,(520,20))

    #Apartado de fin de juego
    if (ShipLives <= 0):

        pygame.mixer.music.set_volume(0.0)

        gameOver = fontType.render("Game Over",True,"White")
        screen.blit(gameOver,((screen.get_width() / 2)-60, (screen.get_height() / 2)-200))

        if inserted == True:
            restart = fontType2.render("Press Y for restart",True,"White")
            screen.blit(restart,((screen.get_width() / 2)-70, (screen.get_height() / 2)-175))

        #Apartado de apodo y puntajes
        
        Menu1.titleScore()
        
        if inserted == False:

            Evento = pygame.event.get()

            Menu1.insert(Evento)
            if Menu1.exitInsert():
                inserted=True
            Menu1.usernameDisplay()


        if restartCondition() and (inserted==True):
            #Stage restart
            Stage = 0
            pygame.mixer.music.set_volume(1.0)
            #Level restart
            actualLevel = 1
            #Time
            seg = 0
            mins = 0
            hour = 0
            #Ship
            ShipLives = 3
            destroyed = False
            points = 0
            angle = [0]
            gravity = [0,0]
            player_pos = [screen.get_width() / 2, screen.get_height() / 2]
            Ship1 = Ship(player_pos,angle,gravity)




    pausePressed = pauseKey()

    if (pausePressed != pauseCondition) and (pausePressed) and (ShipLives > 0):
        
        titleWrited = False
        pauseCondition = True

        pygame.mixer.music.set_volume(0.0)

        while pauseCondition and running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            exitGame(exit)
            if exit[0] == True:
                running = False

            if (pausePressed==False)and pauseKey():
                pauseCondition = False

            pausePressed = pauseKey()

            if titleWrited == False:
                pauseTitle = fontType.render("Pause",True,"White")
                screen.blit(pauseTitle,((screen.get_width() / 2)-40, screen.get_height() / 2))
                pygame.display.flip()
                titleWrited = True
        
        pygame.mixer.music.set_volume(1.0)

    pauseCondition = pausePressed




    #Screen Clean
    pygame.display.flip()

    #FPS
    dt = clock.tick(60) / 1000

pygame.quit()
