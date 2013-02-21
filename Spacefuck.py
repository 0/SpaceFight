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
scanlines = scanline.Scanline(  cfg.scanlineSkip,
                                cfg.scanlineSpeed,
                                cfg.width,
                                cfg.height,
                                cfg.scanlineColor)

menu      = menu.Menu(resources)
game      = game.Game(resources,menu)
running   = 1
framerate = cfg.DEFAULT_FRAMERATE
background= resources.getBackground()

while(running):
    running += controls.update(menu,game)
    if (running == 1):
        #--------------------------
        #Render Background
        screen.blit(background,topleft)
        #--------------------------
        #Scanline
        screen.blit(scanlines.update(),topleft)
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
        clock.tick(framerate)
    else:
        pygame.time.wait(500)
pygame.quit()
