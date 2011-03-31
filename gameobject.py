import pymunk
import random

class GameObject():
    def __init__(self,objclass,angle,pos):
        self.object_class = objclass
        self.force = pymunk.Vec2d(0,0)
        if self.object_class == "Bullet":
            self.entity = self.addBall(8,2,pos)
        elif self.object_class == "Planetoid":
            radius = random.randint(20,35)
            mass = 12*radius*radius*random.randint(3,6)
            self.entity = self.addBall(mass,radius,pos)
        elif self.object_class == "Asteroid":
            radius = random.randint(4,10)
            mass = 12*radius*radius*random.randint(1,4)
            self.entity = self.addBall(mass,radius,pos)
        elif self.object_class == "Ship1":
            self.entity = self.addPoly1(10,angle,pos)
        elif self.object_class == "Ship2":
            self.entity = self.addPoly2(10,angle,pos)
            
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

    def getClass(self):
        return self.object_class

    def getPosition(self):
        return self.getBody()._get_position()

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

    def thrust(self):
        f = pymunk.Vec2d.normalized(
            pymunk.Vec2d(-(
                self.getShape().get_points()[1]-self.getShape().get_points()[3])))
        f = (f[0]*150,f[1]*150)
        self.addForce(f)
        
    def turnLeft(self):
        self.addAngularVelocity(1)
        
    def turnRight(self):
        self.addAngularVelocity(-1)


    def shoot(self):
        ship_v = self.getForce()
        f = pymunk.Vec2d.normalized(
            pymunk.Vec2d(-(
                self.getShape().get_points()[1]-self.getShape().get_points()[3])))
        f = (f[0]*5500+ship_v[0],f[1]*5500+ship_v[1])
        return f

    def getGun(self):
        return self.getShape().get_points()[3]
