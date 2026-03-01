import pygame
import math
from pygame.sprite import Sprite

class Hero(Sprite):
    def __init__(self, name, filename, x, y, rows=4, cols=4, target_size=(48, 48)):
        super().__init__()
        self.name = name
        self.sheet = pygame.image.load(filename).convert()
        # Set colorkey for transparency (Explicitly White)
        self.sheet.set_colorkey((255, 255, 255))
        self.rows = rows
        self.cols = cols
        
        # Calculate frame size from image and rows/cols
        img_width, img_height = self.sheet.get_size()
        self.frame_width = img_width // cols
        self.frame_height = img_height // rows
        
        self.target_size = target_size
        self.row = self.col = 0
        self.rect = pygame.Rect(x, y, target_size[0], target_size[1])
        self.last_update = 0
        self.carried_item = None
        self.victory_mode = False
        self.bounce_offset = 0
        
        # Special Power attributes
        self.is_dashing = False
        self.aura_pulse = 0
        self.after_images = [] # Store (surface, rect, alpha)
        
        # Attack attributes
        self.attack_state = "IDLE" # IDLE, CHARGING, FIRING
        self.attack_start_time = 0
        self.charge_duration = 500 # 0.5s to charge
        
        # HP and Damage
        self.hp = 100
        self.max_hp = 100
        self.invincible_timer = 0 # i-frames after being hit
        self.alpha_pulse = 255 # for blinking effect

    def act(self):
        pass

    def take_damage(self, amount, current_time):
        if current_time > self.invincible_timer:
            self.hp = max(0, self.hp - amount)
            self.invincible_timer = current_time + 1000 # 1s invincibility
            return True # took damage
        return False

    def start_attack(self, current_time):
        if self.attack_state == "IDLE":
            self.attack_state = "CHARGING"
            self.attack_start_time = current_time

    def update(self, current_time, moving=False, dashing=False):
        self.is_dashing = dashing
        
        # Handle Invincibility Blinking
        if current_time < self.invincible_timer:
            self.alpha_pulse = (math.sin(current_time * 0.05) + 1) / 2 * 128 + 127
        else:
            self.alpha_pulse = 255

        # Update Aura pulse
        self.aura_pulse = (math.sin(current_time * 0.005) + 1) / 2 # 0 to 1

        if self.victory_mode:
            self.bounce_offset = math.sin(current_time * 0.01) * 10
            self.col = 0
            return

        # Handle Attack States
        if self.attack_state == "CHARGING":
            if current_time - self.attack_start_time > self.charge_duration:
                self.attack_state = "FIRING"
            return # Don't move or animate normally while charging
        
        if self.attack_state == "FIRING":
            if current_time - self.attack_start_time > self.charge_duration + 800:
                self.attack_state = "IDLE"
            return # Don't move while firing

        # Handle animation timing
        anim_speed = 75 if self.is_dashing else 150
        if moving and current_time - self.last_update > anim_speed:
            self.col = (self.col + 1) % self.cols
            self.last_update = current_time
        elif not moving:
            self.col = 0 # Idle frame

        # Handle After-images for Dash
        if self.is_dashing and moving:
            frame_rect = pygame.Rect(self.col * self.frame_width, self.row * self.frame_height, self.frame_width, self.frame_height)
            frame = self.sheet.subsurface(frame_rect)
            scaled_frame = pygame.transform.scale(frame, self.target_size)
            self.after_images.append({
                'surf': scaled_frame,
                'rect': self.rect.copy(),
                'alpha': 150
            })
        
        # Update/Fade after-images
        for img in self.after_images[:]:
            img['alpha'] -= 15
            if img['alpha'] <= 0:
                self.after_images.remove(img)

    def draw_aura(self, surface, draw_rect):
        aura_color = (0, 191, 255) # Deep Sky Blue
        radius = int(25 + self.aura_pulse * 10)
        alpha = int(100 + self.aura_pulse * 100)
        
        aura_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(aura_surf, (*aura_color, alpha), (radius, radius), radius, 3)
        pygame.draw.circle(aura_surf, (*aura_color, alpha // 2), (radius, radius), radius - 5)
        
        aura_rect = aura_surf.get_rect(midbottom=draw_rect.midbottom)
        aura_rect.y += 5
        surface.blit(aura_surf, aura_rect)

    def draw_charge_effect(self, surface, draw_rect):
        if self.attack_state == "CHARGING":
            # Glow in palm/center
            charge_color = (255, 255, 255)
            # Pulse intensity
            pulse = (math.sin(pygame.time.get_ticks() * 0.05) + 1) / 2
            radius = int(5 + pulse * 15)
            
            glow_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (0, 191, 255, 150), (radius * 2, radius * 2), radius * 2)
            pygame.draw.circle(glow_surf, (255, 255, 255, 200), (radius * 2, radius * 2), radius)
            
            # Position at center/chest area for charging
            glow_rect = glow_surf.get_rect(center=draw_rect.center)
            surface.blit(glow_surf, glow_rect)

    def draw(self, surface):
        draw_rect = self.rect.copy()
        draw_rect.y += self.bounce_offset

        # 1. Draw Magic Aura
        self.draw_aura(surface, draw_rect)

        # 2. Draw After-images
        for img in self.after_images:
            img_surf = img['surf'].copy()
            img_surf.set_alpha(img['alpha'])
            surface.blit(img_surf, img['rect'])

        # 3. Draw Main Character
        # If charging, maybe use a specific row or just stay idle
        frame_rect = pygame.Rect(self.col * self.frame_width, self.row * self.frame_height, self.frame_width, self.frame_height)
        frame = self.sheet.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, self.target_size)
        
        # Apply invincibility blinking
        scaled_frame.set_alpha(self.alpha_pulse)
        surface.blit(scaled_frame, draw_rect)
        
        # 3.5 Draw Charge Effect
        self.draw_charge_effect(surface, draw_rect)

        # 4. Draw carried item
        if self.carried_item:
            item_size = (int(self.target_size[0]*0.8), int(self.target_size[1]*0.8))
            scaled_item = pygame.transform.scale(self.carried_item, item_size)
            item_rect = scaled_item.get_rect(midbottom=draw_rect.midtop)
            item_rect.y += 10
            surface.blit(scaled_item, item_rect)