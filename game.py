import pygame
import pymunk
import gameobject
import random
import player
import menu
import time

class Game():
    def __init__(self,resources,menu):
        self.menu = menu

        self.resources = resources
        
        self.game_surface = pygame.Surface((800,600))
        self.game_surface.convert_alpha()
        self.game_surface.set_colorkey((0,0,0))

        self.active = False

        pymunk.init_pymunk()

        self.boundaries = pygame.Rect(75,50,650,480)
        self.bullet_boundaries = pygame.Rect(0,0,800,600)

        self.AI_mode = False

    def start(self):
        self.ending = False
        self.game_ships = []
        self.game_bullets = []
        self.game_planetoids = []

        self.sudden_death = time.time()+45
        self.sudden_deaths = 0

        self.winner = ""

        self.space = pymunk.Space()
        self.space._set_gravity((0,0))
        
        num_planetoids = random.randint(0,60)

        startx = random.randint(150,200)
        starty = random.randint(550,900)
        
        self.player1 = player.Player(self.addShip("Ship1",
            (startx,starty),
            random.randint(0,360)))
        self.player2 = player.Player(self.addShip("Ship2",
            (800-startx,1450-starty),
            random.randint(0,360)))
        if num_planetoids <= 10:
            startx = 400
            starty = 700
            self.addPlanetoid((startx,starty))
        else:
            for x in range(0,num_planetoids):
                startx = random.randint(100,700)
                starty = random.randint(550,850)
                self.addAsteroid((startx,starty))

    def end(self):
        if time.time()> self.endtime:
            if self.winner == "":
                if len(self.game_ships) == 0:
                    self.winner += "Nobody"
                for ship in self.game_ships:
                    self.winner += ship.getClass().replace("Ship","Player")
            self.active = False
            self.menu.setActive(True)
            self.menu.startMainMenu()
            self.menu.addText(self.winner+" Wins^--------^^"+self.menu.default())
            
        
    def isActive(self):
        return self.active

    def setActive(self,active):
        self.active = active
    def setAI_mode(self,active):
        self.AI_mode = active

    def drawBall(self, game_object,game_surface):
        ball = game_object.getShape()
        pos = self.to_pygame(ball.body.position)
        pygame.draw.circle(game_surface, (0,255,0), pos, int(ball.radius), 1)

    def drawBoundaries(self):
        pygame.draw.rect(self.game_surface, (0,255,0), self.boundaries, 1)

    def drawText(self):
        self.game_surface.blit(self.menu.update(),(0,0))

    def drawPoly(self, game_object,game_surface):
        poly = game_object.getShape()
        i_points = poly.get_points()
        c_points = []
        for point in i_points:
            c_points.append(self.to_pygame2(point))
        pygame.draw.lines(game_surface, (0,255,0), True, c_points, 1)

    def distance(self, obj1,obj2):
        return pow((pow((obj2[0]-obj1[0]),2)+pow((obj2[0]-obj1[0]),2)),0.5)
        
    def to_pygame(self,p):
        return int(p.x), int(-p.y+1000)
    
    def to_pygame2(self,p):
        return int(p[0]), int(-p[1]+1000)

    def burst(self,x,pos):
        for i in range(0,int(x)):
            bullet = self.addBullet(pos,
                                    (90*random.randint(-40,39)+1,
                                     90*random.randint(-40,40)+1))

    def addShip(self,name,pos,angle):
        ship = gameobject.GameObject(name,angle,pos)
        self.game_ships.append(ship)
        self.space.add(ship.getBody(),ship.getShape())
        return ship

    def addBullet(self,pos,impulse):
        bullet = gameobject.GameObject("Bullet",0,pos)
        bullet.addForce(impulse)
        self.game_bullets.append(bullet)
        self.space.add(bullet.getBody(),bullet.getShape())
        return bullet

    def addPlanetoid(self, pos):
        planetoid = gameobject.GameObject("Planetoid",0,pos)
        self.game_planetoids.append(planetoid)
        self.space.add(planetoid.getBody(),planetoid.getShape())
        return planetoid
    
    def addAsteroid(self, pos):
        asteroid = gameobject.GameObject("Asteroid",0,pos)
        self.game_planetoids.append(asteroid)
        self.space.add(asteroid.getBody(),asteroid.getShape())
        return asteroid

    def applyGravity(self,obj1,obj2):
        obj1p    = obj1.getPosition()
        obj2p    = obj2.getPosition()
        distance = max([1,pymunk.Vec2d.get_dist_sqrd(obj1p,obj2p)])
        force    = ((obj1.getMass() * obj2.getMass()) / distance)*0.05
        r        = (0,0)
        f        = pymunk.Vec2d.normalized(pymunk.Vec2d((obj1p[0]-obj2p[0]),(obj1p[1]-obj2p[1])))
        f        = (f[0]*force,f[1]*force)
        obj1.addForce(f)
        obj2.addForce(f)
        
    def update(self):
        
        self.space.step(0.08)
        self.game_surface.fill((0,0,0))

        if self.ending:
            self.end()

        if time.time() > self.sudden_death:
            
            self.sudden_deaths += 1
            self.space._set_gravity(
                ((random.random()-0.5)*0.5*self.sudden_deaths,
                 (random.random()-0.5)*0.5*self.sudden_deaths))
            self.sudden_death += 8 + self.sudden_deaths
            self.menu.addText("Sudden Death: Round "
                              +str(self.sudden_deaths)+"^")
 

        for planetoid in self.game_planetoids:
            p = self.to_pygame(planetoid.getPosition())   

            if not self.boundaries.collidepoint(p):
                self.burst(planetoid.getRadius(),planetoid.getPosition())
                self.game_planetoids.remove(planetoid)
                    
##            else:
##                for other_object in self.game_ships:
##                    self.applyGravity(planetoid,other_object)
                    
##                for other_object in self.game_planetoids:
##                    self.applyGravity(planetoid,other_object)
                    
##                for other_object in self.game_bullets:
##                    self.applyGravity(planetoid,other_object)
                    
            self.drawBall(planetoid,self.game_surface)
        
        for bullet in self.game_bullets:
            bullet.update()
            p = self.to_pygame(bullet.getBody().position)

            if not self.bullet_boundaries.collidepoint(p):
                self.game_bullets.remove(bullet)
                    
            else:
                self.drawBall(bullet,self.game_surface)
                    
        for ship in self.game_ships:
            ship.update()
            ship.reduceAngularVelocity()
            p = self.to_pygame(ship.getBody().position)
            
            if not self.boundaries.collidepoint(p):
                    self.burst(30,ship.getPosition())
                    self.game_ships.remove(ship)
                    self.ending = True
                    self.endtime = time.time() + 3

                    
            else:
                self.drawPoly(ship,self.game_surface)
            
        self.drawBoundaries()

        self.drawText()
        
        return self.game_surface