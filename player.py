import gameobject
import time

class Player():

    def __init__(self,ship,keys):
        self.ship = ship
        self.keys = keys
        self.alive = True
        self.thrust_cooldown = time.time()
        self.turn_cooldown = time.time()
        self.shoot_cooldown = time.time()

    def isAlive(self):
        return self.alive

    def thrust(self):
        now = time.time()
        if time.time() > self.thrust_cooldown:
            self.thrust_cooldown = now + 0.3
            self.ship.thrust()
        
    def turnLeft(self):
        now = time.time()
        if time.time() > self.turn_cooldown:
            self.turn_cooldown = now + 0.05
            self.ship.turnLeft()
        
    def turnRight(self):
        now = time.time()
        if time.time() > self.turn_cooldown:
            self.turn_cooldown = now + 0.05
            self.ship.turnRight()

    def shoot(self):
        self.shoot_cooldown = time.time() + 0.6
        return self.ship.shoot()

    def canShoot(self):
        now = time.time()
        return (time.time() > self.shoot_cooldown)
	
    def getVelocity(self):
        return self.ship.getVelocity()


class HumanPlayer(Player):
    def control(self, key):
        if self.isAlive():
            if key[self.keys['thrust']]:
                self.thrust()
            if key[self.keys['left']]:
                self.turnLeft()
            if key[self.keys['right']]:
                self.turnRight()
            if key[self.keys['shoot']]:
                if self.canShoot():
                    return [self.ship.getGun(), self.shoot(), self.getVelocity()]
