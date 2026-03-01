import sys, os, random
import pygame 
from chars.sara import Hero
from maps import LayeredMap
from effects.energy_beam import EnergyBeam
from chars.monster import Monster

class SaraAdventure:
    def __init__(self):
        pygame.init()
        self.tile_size = 32
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.caption = "Sarah Adventure"
        
        # Paths to assets
        self.sara_path = 'Sarah-assets/assets/sara/sara_spritesheet.png'
        self.forest_tileset = 'Sarah-assets/assets/maps/forest_tileset.png'
        self.space_tileset = 'Sarah-assets/assets/maps/space_tileset.png'
        self.trophy_path = 'Sarah-assets/assets/items/gold_trophy.png'

        self.current_state = "FOREST" # FOREST, SPACE, WIN, GAMEOVER
        self.setup_forest_map()

        # Start Sarah at tile (2, 2)
        self.hero = Hero('Sarah', self.sara_path, 2 * self.tile_size, 2 * self.tile_size)
        self.hero_moving = False
        self.projectiles = []
        self.monsters = []
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Tahoma", 24)
        self.large_font = pygame.font.SysFont("Tahoma", 36, bold=True)

    def spawn_monsters(self):
        self.monsters = []
        for _ in range(10): # Increased to 10
            mx = random.randint(100, self.screen_width - 100)
            my = random.randint(100, self.screen_height - 100)
            self.monsters.append(Monster(self.monster_path, mx, my))

    def setup_forest_map(self):
        map_path = os.path.join('maps', 'sample_map.json')
        if os.path.exists(map_path):
            self.map = LayeredMap.from_json(map_path)
            # Find the items layer name dynamically if needed, 
            # sample_map.json uses 'items' and 'path' and 'ground'
        else:
            # Fallback to manual if file missing (optional, for safety)
            self.map = LayeredMap(20, 20, self.tile_size)
            grass_grid = [[0 for _ in range(20)] for _ in range(20)]
            self.map.add_layer('ground', self.forest_tileset, grass_grid)
            items_grid = [[None for _ in range(20)] for _ in range(20)]
            items_grid[19][19] = 0 
            self.map.add_layer('items', self.trophy_path, items_grid)

    def setup_space_map(self):
        self.map = LayeredMap(32, 24, self.tile_size)
        self.map.layer_order = ['stars', 'items'] # Match the names added below
        # Layer 1: Stars/Space
        space_grid = [[0 for _ in range(32)] for _ in range(24)]
        self.map.add_layer('stars', self.space_tileset, space_grid)
        # Layer 2: Trophy at center
        items_grid = [[None for _ in range(32)] for _ in range(24)]
        items_grid[12][16] = 0 
        self.map.add_layer('items', self.trophy_path, items_grid)

    def handle_close(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_text(self, text, position, color=(255, 255, 255), center=False):
        text_surface = self.font.render(text, True, color)
        if center:
            rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, rect)
        else:
            self.screen.blit(text_surface, position)

    def check_interaction(self):
        # Check center of hero for tile detection
        hx = self.hero.rect.centerx
        hy = self.hero.rect.centery
        
        tile_id = self.map.get_tile_at('items', hx, hy)
        
        if self.current_state == "FOREST":
            # Portal at (19, 19). If we are on any item in Forest, it's the portal
            if tile_id is not None:
                self.current_state = "SPACE"
                self.monsters = [] # Clear monsters from forest
                self.projectiles = [] # Clear active beams
                self.setup_space_map()
                # Reset hero position for new map
                self.hero.rect.x = 2 * self.tile_size
                self.hero.rect.y = 2 * self.tile_size
        elif self.current_state == "SPACE":
            # Trophy at (10, 10)
            if tile_id is not None:
                self.current_state = "WIN"
                self.hero.victory_mode = True
                # Load trophy image for hero to hold
                trophy_img = pygame.image.load(self.trophy_path).convert_alpha()
                trophy_img.set_colorkey(trophy_img.get_at((0,0)))
                self.hero.carried_item = trophy_img

    def handle_input(self):
        if self.current_state == "GAMEOVER":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.__init__() # Reset game
            return

        if self.current_state == "WIN": return

        keys = pygame.key.get_pressed()
        
        # Handle Attack Input (E Key)
        if keys[pygame.K_e]:
            self.hero.start_attack(pygame.time.get_ticks())

        # Don't move if attacking
        if self.hero.attack_state != "IDLE":
            self.hero_moving = False
            return

        self.hero_moving = False
        self.hero_dashing = keys[pygame.K_LSHIFT]
        
        speed = 10 if self.hero_dashing else 5
        
        if keys[pygame.K_LEFT]:
            self.hero.rect.x -= speed
            self.hero.row = 1
            self.hero_moving = True
        elif keys[pygame.K_RIGHT]:
            self.hero.rect.x += speed
            self.hero.row = 2
            self.hero_moving = True
        elif keys[pygame.K_UP]:
            self.hero.rect.y -= speed
            self.hero.row = 3
            self.hero_moving = True
        elif keys[pygame.K_DOWN]:
            self.hero.rect.y += speed
            self.hero.row = 0
            self.hero_moving = True
        
        # Check for map boundaries
        self.hero.rect.x = max(0, min(self.hero.rect.x, self.screen_width - self.hero.rect.width))
        self.hero.rect.y = max(0, min(self.hero.rect.y, self.screen_height - self.hero.rect.height))

        self.check_interaction()

    def get_beam_rect(self, beam):
        # Helper to get a rect representing the current beam collision area
        if beam.direction == 0: # Down
            return pygame.Rect(beam.x - beam.width//2, beam.y, beam.width, beam.length)
        elif beam.direction == 1: # Left
            return pygame.Rect(beam.x - beam.length, beam.y - beam.width//2, beam.length, beam.width)
        elif beam.direction == 2: # Right
            return pygame.Rect(beam.x, beam.y - beam.width//2, beam.length, beam.width)
        elif beam.direction == 3: # Up
            return pygame.Rect(beam.x - beam.width//2, beam.y - beam.length, beam.width, beam.length)
        return pygame.Rect(0,0,0,0)

    def draw_ui(self):
        # Draw Sarah's HP Bar
        margin = 15
        bar_width = 200
        bar_height = 25
        hp_ratio = self.hero.hp / self.hero.max_hp
        
        # Background (Gray)
        pygame.draw.rect(self.screen, (50, 50, 50), (margin, margin, bar_width, bar_height))
        # Health (Red/Green)
        color = (0, 255, 0) if hp_ratio > 0.3 else (255, 0, 0)
        pygame.draw.rect(self.screen, color, (margin, margin, int(bar_width * hp_ratio), bar_height))
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (margin, margin, bar_width, bar_height), 2)
        
        # HP Text
        hp_text = self.font.render(f"HP: {int(self.hero.hp)}", True, (255, 255, 255))
        self.screen.blit(hp_text, (margin + 5, margin + 2))

    def draw_game_over_screen(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 180)) # Dark red overlay
        self.screen.blit(overlay, (0,0))
        
        msg = self.large_font.render("GAME OVER", True, (255, 0, 0))
        rect = msg.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(msg, rect)
        
        sub_msg = self.font.render("กด R เพื่อเริ่มใหม่", True, (255, 255, 255))
        sub_rect = sub_msg.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
        self.screen.blit(sub_msg, sub_rect)

    def draw_win_screen(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        msg = self.large_font.render("ยินดีด้วย! คุณเก็บถ้วยรางวัลได้แล้ว", True, (255, 215, 0))
        msg_rect = msg.get_rect(center=(self.screen_width//2, self.screen_height//2 - 20))
        self.screen.blit(msg, msg_rect)
        
        self.draw_text("จบเกม", (self.screen_width//2, self.screen_height//2 + 40), center=True)

    def start(self):
        while True:
            self.handle_close()
            self.handle_input()
            
            self.map.draw(self.screen)
            
            if self.current_state == "FOREST":
                self.draw_text("Sarah Adventure - ป่า (Forest)", (10, 10))
            elif self.current_state == "SPACE":
                self.draw_text("Sarah Adventure - อวกาศ (Space)", (10, 10))
            
            current_ticks = pygame.time.get_ticks()
            self.hero.update(current_ticks, self.hero_moving, self.hero_dashing) 
            
            # Handle Projectile Creation
            if self.hero.attack_state == "FIRING":
                if not any(isinstance(p, EnergyBeam) for p in self.projectiles):
                    beam = EnergyBeam(self.hero.rect.centerx, self.hero.rect.centery, self.hero.row)
                    self.projectiles.append(beam)
            
            # Update and Draw Projectiles
            for p in self.projectiles[:]:
                p.update(current_ticks)
                p.draw(self.screen)
                
                # Collision with Monsters
                for m in self.monsters[:]:
                    beam_rect = self.get_beam_rect(p)
                    if m.rect.colliderect(beam_rect):
                        m.take_damage(2) # Damage per frame
                
                if not p.alive:
                    self.projectiles.remove(p)

            # Update and Draw Monsters
            for m in self.monsters[:]:
                m.update(current_ticks)
                # Keep monsters in bounds
                m.rect.x = max(0, min(m.rect.x, self.screen_width - m.rect.width))
                m.rect.y = max(0, min(m.rect.y, self.screen_height - m.rect.height))
                
                m.check_player_collision(self.hero, current_ticks)
                m.draw(self.screen)
                if not m.alive:
                    self.monsters.remove(m)

            self.hero.draw(self.screen)
            self.draw_ui()

            if self.hero.hp <= 0:
                self.current_state = "GAMEOVER"

            if self.current_state == "GAMEOVER":
                self.draw_game_over_screen()

            if self.current_state == "WIN":
                self.draw_win_screen()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = SaraAdventure()
    game.start()
