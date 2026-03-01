import pygame
import random
from pygame.sprite import Sprite

class Monster(Sprite):
    def __init__(self, filename, x, y, target_size=(48, 48)):
        super().__init__()
        self.sheet = pygame.image.load(filename).convert()
        # Set colorkey for transparency (Explicitly White)
        self.sheet.set_colorkey((255, 255, 255))
        
        self.rows = 4
        self.cols = 4
        img_width, img_height = self.sheet.get_size()
        self.frame_width = img_width // self.cols
        self.frame_height = img_height // self.rows
        
        self.target_size = target_size
        self.rect = pygame.Rect(x, y, target_size[0], target_size[1])
        
        self.row = 0 # Down
        self.col = 0
        self.last_update = 0
        self.hp = 100
        self.alive = True
        self.speed = 2
        
        # AI attributes
        self.move_timer = 0
        self.move_dir = random.randint(0, 3) # 0:D, 1:L, 2:R, 3:U

    def update(self, current_time):
        if not self.alive: return
        
        # Random Movement AI
        if current_time - self.move_timer > random.randint(1000, 3000):
            self.move_dir = random.randint(0, 3)
            self.move_timer = current_time
            self.row = self.move_dir
            
        # Apply movement
        if self.move_dir == 0: self.rect.y += self.speed
        elif self.move_dir == 1: self.rect.x -= self.speed
        elif self.move_dir == 2: self.rect.x += self.speed
        elif self.move_dir == 3: self.rect.y -= self.speed
        
        # Keep in bounds (rough map bounds - will be updated in main)
        self.rect.x = max(0, min(self.rect.x, 2000))
        self.rect.y = max(0, min(self.rect.y, 2000))

        # Animation
        if current_time - self.last_update > 200:
            self.col = (self.col + 1) % self.cols
            self.last_update = current_time

    def check_player_collision(self, player, current_time):
        if not self.alive: return
        if self.rect.colliderect(player.rect):
            if player.take_damage(10, current_time):
                # Simple knockback - move monster away slightly
                if self.move_dir == 0: self.rect.y -= 20
                elif self.move_dir == 1: self.rect.x += 20
                elif self.move_dir == 2: self.rect.x -= 20
                elif self.move_dir == 3: self.rect.y += 20

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def draw(self, surface):
        if not self.alive: return
        
        # Extract frame
        frame_rect = pygame.Rect(self.col * self.frame_width, self.row * self.frame_height, self.frame_width, self.frame_height)
        frame = self.sheet.subsurface(frame_rect)
        
        # Scale
        scaled_frame = pygame.transform.scale(frame, self.target_size)
        surface.blit(scaled_frame, self.rect)
        
        # HP Bar (small)
        bar_width = self.target_size[0]
        bar_height = 5
        hp_width = (self.hp / 100) * bar_width
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, hp_width, bar_height))
