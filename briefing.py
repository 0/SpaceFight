import pygame

class Briefing():
    def __init__(self,resources):
        self.briefing_surface = pygame.Surface((800,600))
        self.briefing_surface.convert()
        self.briefing_surface.set_colorkey((0,0,0))

        self.active = False

        #self.current_string
        
    def update(self,controls):
        
        return self.briefing_surface

    def is_active(self):
        return self.active




        if time.time()>= nexttype and dtype:
            if len(string) > 1:
                char = string[0]
                string = string[1:]
                nexttype+=0.1
            elif len(string) == 1:
                char = string[0]
                string = ""
                nexttype+=0.1
            elif len(string) == 0:
                dtype = False
            if char == "^":
                textx=200
                texty+=14
                nexttype+=0.5
                line+=1
            else:
                textsurface.blit(thefont.render(char, True, (0,255,0),(0,0,0)),(textx,texty))
                textx+=12
        screen.blit(textsurface,(0,-14*line))
