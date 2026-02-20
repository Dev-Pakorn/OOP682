import sys, os
import pygame 
from chars.sara import Hero
class SaraAdventure:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        self.caption = "Sara Adventure"
        self.hero = Hero('Sara','sara/sara-cal1.png',50,50)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("None", 24)

    def handle_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_text(self,text,position,color=(0,0,0)):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.hero.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.hero.rect.x += 5
        if keys[pygame.K_UP]:
            self.hero.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.hero.rect.y += 5

    
    def start(self):
        start = pygame.time.get_ticks()
        while True:
            self.handle_close()
            self.handle_input()
            self.screen.fill((255, 255, 255))
            self.draw_text("Sara Adventure!", (100, 100))
            elapsed_time = pygame.time.get_ticks() - start
            self.hero.update(elapsed_time)
            self.hero.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    game = SaraAdventure()
    game.start()