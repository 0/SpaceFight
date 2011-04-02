import pygame
import time

class Control():
    def __init__(self):
        pass
    
    def update(self,menu,game):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            return False
        
        if menu.isActive():
            self.menuControl(key,menu,game)
            
        elif game.isActive():
            self.gameControl(key,game,menu)
        
        return True

    def menuControl(self,key,menu,game):
        if menu.getMainMenu():
            if key[pygame.K_SPACE]:
                menu.briefing()
                self.next_press = time.time() + 0.35
            if not game.AI_mode and key[pygame.K_HOME]:
                menu.setText("^^AI Activated (Or it would be if it was implemented)")
                game.setAI_mode(True)
            if game.AI_mode and key[pygame.K_END]:
                menu.SetText("^^AI Deactivated (Or it would be if it was implemented)")
                game.setAI_mode(False)
        else:
            if time.time() > self.next_press:
                if key[pygame.K_SPACE]:
                    menu.setActive(False)
                    menu.clear()
                    game.setActive(True)
                    game.start()
            
    def gameControl(self,key,game,menu):
        if game.player1.isAlive():
            if key[pygame.K_w]:
                game.player1.thrust()
            if key[pygame.K_a]:
                game.player1.turnLeft()
            if key[pygame.K_d]:
                game.player1.turnRight()
            if key[pygame.K_LALT]:
                if game.player1.canShoot():
                    game.addBullet(game.player1.ship.getGun(),game.player1.shoot(),game.player1.getVelocity())
                
        if game.player2.isAlive():
            if key[pygame.K_i]:
               game.player2.thrust()
            if key[pygame.K_j]:
                game.player2.turnLeft()
            if key[pygame.K_l]:
                game.player2.turnRight()
            if key[pygame.K_RCTRL]:
                if game.player2.canShoot():
                    game.addBullet(game.player2.ship.getGun(),game.player2.shoot(),game.player2.getVelocity())
