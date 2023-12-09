import pygame
import random
import math
from functions import Rotate

class Bullet:
    def __init__(self,coords,angle):
        self.direction = angle
        self.Coords = coords
        acceleration=[0.0,-4]
        Rotate(acceleration,[0.0,0.0],self.direction)
        self.gravity1 = acceleration[0]
        self.gravity2 = acceleration[1]

    def Draw(self,screen):
        p1 = [self.Coords[0],self.Coords[1]+4]
        p2 = [self.Coords[0],self.Coords[1]-4]
        Rotate(p1,self.Coords,self.direction)
        Rotate(p2,self.Coords,self.direction)
        pygame.draw.line(screen,"white",p1,p2,1)

    def Movements(self):
        self.Coords[0] -= self.gravity1
        self.Coords[1] -= self.gravity2

    def escenaryLimit(self):  
        if (self.Coords[1] > 750) or (self.Coords[1] < -150):
            return True
        if (self.Coords[0] > 750) or (self.Coords[0] < -150):
            return True

    def ImpactBullet(self,ast):
        p1 = [self.Coords[0],self.Coords[1]+4]
        p2 = [self.Coords[0],self.Coords[1]-4]
        isTrue = ast.colission(p1) or ast.colission(p2)
        return isTrue



class Asteroid:
    def __init__(self):
        
        sides = 9
        inclination = 360 / sides
        deformity = 8
        ang = 0
        i = 0

        self.p = []
        self.Size = random.randrange(15,30,1)
        self.x = random.randrange(0,700,1)
        self.y = random.randrange(0,700,1)
        
        for i in range(sides):
            self.p.append([self.x,self.y + random.randrange(self.Size,self.Size+deformity,2)])
            Rotate(self.p[i],[self.x,self.y],ang)
            ang += inclination

        self.gravity = [random.uniform(-1,1),random.uniform(-1,1)]

    def Draw(self,screen):
        for i in range(len(self.p)-1):
            pygame.draw.line(screen,"white",self.p[i],self.p[i+1],1)
        pygame.draw.line(screen,"white",self.p[len(self.p)-1],self.p[0],1)
            
    def centerPoint(self):
        self.x -= self.gravity[0]
        self.y -= self.gravity[1]

    def Movements(self):
        Asteroid.centerPoint(self)
        for i in range(len(self.p)):
            self.p[i][0] -= self.gravity[0]
            self.p[i][1] -= self.gravity[1]

    def escenaryLimit(self):
        for i in range(len(self.p)):
            #Axis X
            if self.p[i][0] > 750:
                for j in range(len(self.p)):
                    self.p[j][0] -= 850
                self.x -= 850
            elif self.p[i][0] < -150:
                for j in range(len(self.p)):
                    self.p[j][0] += 850
                self.x += 850
            #Axis Y
            if self.p[i][1] > 750:
                for j in range(len(self.p)):
                    self.p[j][1] -= 850
                self.y -= 850
            elif self.p[i][1] < -150:
                for j in range(len(self.p)):
                    self.p[j][1] += 850
                self.y += 850

    def colission(self,coordsObjet):
        dx = coordsObjet[0] - self.x
        dy = coordsObjet[1] - self.y
        return (math.sqrt(dx*dx + dy*dy) < self.Size)



class Ship:
    def __init__(self,coords,angle,gravity):
        self.angle = angle
        self.gravity = gravity
        self.Coords = coords

    def VertexThrust(self):
        self.p6 = [self.Coords[0]+4,self.Coords[1]-4]
        self.p7 = [self.Coords[0]-4,self.Coords[1]-4]
        self.p8 = [self.Coords[0],self.Coords[1]-18]

        Rotate(self.p6,self.Coords,self.angle[0])
        Rotate(self.p7,self.Coords,self.angle[0])
        Rotate(self.p8,self.Coords,self.angle[0])

    def thrustDraw(self,screen):
        Ship.VertexThrust(self)

        pygame.draw.line(screen,"white",self.p6,self.p8,1)
        pygame.draw.line(screen,"white",self.p7,self.p8,1)

    def VertexShip(self):
        self.p1 = [self.Coords[0],self.Coords[1]+16]
        self.p2 = [self.Coords[0]-8,self.Coords[1]-10]
        self.p3 = [self.Coords[0]+8,self.Coords[1]-10]
        self.p4 = [self.Coords[0]+6,self.Coords[1]-4]
        self.p5 = [self.Coords[0]-6,self.Coords[1]-4]

        Rotate(self.p1,self.Coords,self.angle[0])
        Rotate(self.p2,self.Coords,self.angle[0])
        Rotate(self.p3,self.Coords,self.angle[0])
        Rotate(self.p4,self.Coords,self.angle[0])
        Rotate(self.p5,self.Coords,self.angle[0])

    def Draw(self,screen):
        keys = pygame.key.get_pressed()

        Ship.VertexShip(self)

        if keys[pygame.K_w]:
            Ship.thrustDraw(self,screen)
            pygame.draw.line(screen,"white",self.p4,self.p5,1)
            pygame.draw.line(screen,"white",self.p2,self.p1,1)
            pygame.draw.line(screen,"white",self.p3,self.p1,1)
        else:
            pygame.draw.line(screen,"white",self.p4,self.p5,1)
            pygame.draw.line(screen,"white",self.p2,self.p1,1)
            pygame.draw.line(screen,"white",self.p3,self.p1,1)

    def Movements(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            acceleration=[0.0,-0.1]
            Rotate(acceleration,[0.0,0.0],self.angle[0])
            self.gravity[0] += acceleration[0]
            self.gravity[1] += acceleration[1]

        if keys[pygame.K_q]:
            self.angle[0] += 3
        if keys[pygame.K_e]:
            self.angle[0] -= 3
    
        self.Coords[0] -= self.gravity[0]
        self.Coords[1] -= self.gravity[1]

    def escenaryLimit(self):
        if self.Coords[1] > 750:
            self.Coords[1] = -100
        if self.Coords[1] < -150:
            self.Coords[1] = 740

        if self.Coords[0] > 750:
            self.Coords[0] = -100
        if self.Coords[0] < -150:
            self.Coords[0] = 740

    def Shot(self,bullets,shootButton):
        keys = pygame.key.get_pressed()
        pulse = keys[pygame.K_SPACE] 

        if (pulse != shootButton[0]) and (pulse):
            
            bullets.append(Bullet(self.p1,self.angle[0]))
        
        shootButton[0] = pulse

    def Impact(self,ast):
        isTrue = ast.colission(self.p1) or ast.colission(self.p2) or ast.colission(self.p3) or ast.colission(self.p4) or ast.colission(self.p5)
        return isTrue
        

