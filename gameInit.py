import pygame
from classes import Ship,Asteroid,Bullet
from functions import exitGame

#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
dt = 0

#Game Function Data:
exit = [False]

#Player Data:
angle = [0]
gravity = [0,0]
player_pos = [screen.get_width() / 2, screen.get_height() / 2]
shootButton = [False]
Ship1 = Ship(player_pos,angle,gravity)
ShipImpact = False

#Bullets Data:
bullets = []
BulletImpact = False 

#Asteroids Data:
astCant = []

for i in range(15):
    astCant.append(Asteroid())


while running:
    
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    exitGame(exit)
    if exit[0] == True:
        running = False

    #Screen
    screen.fill("black")

    #Escenary

    #Ship
    Ship1.Movements()
    Ship1.escenaryLimit()
    Ship1.Draw(screen)
    Ship1.Shot(bullets,shootButton)
    
    if astCant:
        for i in range(len(astCant)):
            if Ship1.Impact(astCant[i]):    #Refinar
                running = False

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
    
    #Impacto misil con asteroide (CORREGIR)
    if bullets and astCant :
        itm1 = 0
        itm2 = 0
        while (itm1 != len(astCant))and(astCant):
            if (itm2 != len(bullets))and(bullets): 
                if bullets[itm2].ImpactBullet(astCant[itm1]):
                    bullets.pop(itm2)
                    astCant.pop(itm1)
                else:
                    itm2 += 1
            elif (itm2 > 0)and(itm2 == len(bullets)):
                itm2 = 0
            itm1 += 1

    if not(astCant):
        for i in range(15):
            astCant.append(Asteroid())

    #Screen Clean
    pygame.display.flip()

    #FPS
    dt = clock.tick(60) / 1000

pygame.quit()
