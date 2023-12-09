# Imports
import sys
import pygame
import math
from functions import Rotate

class objeto1:
    def __init__(self,coords):
        self.x = coords[0]
        self.y = coords[1]
    def drawCircle(self,screen):
        pygame.draw.circle(screen,"white",[self.x,self.y],20)
    def colission1(self,coordsObjet):
        dx = coordsObjet[0] - self.x
        dy = coordsObjet[1] - self.y
        return (math.sqrt(dx*dx + dy*dy) < 20)


class objeto2:
    def __init__(self,coords,ang):
        self.x = coords[0]
        self.y = coords[1]
        self.angle = ang[0]
    def draw(self,screen):
        p1 = [self.x+10,self.y+2]
        p2 = [self.x-10,self.y+2]
        p3 = [self.x,self.y+25]
        Rotate(p1,[self.x,self.y],self.angle)
        Rotate(p2,[self.x,self.y],self.angle)
        Rotate(p3,[self.x,self.y],self.angle)
        pygame.draw.line(screen,"white",p1,p3,1)
        pygame.draw.line(screen,"white",p2,p3,1)
        pygame.draw.line(screen,"white",p1,p2,1)
    def colission2(self,objeto1):
        p1 = [self.x+10,self.y+2]
        p2 = [self.x-10,self.y+2]
        p3 = [self.x,self.y+25]
        Rotate(p1,[self.x,self.y],self.angle)
        Rotate(p2,[self.x,self.y],self.angle)
        Rotate(p3,[self.x,self.y],self.angle)
        cumple = objeto1.colission1(p1) or objeto1.colission1(p2) or objeto1.colission1(p3)
        return cumple 
    def Movements(self,coords,angle):
        keys = pygame.key.get_pressed()
        impulso = 0.5

        if keys[pygame.K_w]:
            coords[1] -= impulso
        if keys[pygame.K_s]:
            coords[1] += impulso
        if keys[pygame.K_a]:
            coords[0] -= impulso
        if keys[pygame.K_d]:
            coords[0] += impulso

        if keys[pygame.K_q]:
            angle[0] += 3
        if keys[pygame.K_e]:
            angle[0] -= 3

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

pygame.key.set_repeat(10)

coords1 = [(width/2),(height/2)]
coords2 = [(width/2)+40,(height/2)-15]
ang = [20]

running = True

# Game loop.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    if coords1[0] > 10:

        ob1 = objeto1(coords1)
        ob1.drawCircle(screen)

        ob2 = objeto2(coords2,ang)
        ob2.draw(screen)
        ob2.Movements(coords2,ang)
        print(ob2.colission2(ob1))

        coords1[0] -= 0.4
    else:
        coords1[0] = (width/2)+60
    

    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()