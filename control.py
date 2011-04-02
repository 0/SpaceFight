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
        for p in game.players:
            bullet = p.control(key)

            if bullet:
                game.addBullet(*bullet)
