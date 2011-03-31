import gameobject
import time

class Player():

    def __init__(self,ship):
        self.ship = ship
        self.alive = True
        self.thrust_cooldown = time.time()
        self.turn_cooldown = time.time()
        self.shoot_cooldown = time.time()

    def isAlive(self):
        return self.alive

    def thrust(self):
        now = time.time()
        if time.time() > self.thrust_cooldown:
            self.thrust_cooldown = now + 0.2
            self.ship.thrust()
        
    def turnLeft(self):
        now = time.time()
        if time.time() > self.turn_cooldown:
            self.turn_cooldown = now + 0.2
            self.ship.turnLeft()
        
    def turnRight(self):
        now = time.time()
        if time.time() > self.turn_cooldown:
            self.turn_cooldown = now + 0.2
            self.ship.turnRight()

    def shoot(self):
        self.shoot_cooldown = time.time() + 0.6
        return self.ship.shoot()

    def canShoot(self):
        now = time.time()
        return (time.time() > self.shoot_cooldown)
