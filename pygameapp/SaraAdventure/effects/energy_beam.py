import pygame
import math

class EnergyBeam:
    def __init__(self, x, y, direction, color=(0, 191, 255)):
        self.x = x
        self.y = y
        self.direction = direction # 0: Down, 1: Left, 2: Right, 3: Up
        self.color = color
        self.lifetime = 1000 # 1 second duration
        self.start_time = pygame.time.get_ticks()
        self.alive = True
        self.max_length = 500
        self.width = 10
        self.growth_speed = 15

    def update(self, current_time):
        elapsed = current_time - self.start_time
        if elapsed > self.lifetime:
            self.alive = False
            return
        
        # Beam grows over time
        self.length = min(self.max_length, elapsed * self.growth_speed)
        # Fade out towards the end
        self.alpha = 255 if elapsed < 800 else max(0, 255 - (elapsed - 800) * 1.2)

    def draw(self, surface):
        if not self.alive: return
        
        # Calculate end point based on direction
        end_x, end_y = self.x, self.y
        if self.direction == 0: end_y += self.length # Down
        elif self.direction == 1: end_x -= self.length # Left
        elif self.direction == 2: end_x += self.length # Right
        elif self.direction == 3: end_y -= self.length # Up
        
        # Draw outer glow
        for i in range(3):
            w = self.width + (i * 4)
            s = pygame.Surface((max(abs(end_x - self.x), w), max(abs(end_y - self.y), w)), pygame.SRCALPHA)
            alpha = int(self.alpha / (i + 1))
            
            # Draw line on temporary surface to support alpha
            if self.direction in [1, 2]: # Horizontal
                pygame.draw.line(s, (*self.color, alpha), (0, w//2), (s.get_width(), w//2), w)
            else: # Vertical
                pygame.draw.line(s, (*self.color, alpha), (w//2, 0), (w//2, s.get_height()), w)
            
            # Find draw position
            dx = min(self.x, end_x) - (w//2 if self.direction not in [1,2] else 0)
            dy = min(self.y, end_y) - (w//2 if self.direction in [1,2] else 0)
            surface.blit(s, (dx, dy))
            
        # Draw white core
        pygame.draw.line(surface, (255, 255, 255, self.alpha), (self.x, self.y), (end_x, end_y), self.width // 2)
