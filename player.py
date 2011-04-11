import math
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
        return time.time() > self.shoot_cooldown
	
    def getVelocity(self):
        return self.ship.getVelocity()


class HumanPlayer(Player):
    def control(self, key, others):
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


class ComputerPlayer(Player):
    aim_tolerance = 0.2
    """Other player should be within this many radians on either side."""

    def control(self, key, others):
        other = others[0]

        if self.isAlive():
            # Full steam ahead!
            self.thrust()

            # Determine angle relative to other ship.
            target_vector = self.ship.getPosition() - other.ship.getPosition()
            target_angle = target_vector.get_angle()
            own_angle = (self.ship.getAngle() - math.pi / 2)
            relative_angle = (own_angle - target_angle) % (2 * math.pi)

            if (relative_angle > self.aim_tolerance and
                    relative_angle < (2 * math.pi - self.aim_tolerance)):
                # Take the line...
                if relative_angle > math.pi:
                    self.turnLeft()
                else:
                    self.turnRight()
            else:
                # ... and fire!
                if self.canShoot():
                    return [self.ship.getGun(), self.shoot(), self.getVelocity()]
