import random
import pygame
from classes import Ship,Asteroid,Bullet
from functions import exitGame
from functions import revive

#Pygame Setup
pygame.init()
screen = pygame.display.set_mode((700, 700))
clock = pygame.time.Clock()
running = True
dt = 0

#Game Function Data:
exit = [False]
fontType = pygame.font.Font("Resources/Font/pixelmix.ttf",18)


#Player Data:
angle = [0]
gravity = [0,0]
player_pos = [screen.get_width() / 2, screen.get_height() / 2]
shootButton = [False]
Ship1 = Ship(player_pos,angle,gravity)
ShipImpact = False
points = 0
ShipLives = 3
destroyed = False
fragments = []

#Bullets Data:
bullets = []
BulletImpact = False 

#Asteroids Data:
astCant = []
size1 = 15
size2 = 7

for i in range(15):
    astCant.append(Asteroid(size1,[random.randrange(0,700,1),random.randrange(0,700,1)],True))


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
    if destroyed == False:
        Ship1.Movements()
        Ship1.escenaryLimit()
        Ship1.Draw(screen)
        Ship1.Shot(bullets,shootButton)
    
    if astCant and (destroyed == False):
        for i in range(len(astCant)):
            if Ship1.Impact(astCant[i]): #Refinar
                destroyed = True
                ShipLives -= 1
                Ship1.shipExplosion(fragments)

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
                    pooped = True
                else:
                    itm2 += 1    
            itm2 = 0
            itm1 += 1

            if pooped:
                points += 1
            
    if not(astCant):
        for i in range(15):
            astCant.append(Asteroid(size1,[random.randrange(0,700,1),random.randrange(0,700,1)],True))

    score = fontType.render("Points: " + str(points),True,"White")
    screen.blit(score,(20,20))


    lives = fontType.render("Lives: " + str(ShipLives),True,"White")
    screen.blit(lives,(20,45))

    if ShipLives == 0:
        gameOver = fontType.render("Game Over",True,"White")
        screen.blit(gameOver,((screen.get_width() / 2)-60, screen.get_height() / 2))

    #Screen Clean
    pygame.display.flip()

    #FPS
    dt = clock.tick(60) / 1000

pygame.quit()
