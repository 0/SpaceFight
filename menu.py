import pygame
import random
import time

import cfg

class Menu():
    def __init__(self,resources):
        #------------------------
        #Set Resources
        self.resources      = resources
        #------------------------
        #Create Menu Surface
        self.menu_surface   = pygame.Surface((cfg.width, cfg.height))
        self.menu_surface.convert()
        self.menu_surface.set_colorkey((0,0,0))
        #------------------------
        #Create Buffer Surface
        self.buffer_surface = pygame.Surface((cfg.width, cfg.height))
        self.buffer_surface.convert()
        self.buffer_surface.set_colorkey((0,0,0))
        #------------------------
        #Set Initial Parameters
        self.active         = True
        self.main_menu      = True
        self.initial_cursor = (cfg.border_thickness, cfg.height -
                cfg.border_thickness - self.resources.getFont().get_height())
        self.cursor         = self.initial_cursor
        # TODO: Run pygame.key.name on the actual key values.
        self.default_text   = "*********^Spacefuck^*********^^Space to Start^^Esc to Quit^^--------^Controls:^P1:^W: thrust^A: turn left^D: turn right^left alt: shoot^^P2:^I: thrust^J: turn left^L: turn right^right ctrl: shoot"
        self.text           = self.default_text
        self.next_type      = time.time()


    def update(self):
        if self.text:
            now = time.time()

            if now >= self.next_type:
                char = self.text[0]
                self.text = self.text[1:]

                if char == "^" or char =="\n":
                    self.buffer_surface.fill((0,0,0))
                    self.buffer_surface.blit(self.menu_surface,(0,-14))
                    self.cursorReturn()
                    self.next_type = now + 0.45

                else:
                    self.buffer_surface.blit(self.resources.getFont().render
                                   (char, True, (0,255,0),(0,0,0)),self.cursor)
                    self.cursorRight(1)
                    self.next_type = now + 0.05

                self.menu_surface.fill((0,0,0))
                self.menu_surface.blit(self.buffer_surface,(0,0))
        return self.menu_surface

    def isActive(self):
        return self.active

    def getMainMenu(self):
        return self.main_menu

    def startMainMenu(self):
        self.main_menu = True

    def setActive(self,active):
        self.active = active

    def setText(self, text):
        self.text = text

    def addText(self, text):
        self.text += text

    def cursorRight(self,n):
        self.cursor = (self.cursor[0]+(12*n),self.cursor[1])

    def cursorReturn(self):
        self.cursor = self.initial_cursor[0],self.cursor[1]

    def clear(self):
        self.buffer_surface.fill((0,0,0))
        self.menu_surface.fill((0,0,0))
        self.cursorReturn()
        self.text = ""

    def briefing(self):
        self.main_menu = False
        self.clear()
        titles = self.resources.getTitles()
        blurbs = self.resources.getBlurbs()
        self.addText(random.choice(titles))
        self.addText("^^") # Two line breaks.
        self.addText(random.choice(blurbs))

    def default(self):
        return self.default_text
