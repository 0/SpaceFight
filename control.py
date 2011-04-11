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
            self.gameControl(key,game)
        
        return True

    def menuControl(self,key,menu,game):
        if menu.getMainMenu():
            if key[pygame.K_SPACE]:
                menu.briefing()
                self.next_press = time.time() + 0.35
            # TODO: There should be a better way of doing this.
            if not game.AI_mode[0] and key[pygame.K_q]:
                game.AI_mode[0] = True
                menu.setText("^^AI Activated for Player 1")
            if game.AI_mode[0] and key[pygame.K_w]:
                game.AI_mode[0] = False
                menu.setText("^^AI Deactivated for Player 1")
            if not game.AI_mode[1] and key[pygame.K_a]:
                game.AI_mode[1] = True
                menu.setText("^^AI Activated for Player 2")
            if game.AI_mode[1] and key[pygame.K_s]:
                game.AI_mode[1] = False
                menu.setText("^^AI Deactivated for Player 2")
        else:
            if time.time() > self.next_press:
                if key[pygame.K_SPACE]:
                    menu.setActive(False)
                    menu.clear()
                    game.setActive(True)
                    game.start()
            
    def gameControl(self,key,game):
        for i, p in enumerate(game.players):
            # Pass in the keys pressed for HumanPlayer and a list of other players for ComputerPlayer.
            bullet = p.control(key, game.players[:i] + game.players[i+1:])

            if bullet:
                game.addBullet(*bullet)
