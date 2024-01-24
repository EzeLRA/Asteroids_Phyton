import pygame
from pygame.locals import *
import random
import math
from functions import Rotate
import sys

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
    def __init__(self,size,pos,stagePri):
        
        sides = 9
        inclination = 360 / sides
        deformity = 8
        ang = 0
        i = 0

        self.stageIsPri = stagePri

        self.p = []
        if stagePri:
            self.Size = random.randrange(size,size+15,1)
        else:
            self.Size = random.randrange(size,size+5,1)
        self.x = pos[0]
        self.y = pos[1]
        
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

    

class Fragment:
    def __init__(self,p1,p2,pC,ang):
        self.pC = pC
        self.p1 = p1
        self.p2 = p2
        self.angle = 3
        self.gravity = [random.uniform(-1,1)+1,random.uniform(-1,1)+1]

    def Draw(self,screen):
        pygame.draw.line(screen,"white",self.p1,self.p2,1)

    def Movements(self):
        self.angle += 0.001
        Rotate(self.p1,self.pC,self.angle)
        Rotate(self.p2,self.pC,self.angle)
        self.p1[0] -= self.gravity[0]
        self.p1[1] -= self.gravity[1]
        self.p2[0] -= self.gravity[0]
        self.p2[1] -= self.gravity[1]
        self.pC[0] -= self.gravity[0]
        self.pC[1] -= self.gravity[1]

    def escenaryLimit(self):
        if (self.pC[1] > 750)and(self.pC[1] < -150)or(self.pC[0] > 750)and(self.pC[0] < -150):
            return True
        else:
            return False


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

        SoundShoot = pygame.mixer.Sound("Resources/Sounds/actions/shot.wav")

        if (pulse != shootButton[0]) and (pulse):
            
            bullets.append(Bullet(self.p1,self.angle[0]))
            SoundShoot.play()
        
        shootButton[0] = pulse

    def Impact(self,ast):
        isTrue = ast.colission(self.p1) or ast.colission(self.p2) or ast.colission(self.p3) or ast.colission(self.p4) or ast.colission(self.p5)
        return isTrue
    
    def shipExplosion(self,fragments):
        f1a = [self.Coords[0],self.Coords[1]+16]
        f1b = [self.Coords[0],self.Coords[1]+16]
        f2 = [self.Coords[0]-8,self.Coords[1]-10]
        f3 = [self.Coords[0]+8,self.Coords[1]-10]
        f4 = [self.Coords[0]+6,self.Coords[1]-4]
        f5 = [self.Coords[0]-6,self.Coords[1]-4]
        distMedia1 = [((f4[0]-f5[0])/2)+f5[0],((f4[1]-f5[1])/2)+f5[1]]
        distMedia2 = [((f1a[0]-f2[0])/2)+f2[0],((f1a[1]-f2[1])/2)+f2[1]]
        distMedia3 = [((f1b[0]-f3[0])/2)+f3[0],((f1b[1]-f3[1])/2)+f3[1]]

        
        fragments.append(Fragment(f4,f5,distMedia1,self.angle[0]))
        fragments.append(Fragment(f1a,f2,distMedia2,self.angle[0]))
        fragments.append(Fragment(f1b,f3,distMedia3,self.angle[0]))

class menuScores:
    def __init__(self,x,y,screen):
        self.X = x
        self.Y = y
        self.Screen = screen
        self.fontMenu = pygame.font.Font("Resources/Font/pixelmix.ttf", 15)
        self.username = ""
        self.cant = 0
        self.caracteres = ['',]
        self.max = 6
        self.vector = []

    def titleScore(self):
        img_letra = self.fontMenu.render("Insert your username:", True, "White")
        self.Screen.blit(img_letra, (self.X-105, self.Y))

    def usernameTitle(self):
        img_letra = self.fontMenu.render("______", True, "White")
        self.Screen.blit(img_letra, (self.X-35, self.Y+30))

    def insert(self, Evento):
        for action in Evento:
            if action.type == pygame.QUIT:
                sys.exit(0)
            if action.type == KEYDOWN:
                if action.key == K_ESCAPE:
                    sys.exit(0)
                elif action.key == K_BACKSPACE: #Borrado
                    self.caracteres[0] = self.caracteres[0][0:-1]
                    self.username = self.caracteres[0]
                    self.cant -= 1
                else:
                    if (self.cant < self.max)and(action.key != K_RETURN):
                        self.caracteres[0] = str(self.caracteres[0] + action.unicode)
                        self.username = self.caracteres[0]
                        self.cant += 1

    def exitInsert(self):
        keys = pygame.key.get_pressed()
        if (keys[K_RETURN]) and (self.cant == self.max): #Enter
            return True
        else:
            return False

    def usernameDisplay(self):
        img_letra = self.fontMenu.render(self.username, True, "White")
        self.Screen.blit(img_letra, (self.X-35, self.Y+30))

    def displayList(self):
        #Lectura de archivo y ordenado

        archivo = open("stats.txt",'r')

        self.vector = []

        linea = archivo.readline()
        while(linea!=""):
            linea = archivo.readline()
            cad = linea.replace('\n','')
            if cad != "":
                self.vector.append([])
                self.vector[len(self.vector)-1] = cad.split(';')

        archivo.close()


        #Ordenado de vector
        for i in range(len(self.vector)):
            for j in range(len(self.vector)-1):
                if (int(self.vector[j][1]) < int(self.vector[j+1][1])):
                    temp = self.vector[j]
                    self.vector[j] = self.vector[j+1]
                    self.vector[j+1] = temp

        posY = 0

        for i in range(0,len(self.vector)):
            img_letra = self.fontMenu.render(str(self.vector[i][0])+" "+str(self.vector[i][1])+" "+str(self.vector[i][2])+" "+str(self.vector[i][3]), True, "White")
            self.Screen.blit(img_letra, (self.X-35, (self.Y+70)+posY))
            
            posY += 17

    def setNewStats(self,points,level,time):
        encontro = False

        #Agregado de elemento (Desordenado)
        archivo = open("stats.txt",'r+')

        linea = archivo.readline()
        while (linea != ""):
            linea = archivo.readline()
            cad = linea.replace('\n','')
            cad = cad.split(';')

            #Busca en la lista si no hay datos que no coincidan
            if (linea != "")and(cad[0]==self.username)and(cad[1]==str(points))and(cad[2]==str(level)and(cad[3]==str(time))):
                encontro = True

            #Guarda en la ultima linea vacia si no existe el dato 
            if (linea == "")and(encontro==False):
                archivo.write("\n"+self.username+";"+str(points)+";"+str(level)+";"+str(time))               

        archivo.close()

    




        
        


