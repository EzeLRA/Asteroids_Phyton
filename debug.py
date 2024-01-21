import pygame
from pygame.locals import *
import sys

class menu():
    def __init__(self):
        self.fuente = pygame.font.Font(None, 25)

        self.distancia = 20
        self.pos_x = 50
        self.pos_y = 50

        self.cursorIndice = 1
        self.cursor_x = 50
        self.cursor_y = 50

    def cursorAbajo(evento):
        for accion in evento:
            if accion.type == KEYDOWN and accion.key == K_DOWN:
                return True
            else:
                return False

    def cursorArriba(evento):
        for accion in evento:
            if accion.type == KEYDOWN and accion.key == K_UP:
                return True
            else:
                return False

    def texto(self,superficie,evento):
        superficie.fill((0, 0, 0))

        if menu.cursorArriba(evento) and self.cursorIndice < 2:
            self.cursorIndice += 1
        if menu.cursorAbajo(evento) and self.cursorIndice > 1:
            self.cursorIndice -= 1

        cursorCarac = '-'
        img_letra3 = self.fuente.render(cursorCarac, True, (200, 200, 200))
        if self.cursorIndice == 1:
            superficie.blit(img_letra3, (self.cursor_x-20, self.cursor_y))
        if self.cursorIndice == 2:
            superficie.blit(img_letra3, (self.cursor_x-20, self.cursor_y+20))

        cad1 = 'Escribir'
        img_letra = self.fuente.render(cad1, True, (200, 200, 200))
        superficie.blit(img_letra, (self.pos_x, self.pos_y))

        cad2 = 'Salir'
        img_letra2 = self.fuente.render(cad2, True, (200, 200, 200))
        superficie.blit(img_letra2, (self.pos_x, self.pos_y + 20))



class Entrada():
    def __init__(self):
        self.lineas = 0
        self.cant = 0
        self.caracteres = [' ',]
        self.fuente = pygame.font.Font(None, 25)


        self.distancia = 20
        self.pos_x = 50
        self.pos_y = 50


    def teclas(self, evento, maxim):
        for accion in evento:
            #print('algo...')
            if accion.type == KEYDOWN:
                if accion.key == K_ESCAPE:
                    sys.exit(0)
                elif accion.key == K_BACKSPACE: #Borrado
                    self.caracteres[0] = self.caracteres[0][0:-1]
                    self.cant -= 1
                else:
                    if self.cant < maxim:
                        self.caracteres[0] = str(self.caracteres[0] + accion.unicode)
                        self.cant += 1

    def salirEscritura(self,evento):
        for accion in evento:
            if accion.type == KEYDOWN and accion.key == K_RETURN: #Enter
                return True
            else:
                return False

    def sacarTexto(self):
        return self.caracteres[0]

    def mensaje(self, superficie):
        superficie.fill((0, 0, 0))
        for self.lineas in range(len(self.caracteres)):
            img_letra = self.fuente.render(self.caracteres[0], True, (200, 200, 200))
            superficie.blit(img_letra, (self.pos_x, self.pos_y + self.distancia))



def main():
    
    pygame.init()
    pantalla = pygame.display.set_mode((700, 500))
    pygame.display.set_caption('Escribir en pygame')
    salir = False

    #parametros
    escribir = False
    cad = ''
    maximo = 8

    entrar_texto = Entrada()

    menuPri = menu()

    while not salir:
        eventos = pygame.event.get()
        for accion in eventos:
            if accion.type == pygame.QUIT:
                salir = True

    
        menuPri.texto(pantalla,eventos)

        for accion in eventos:
            if accion.type == KEYDOWN:
                if accion.key == K_F1 and menuPri.cursorIndice == 1:
                    escribir = True
                if accion.key == K_F1 and menuPri.cursorIndice == 2:
                    salir = True


        if escribir:
            cad = entrar_texto.sacarTexto()
            print(cad)
            entrar_texto.mensaje(pantalla)
            if entrar_texto.salirEscritura(eventos):
                escribir = False
                salir = True
            entrar_texto.teclas(eventos,maximo)
       
    

        pygame.display.update()

main()