#Pygame Imports
import pygame
import control
import menu
import game

#Local Imports
import loader
import scanline

#--------------------------
#Start
pygame.init()

#Pygame Initialization
pygame.display.set_icon(pygame.image.load("Triangle.png"))
pygame.display.set_caption("Spacefuck")
screen    = pygame.display.set_mode((800,600))

#Constants and Resource Objects
clock     = pygame.time.Clock()
topleft   = (0,0)

to_render = pygame.Surface((800,600))

resources = loader.Load()
controls  = control.Control()
scanlines = scanline.Scanline(4,2,800,600)

menu      = menu.Menu(resources)
game      = game.Game(resources,menu)

running   = True

while(running):
    #--------------------------
    #Render Background
    to_render.blit(resources.getBackground(),topleft)
    #--------------------------
    #Scanline
    for line in scanlines.update():
        pygame.draw.line(to_render,(24,30,24),line[0],line[1],1)
    #--------------------------
    #Control Events
    running = controls.update(menu,game)
    #--------------------------
    #States
    #----Menu and Text State
    if menu.isActive():
        to_render.blit(menu.update(),topleft)
    #----Game State
    elif game.isActive():
         to_render.blit(game.update(),topleft)
    #--------------------------
    #Final Rendering
    to_render.blit(resources.getForeground(),topleft)
    screen.blit(to_render,topleft)
    pygame.display.flip()
    #--------------------------
    #Frame Control
    clock.tick(60)
pygame.quit()
