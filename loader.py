import pygame

import cfg

class Load():

    def __init__(self):
        self.text()
        self.images()

    def text(self):
        self.font      = self.loadFont()
        self.titles    = self.loadTitles()
        self.blurbs    = self.loadBlurbs()

    def loadFont(self):
        return pygame.font.Font("resources/Font.ttf",12)

    def loadTitles(self):
        return open("resources/titles.txt", "r").readlines()

    def getFont(self):
        return self.font

    def getTitles(self):
        return self.titles

    def getBlurbs(self):
        return self.blurbs

    def loadBlurbs(self):
        return open("resources/blurbs.txt", "r").readlines()

    def images(self):
        self.foreground= self.loadForeground()
        self.background= self.loadBackground()
        #self.triangle  = self.loadTriangle()
        #self.circle    = self.loadCircle()
        #self.dot       = self.loadDot()

    def loadForeground(self):
        border = pygame.Surface((cfg.width, cfg.height),pygame.SRCALPHA,32)

        # Since the border looks fine when stretched longitudinally, but not
        # when compressed, try to keep the aspect ratio correct for the side
        # which has been shrunk more.
        side_ratios = [float(cfg.width) / cfg.DEFAULT_WIDTH,
                       float(cfg.height) / cfg.DEFAULT_HEIGHT,
                       1] # But don't exceed the default size.
        thickness = int(min(side_ratios) * cfg.DEFAULT_BORDER_THICKNESS)
        cfg.border_thickness = thickness

        sizes = {'corner': (thickness, thickness),
                 'horiz': (cfg.width - 2 * thickness, thickness),
                 'vert': (thickness, cfg.height - 2 * thickness)}
        pieces = [("NW", 'corner', (0, 0)),
                  ("N", 'horiz', (thickness, 0)),
                  ("NE", 'corner', (cfg.width - thickness, 0)),
                  ("W", 'vert', (0, thickness)),
                  ("E", 'vert', (cfg.width - thickness, thickness)),
                  ("SW", 'corner', (0, cfg.height - thickness)),
                  ("S", 'horiz', (thickness, cfg.height - thickness)),
                  ("SE", 'corner', (cfg.width - thickness,
                                    cfg.height - thickness))]

        for location, kind, coords in pieces:
            img = pygame.image.load("resources/border/%s.png" % (location))
            img_scaled = pygame.transform.scale(img, sizes[kind])
            border.blit(img_scaled, coords)

        return border.convert_alpha()

    def loadBackground(self):
        back = pygame.image.load("resources/Back.png")
        background = pygame.transform.scale(back, (cfg.width, cfg.height))
        background = background.convert()
        background.set_alpha(55)
        return background

    def loadTriangle(self):
        triangle = pygame.Surface((40,40),pygame.SRCALPHA|pygame.RLEACCEL,32)
        triangle.blit(pygame.image.load("resources/Triangle.png"),(0,0))
        triangle = triangle.convert_alpha()
        return triangle

    def loadCircle(self):
        circle = pygame.Surface((40,40),pygame.SRCALPHA|pygame.RLEACCEL,32)
        circle.blit(pygame.image.load("resources/Circle.png"),(0,0))
        circle = circle.convert_alpha()
        return circle

    def loadDot(self):
        dot = pygame.Surface((6,6),pygame.SRCALPHA|pygame.RLEACCEL,32)
        dot.blit(pygame.image.load("resources/Dot.png"),(0,0))
        dot = dot.convert_alpha()
        return dot

    def getBackground(self):
        return self.background

    def getForeground(self):
        return self.foreground
