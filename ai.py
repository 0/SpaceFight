import math
import player
import pymunk


class ComputerPlayer(player.Player):
    AIM_TOLERANCE = 0.2
    """Other player should be within this many radians on either side."""

    STABILIZATION_CREEP_TOLERANCE = 0.3
    """When trying to keep still, ignore velocities of magnitude up to this."""

    def control(self, key, others):
        if not self.isAlive():
            return

        alive_others = [x for x in others if x.isAlive()]
        if alive_others:
            other = alive_others[0]
        else:
            other = None

        if other:
            # Full steam ahead!
            self.thrust()

            # Determine angle relative to other ship.
            target_vector = self.ship.getPosition() - other.ship.getPosition()
            target_angle = target_vector.get_angle()
            own_angle = (self.ship.getAngle() - math.pi / 2)
            relative_angle = (own_angle - target_angle) % (2 * math.pi)

            if (relative_angle > self.AIM_TOLERANCE and
                    relative_angle < (2 * math.pi - self.AIM_TOLERANCE)):
                # Take the line...
                if relative_angle > math.pi:
                    self.turnLeft()
                else:
                    self.turnRight()
            else:
                # ... and fire!
                if self.canShoot():
                    return [self.ship.getGun(), self.shoot(), self.getVelocity()]
        else:
            # Stabilize.
            v = self.ship.getVelocity()

            if v.get_length() > self.STABILIZATION_CREEP_TOLERANCE:
                own_angle = pymunk.Vec2d().unit()
                own_angle.rotate(self.ship.getAngle())

                # Rotate opposite to the direction of motion.
                desired_angle = v.rotated(math.pi)
                angle_difference = own_angle.get_angle_between(desired_angle)

                if angle_difference > 0:
                    self.turnLeft()
                elif angle_difference < 0:
                    self.turnRight()

                self.thrust()
