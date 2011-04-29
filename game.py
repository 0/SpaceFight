import pygame
import pymunk
import random
import time

import cfg
import gameobject
import player

class Game():
    # TODO: Should place this somewhere better.
    keys = [{'thrust': pygame.K_w, 'left': pygame.K_a, 'right': pygame.K_d,
             'shoot': pygame.K_LALT},
            {'thrust': pygame.K_i, 'left': pygame.K_j, 'right': pygame.K_l,
             'shoot': pygame.K_RCTRL}]

    # XXX: Why 1000?
    PYMUNK_HEIGHT = 1000

    def __init__(self,resources,menu):
        self.menu = menu

        self.resources = resources

        self.game_surface = pygame.Surface((cfg.width, cfg.height))
        self.game_surface.convert_alpha()
        self.game_surface.set_colorkey((0,0,0))

        self.active = False

        pymunk.init_pymunk()

        border_ratio = (float(cfg.border_thickness) /
                cfg.DEFAULT_BORDER_THICKNESS)
        edge_distances = dict([(k, int(v * border_ratio)) for (k, v) in
                cfg.DEFAULT_BOUNDS.items()])

        self.boundaries = pygame.Rect(edge_distances['left'],
                edge_distances['top'],
                cfg.width - edge_distances['left'] - edge_distances['right'],
                cfg.height - edge_distances['top'] - edge_distances['bottom'])
        self.bullet_boundaries = pygame.Rect(0, 0, cfg.width, cfg.height)

        # TODO: Associate with the Player objects.
        self.AI_mode = [False, False]

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

        num_planetoids = random.randint(0,90)

        # Starting coordinates within the boundaries rectangle.
        startx = random.randint(0, self.boundaries.width / 2)
        starty = random.randint(0, self.boundaries.height)

        # Absolute (pymunk) starting coordinates.
        p1_pos = (self.boundaries.x + startx,
                  self.PYMUNK_HEIGHT - self.boundaries.y - starty)
        p2_pos = (self.boundaries.x + self.boundaries.width - startx,
                  self.PYMUNK_HEIGHT - self.boundaries.y -
                  self.boundaries.height + starty)

        self.players = [] # "Player 1" will be the 0th player.
        self.players.append(self.genPlayer(1, p1_pos, random.random() * 6.28,
            self.AI_mode[0], self.keys[0]))
        self.players.append(self.genPlayer(2, p2_pos, random.random() * 6.28,
            self.AI_mode[1], self.keys[1]))

        if num_planetoids <= 10:
            startx = self.boundaries.x + self.boundaries.width / 2
            starty = self.PYMUNK_HEIGHT - (self.boundaries.y +
                    self.boundaries.height / 2)
            self.addPlanetoid((startx, starty))
        else:
            for _ in xrange(num_planetoids):
                startx = (self.boundaries.x +
                        random.randint(0, self.boundaries.width))
                starty = self.PYMUNK_HEIGHT - (self.boundaries.y +
                        random.randint(0, self.boundaries.height))
                self.addAsteroid((startx,starty))

    def end(self):
        if time.time()> self.endtime:
            if self.winner == "":
                if len(self.game_ships) == 0:
                    self.winner += "Nobody"
                for ship in self.game_ships:
                    self.winner += "Player " + str(ship.getPlayerNumber())
            self.active = False
            self.menu.setActive(True)
            self.menu.startMainMenu()
            self.menu.addText(self.winner+" Wins^--------^^"+self.menu.default())

    def genPlayer(self, p_num, pos, angle, ai, keys):
        ship = self.addShip(p_num, pos, angle)

        if ai:
            return player.ComputerPlayer(ship, None)
        else:
            return player.HumanPlayer(ship, keys)

    def isActive(self):
        return self.active

    def setActive(self,active):
        self.active = active

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
        return int(p.x), int(-p.y + self.PYMUNK_HEIGHT)

    def to_pygame2(self,p):
        return int(p[0]), int(-p[1] + self.PYMUNK_HEIGHT)

    def burst(self,x,pos):
        for _ in xrange(int(x)):
            self.addBullet(pos,
                           (90*random.randint(-40,39)+1,
                            90*random.randint(-40,40)+1),
                           (0,0))

    def addShip(self,p_num,pos,angle):
        ship = gameobject.Ship(p_num,angle,pos)
        self.game_ships.append(ship)
        self.space.add(ship.getBody(),ship.getShape())
        return ship

    def addBullet(self,pos,impulse,velocity):
        bullet = gameobject.Bullet(pos)
        bullet.setVelocity(velocity)
        bullet.addForce(impulse)
        self.game_bullets.append(bullet)
        self.space.add(bullet.getBody(),bullet.getShape())
        return bullet

    def addPlanetoid(self, pos):
        planetoid = gameobject.Planetoid(pos)
        self.game_planetoids.append(planetoid)
        self.space.add(planetoid.getBody(),planetoid.getShape())
        return planetoid

    def addAsteroid(self, pos):
        asteroid = gameobject.Asteroid(pos)
        self.game_planetoids.append(asteroid)
        self.space.add(asteroid.getBody(),asteroid.getShape())
        return asteroid

    def applyGravity(self,obj1,obj2):
        obj1p    = obj1.getPosition()
        obj2p    = obj2.getPosition()
        distance = max(1, obj1p.get_dist_sqrd(obj2p))
        force    = ((obj1.getMass() * obj2.getMass()) / distance)*0.05
        f        = pymunk.Vec2d((obj1p[0]-obj2p[0]),(obj1p[1]-obj2p[1])).normalized()
        g        = (f[0]*force,f[1]*force)
        obj1.addForce(g)
        obj2.addForce(g)

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
                    ship.player.die()
                    self.ending = True
                    self.endtime = time.time() + 3


            else:
                self.drawPoly(ship,self.game_surface)

        self.drawBoundaries()

        self.drawText()

        return self.game_surface
