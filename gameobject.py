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
        shape._set_elasticity(0.75)
        return shape

    def setVelocity(self,velocity):
        self.getBody()._set_velocity(velocity)

    def getVelocity(self):
        return self.getBody()._get_velocity()

    def setForce(self,f):
        self.getBody()._set_force(f)

    def addForce(self,f):
        self.force.x += f[0]
        self.force.y += f[1]

    def getForce(self):
        return self.entity.body._get_force()

    def getBody(self):
        return self.entity.body

    def getShape(self):
        return self.entity

    def getPosition(self):
        return self.getBody()._get_position()

    def getAngle(self):
        return self.getBody()._get_angle()

    def getRadius(self):
        return self.getShape()._get_radius()

    def getMass(self):
        return self.getBody()._get_mass()

    def getAngularVelocity(self):
        return self.getBody()._get_angular_velocity()

    def reduceAngularVelocity(self):
        self.getBody()._set_angular_velocity(self.getBody()._get_angular_velocity()*0.93)

    def addAngularVelocity(self,x):
        self.getBody()._set_angular_velocity(self.getAngularVelocity()+x)


class Bullet(GameObject):
    def __init__(self,pos):
        GameObject.__init__(self)

        self.entity = self.addBall(8,2,pos)


class Planetoid(GameObject):
    def __init__(self,pos):
        GameObject.__init__(self)

        radius = random.randint(20,35)
        mass = 12*radius*radius*random.randint(3,6)
        self.entity = self.addBall(mass,radius,pos)


class Asteroid(GameObject):
    def __init__(self,pos):
        GameObject.__init__(self)

        radius = random.randint(4,10)
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
        body._set_angle(angle)
        body.position = pos
        shape = pymunk.Poly(body,[(0,15),(-5,-10),(0,-10),(5,-10)])
        shape._set_elasticity(0.75)
        return shape

    def addPoly2(self,mass,angle,pos):
        body = pymunk.Body(mass, mass*5)
        body._set_angle(angle)
        body.position = pos
        shape = pymunk.Poly(body,[(0,15),(-7,0),(0,-7),(7,0)])
        shape._set_elasticity(0.75)
        return shape

    def thrust(self):
        f = pymunk.Vec2d.normalized(
            pymunk.Vec2d(-(
                self.getShape().get_points()[1]-self.getShape().get_points()[3])))
        f = (f[0]*150,f[1]*150)
        self.addForce(f)

    def turnLeft(self):
        self.addAngularVelocity(self.TURN_ACCELERATION)

    def turnRight(self):
        self.addAngularVelocity(-self.TURN_ACCELERATION)

    def shoot(self):
        ship_v = self.getVelocity()
        f = pymunk.Vec2d.normalized(
            pymunk.Vec2d(-(
                self.getShape().get_points()[1]-self.getShape().get_points()[3])))
        f = (f[0]*5500,f[1]*5500)
        return f

    def getGun(self):
        return self.getShape().get_points()[3]
