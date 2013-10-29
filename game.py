import pygame
import pymunk
import random
import time

import ai
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

#       pymunk.init_pymunk() # No longer needed: Latest version of pymunk self initializes.

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
        self.space.gravity = (0, 0)

        # The maximum asteroid density at which the game is still playable was
        # experimentally determined to be approximately 9% of the playing area,
        # regardless of its size or shape.
        max_area = 0.09 * self.boundaries.width * self.boundaries.height
        mean_radius = 0.5 * (gameobject.Asteroid.MIN_RADIUS +
                gameobject.Asteroid.MAX_RADIUS)
        max_planetoids = int(max_area / 3.14 / (mean_radius ** 2))
        num_planetoids = random.randint(0, max_planetoids)

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

        # Use a single obstacle about 10% of the time, in cases when less than
        # 1% of the playing area would be occupied by asteroids.
        if 10 * num_planetoids < max_planetoids:
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
                if not self.game_ships:
                    self.winner += "Nobody"
                for ship in self.game_ships:
                    self.winner += "Player " + str(ship.getPlayerNumber())
            self.active = False
            self.menu.setActive(True)
            self.menu.startMainMenu()
            self.menu.addText(self.winner+" Wins^--------^^"+self.menu.default())

    def genPlayer(self, p_num, pos, angle, AI_mode, keys):
        ship = self.addShip(p_num, pos, angle)

        if AI_mode:
            return ai.ComputerPlayer(ship, None)
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
        c_points = [self.to_pygame(point) for point in poly.get_vertices()]
        pygame.draw.lines(game_surface, (0,255,0), True, c_points, 1)

    def to_pygame(self,p):
        return int(p.x), int(-p.y + self.PYMUNK_HEIGHT)

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

    def update(self):

        self.space.step(0.08)
        self.game_surface.fill((0,0,0))

        if self.ending:
            self.end()

        if time.time() > self.sudden_death:

            self.sudden_deaths += 1
            self.space.gravity = (
                    (random.random() - 0.5) * 0.5 * self.sudden_deaths,
                    (random.random() - 0.5) * 0.5 * self.sudden_deaths)
            self.sudden_death += 8 + self.sudden_deaths
            self.menu.addText("Sudden Death: Round "
                              +str(self.sudden_deaths)+"^")


        for planetoid in self.game_planetoids:
            p = self.to_pygame(planetoid.getPosition())

            if not self.boundaries.collidepoint(p):
                self.burst(planetoid.getRadius(),planetoid.getPosition())
                self.game_planetoids.remove(planetoid)

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
