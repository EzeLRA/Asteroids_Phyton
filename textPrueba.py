# Imports
import sys
import pygame
import math
from functions import Rotate

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))


letra = pygame.font.Font("Resources/Font/pixelmix.ttf",42)

pygame.key.set_repeat(10)

running = True

# Game loop.
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    letra30 = pygame.font.SysFont("Arial", 30)                       
    imagenTextoPresent = letra30.render('Texto',True, (200,200,200), (0,0,0))                               
    rectanguloTextoPresent = imagenTextoPresent.get_rect()          
    rectanguloTextoPresent.centerx = screen.get_rect().centerx
    rectanguloTextoPresent.centery = screen.get_rect().centery  

    texto = letra.render("Hola , Saludos",True,"White")
    screen.blit(texto,(20,20))

    screen.blit(imagenTextoPresent, rectanguloTextoPresent)

    pygame.display.flip()
    fpsClock.tick(fps)

pygame.quit()