import pygame

class Load():

    def __init__(self):
        self.text()
        self.images()

    def text(self):
        self.font      = self.loadFont()
        self.titles    = self.loadTitles()
        self.blurbs    = self.loadBlurbs()
        
    def loadFont(self):
        return pygame.font.Font("Font.ttf",12)

    def loadTitles(self):
        titles = []
        for line in open("titles.txt","r"):
            titles.append(line)
        return titles
    
    def getFont(self):
        return self.font

    def getTitles(self):
        return self.titles
    
    def getBlurbs(self):
        return self.blurbs
    
    def loadBlurbs(self):
        blurbs = []
        for line in open("blurbs.txt","r"):
            blurbs.append(line)
        return blurbs

    def images(self):
        self.foreground= self.loadForeground()
        self.background= self.loadBackground()
        #self.triangle  = self.loadTriangle()
        #self.circle    = self.loadCircle()
        #self.dot       = self.loadDot()


    def loadForeground(self):
        border = pygame.Surface((800,600),pygame.SRCALPHA,32)
        border.blit(pygame.image.load("Top.png"),(0,0))
        border.blit(pygame.image.load("Bottom.png"),(0,500))
        border.blit(pygame.image.load("Left.png"),(0,0))
        border.blit(pygame.image.load("Right.png"),(700,0))
        border = border.convert_alpha()
        return border

    def loadBackground(self):
        background = pygame.Surface((800,600),pygame.SRCALPHA,32)
        background.blit(pygame.image.load("Back.png"),(0,0))
        background = background.convert()
        background.set_alpha(55)
        return background

    def loadTriangle(self):
        triangle = pygame.Surface((40,40),pygame.SRCALPHA|pygame.RLEACCEL,32)
        triangle.blit(pygame.image.load("Triangle.png"),(0,0))
        triangle = triangle.convert_alpha()
        return triangle

    def loadCircle(self):
        circle = pygame.Surface((40,40),pygame.SRCALPHA|pygame.RLEACCEL,32)
        circle.blit(pygame.image.load("Circle.png"),(0,0))
        circle = circle.convert_alpha()
        return circle

    def loadDot(self):
        dot = pygame.Surface((6,6),pygame.SRCALPHA|pygame.RLEACCEL,32)
        dot.blit(pygame.image.load("Dot.png"),(0,0))
        dot = dot.convert_alpha()
        return dot

    def getBackground(self):
        return self.background

    def getForeground(self):
        return self.foreground
