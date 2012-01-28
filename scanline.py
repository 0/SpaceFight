import pygame

class Scanline():
    def __init__(self,skip,speed,width,height,color):
        self.line = 0
        self.offset = 0
        self.skip = skip
        self.speed = speed
        self.height = height
        self.width = width
        self.color = color
        self.line_surface = pygame.Surface((width, height))
        self.line_surface.convert_alpha()
        self.line_surface.set_colorkey((0,0,0))
        
    def update(self):
        self.line_surface.fill((0,0,0))
        for _ in xrange(self.speed):
            pygame.draw.line(self.line_surface,self.color,(0,self.line),(self.width,self.line),1)
            self.line+= self.skip
            if self.line > self.height:
                self.offset+=1
                self.line = self.offset
            if self.offset == self.skip:
                self.offset = 0
                
        #pygame.draw.line(self.line_surface,self.color,line[0],line[1],1)
        return self.line_surface
