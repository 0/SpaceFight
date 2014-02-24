import pymunk
import random

class GameObject():
    def __init__(self):
        self.force = pymunk.Vec2d(0,0)

    def update(self):
        self.setForce(self.force)
        self.force = pymunk.Vec2d.zero()

    def addBall(self,mass,radius,pos):
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
        body = pymunk.Body(mass, inertia)
        body.position = pos
        shape = pymunk.Circle(body, radius, (0,0))
        shape.elasticity = 0.75
        return shape

    def setVelocity(self,velocity):
        self.getBody().velocity = velocity

    def getVelocity(self):
        return self.getBody().velocity

    def setForce(self,f):
        self.getBody().force = f

    def addForce(self,f):
        self.force.x += f[0]
        self.force.y += f[1]

    def getForce(self):
        return self.entity.body.force

    def getBody(self):
        return self.entity.body

    def getShape(self):
        return self.entity

    def getPosition(self):
        return self.getBody().position

    def getAngle(self):
        return self.getBody().angle

    def getRadius(self):
        return self.getShape().radius

    def getMass(self):
        return self.getBody().mass

    def getAngularVelocity(self):
        return self.getBody().angular_velocity

    def reduceAngularVelocity(self):
        self.getBody().angular_velocity *= 0.93

    def addAngularVelocity(self,x):
        self.getBody().angular_velocity += x


class Bullet(GameObject):
    def __init__(self,pos):
        GameObject.__init__(self)

        self.entity = self.addBall(8,2,pos)


class Planetoid(GameObject):
    MIN_RADIUS = 20
    MAX_RADIUS = 35

    def __init__(self,pos):
        GameObject.__init__(self)

        radius = random.randint(self.MIN_RADIUS, self.MAX_RADIUS)
        mass = 12*radius*radius*random.randint(3,6)
        self.entity = self.addBall(mass,radius,pos)


class Asteroid(GameObject):
    MIN_RADIUS = 4
    MAX_RADIUS = 10

    def __init__(self,pos):
        GameObject.__init__(self)

        radius = random.randint(self.MIN_RADIUS, self.MAX_RADIUS)
        mass = 12*radius*radius*random.randint(1,4)
        self.entity = self.addBall(mass,radius,pos)


class Ship(GameObject):
    TURN_ACCELERATION = 0.35

    def __init__(self,p_num,angle,pos):
        GameObject.__init__(self)

        self.p_num = p_num

        if p_num == 1:
            self.entity = self.addPoly1(10,angle,pos)
        elif p_num == 2:
            self.entity = self.addPoly2(10,angle,pos)
        else:
            raise ValueError('Invalid player number: %d' % p_num)

    def getPlayerNumber(self):
        return self.p_num

    def addPoly1(self,mass,angle,pos):
        body = pymunk.Body(mass, mass*5)
        body.angle = angle
        body.position = pos
        shape = pymunk.Poly(body,[(0,15),(-5,-10),(0,-10),(5,-10)])
        shape.elasticity = 0.75
        return shape

    def addPoly2(self,mass,angle,pos):
        body = pymunk.Body(mass, mass*5)
        body.angle = angle
        body.position = pos
        shape = pymunk.Poly(body,[(0,15),(-7,0),(0,-7),(7,0)])
        shape.elasticity = 0.75
        return shape

    def getGun(self):
        return self.getShape().get_vertices()[3]

    def thrust(self):
        f = pymunk.Vec2d((self.getGun() - self.getShape().get_vertices()[1])).normalized()
        self.addForce(150 * f)

    def turnLeft(self):
        self.addAngularVelocity(self.TURN_ACCELERATION)

    def turnRight(self):
        self.addAngularVelocity(-self.TURN_ACCELERATION)

    def shoot(self):
        f = pymunk.Vec2d((self.getGun() - self.getShape().get_vertices()[1])).normalized()
        return 5500 * f
