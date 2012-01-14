#!/usr/bin/env python2

#Pygame Imports
import pygame
import control
import menu
import game

#Local Imports
import cfg
import loader
import scanline

#--------------------------
#Start
pygame.init()

#Pygame Initialization
pygame.display.set_icon(pygame.image.load("resources/Triangle.png"))
pygame.display.set_caption("Spacefuck")

mode_flags = 0
if cfg.fullscreen:
    mode_flags |= pygame.FULLSCREEN
screen = pygame.display.set_mode((cfg.width, cfg.height), mode_flags)

#Constants and Resource Objects
clock     = pygame.time.Clock()
topleft   = (0,0)

resources = loader.Load()
controls  = control.Control()
scanlines = scanline.Scanline(4, 2, cfg.width, cfg.height)

menu      = menu.Menu(resources)
game      = game.Game(resources,menu)

running   = True

while(running):
    #--------------------------
    #Render Background
    screen.blit(resources.getBackground(),topleft)
    #--------------------------
    #Scanline
    for line in scanlines.update():
        pygame.draw.line(screen,(24,30,24),line[0],line[1],1)
    #--------------------------
    #Control Events
    running = controls.update(menu,game)
    #--------------------------
    #States
    #----Menu and Text State
    if menu.isActive():
        screen.blit(menu.update(),topleft)
    #----Game State
    elif game.isActive():
         screen.blit(game.update(),topleft)
    #--------------------------
    #Final Rendering
    screen.blit(resources.getForeground(),topleft)
    pygame.display.flip()
    #--------------------------
    #Frame Control
    clock.tick(60)
pygame.quit()
