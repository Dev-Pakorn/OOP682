import pygame
import json
import os
import sys

# Add current dir to path to import local modules
sys.path.append(os.getcwd())

class MapEditor:
    def __init__(self):
        pygame.init()
        self.tile_size = 32
        self.cols = 80
        self.rows = 10
        self.screen_width = 1024 # Fixed window width for better viewing
        self.screen_height = self.rows * self.tile_size + 150 
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sarah Adventure - Map Editor (80x10)")
        
        # Camera/Scroll offset for wide maps
        self.scroll_x = 0
        
        self.clock = pygame.time.get_ticks()
        self.running = True
        
        # Theme Config
        self.themes = {
            "FOREST": {
                "tileset": 'Sarah-assets/assets/maps/forest_tileset.png',
                "save": 'maps/forest_map.json'
            },
            "SPACE": {
                "tileset": 'Sarah-assets/assets/maps/space_tileset.png',
                "save": 'maps/space_map.json'
            }
        }
        self.current_theme = "FOREST"
        self.layer_names = ["ground", "path", "items"]
        self.current_layer_idx = 0
        
        # UI Styling (Premium Colors)
        self.COLORS = {
            "bg": (20, 20, 24),
            "sidebar": (30, 30, 36),
            "accent": (0, 180, 255),
            "text": (230, 230, 240),
            "grid": (45, 45, 50),
            "hover": (60, 60, 75),
            "success": (46, 204, 113)
        }
        
        # UI Sidebar Config
        self.sidebar_width = 240
        self.screen_width = 1024 + self.sidebar_width
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Selection
        self.selected_tile_id = 0
        self.font_main = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.font_sub = pygame.font.SysFont("Segoe UI", 16)
        
        # Load Initial Theme
        self.switch_theme("FOREST")

    def draw_rounded_rect(self, surface, color, rect, radius=10):
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def switch_theme(self, theme_name):
        if theme_name not in self.themes: return
        self.current_theme = theme_name
        self.tileset_path = self.themes[theme_name]["tileset"]
        self.save_path = self.themes[theme_name]["save"]
        
        # Load Tileset
        try:
            self.tileset = pygame.image.load(self.tileset_path).convert_alpha()
        except pygame.error:
            self.tileset = pygame.Surface((self.tile_size, self.tile_size))
            self.tileset.fill((200, 200, 200))

        self.tiles_per_row = self.tileset.get_width() // self.tile_size
        self.total_tiles = (self.tileset.get_width() // self.tile_size) * (self.tileset.get_height() // self.tile_size)
        self.selected_tile_id = 0 # Reset selection
        
        # Clear/Load Grids
        self.grids = {
            "ground": [[0 for _ in range(self.cols)] for _ in range(self.rows)],
            "path": [[-1 for _ in range(self.cols)] for _ in range(self.rows)],
            "items": [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        }
        self.load_map()
        print(f"Switched to {theme_name} theme")

    def load_map(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for layer_data in data['layers']:
                        name = layer_data['name']
                        if name in self.grids:
                            loaded_grid = layer_data['grid']
                            for r in range(min(self.rows, len(loaded_grid))):
                                for c in range(min(self.cols, len(loaded_grid[r]))):
                                    self.grids[name][r][c] = loaded_grid[r][c]
            except Exception as e:
                print(f"Error loading map: {e}")

    def save_map(self):
        data = {
            "tile_width": self.tile_size,
            "tile_height": self.tile_size,
            "layers": []
        }
        for name in self.layer_names:
            data["layers"].append({
                "name": name,
                "tileset": f"../Sarah-assets/assets/maps/{self.current_theme.lower()}_tileset.png",
                "grid": self.grids[name]
            })
        
        if not os.path.exists('maps'): os.makedirs('maps')
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Map saved to {self.save_path}")

    def draw(self):
        self.screen.fill(self.COLORS["bg"])
        
        # Canvas Area
        canvas_width = self.screen_width - self.sidebar_width
        
        # Draw Grids
        for name in self.layer_names:
            grid = self.grids[name]
            for r in range(self.rows):
                for c in range(self.cols):
                    tile_id = grid[r][c]
                    if tile_id != -1:
                        x_pos = c * self.tile_size - self.scroll_x
                        if -self.tile_size < x_pos < canvas_width:
                            src_x = (tile_id % self.tiles_per_row) * self.tile_size
                            src_y = (tile_id // self.tiles_per_row) * self.tile_size
                            self.screen.blit(self.tileset, (x_pos, r * self.tile_size), (src_x, src_y, self.tile_size, self.tile_size))
        
        # Subtle Grid Lines
        for c in range(self.cols + 1):
            x = c * self.tile_size - self.scroll_x
            if 0 <= x <= canvas_width:
                pygame.draw.line(self.screen, self.COLORS["grid"], (x, 0), (x, self.rows * self.tile_size))
        for r in range(self.rows + 1):
            pygame.draw.line(self.screen, self.COLORS["grid"], (0, r * self.tile_size), (canvas_width, r * self.tile_size))

        # SIDEBAR UI
        sidebar_rect = (canvas_width, 0, self.sidebar_width, self.screen_height)
        pygame.draw.rect(self.screen, self.COLORS["sidebar"], sidebar_rect)
        pygame.draw.line(self.screen, self.COLORS["accent"], (canvas_width, 0), (canvas_width, self.screen_height), 2)

        ui_x = canvas_width + 15
        ui_y = 20
        
        # Header
        header = self.font_main.render("MAP EDITOR", True, self.COLORS["accent"])
        self.screen.blit(header, (ui_x, ui_y))
        
        # Theme/Map Info
        ui_y += 35
        self.draw_rounded_rect(self.screen, (40, 40, 50), (ui_x-5, ui_y, self.sidebar_width-20, 100), 8)
        theme_txt = self.font_main.render(f"Mode: {self.current_theme}", True, (255, 255, 255))
        self.screen.blit(theme_txt, (ui_x + 5, ui_y + 10))
        
        hint_txt = self.font_sub.render("F: Forest | P: Space", True, (150, 150, 160))
        self.screen.blit(hint_txt, (ui_x + 5, ui_y + 35))
        
        layer_txt = self.font_sub.render(f"Layer: {self.layer_names[self.current_layer_idx]} (1-3)", True, (200, 200, 210))
        self.screen.blit(layer_txt, (ui_x + 5, ui_y + 60))

        # Tile Selection Container
        ui_y += 115
        self.font_main.render("SELECT TILE", True, self.COLORS["text"])
        self.screen.blit(self.font_main.render("TILESET", True, self.COLORS["text"]), (ui_x, ui_y))
        
        # Mini Tileset Preview
        ui_y += 30
        preview_bg = (canvas_width + 10, ui_y, self.sidebar_width - 20, 120)
        self.draw_rounded_rect(self.screen, (20, 20, 24), preview_bg, 5)
        
        # Draw all available tiles in a mini-grid
        tiles_x_start = canvas_width + 15
        tiles_y_start = ui_y + 10
        for i in range(min(self.total_tiles, 32)): # Show first 32 tiles
            col = i % 6
            row = i // 6
            tx = tiles_x_start + col * (self.tile_size + 4)
            ty = tiles_y_start + row * (self.tile_size + 4)
            
            # Tile rect
            tile_rect = (tx, ty, self.tile_size, self.tile_size)
            src_x = (i % self.tiles_per_row) * self.tile_size
            src_y = (i // self.tiles_per_row) * self.tile_size
            
            # Hover/Selection highlight
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(tile_rect).collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, self.COLORS["accent"], (tx-2, ty-2, self.tile_size+4, self.tile_size+4), 2)
                if pygame.mouse.get_pressed()[0]: self.selected_tile_id = i
            
            if self.selected_tile_id == i:
                pygame.draw.rect(self.screen, self.COLORS["success"], (tx-2, ty-2, self.tile_size+4, self.tile_size+4), 2)
            
            self.screen.blit(self.tileset, (tx, ty), (src_x, src_y, self.tile_size, self.tile_size))

        # Save Button Area
        ui_y = self.screen_height - 60
        btn_rect = (canvas_width + 20, ui_y, self.sidebar_width - 40, 40)
        btn_color = self.COLORS["success"] if not pygame.Rect(btn_rect).collidepoint(pygame.mouse.get_pos()) else (56, 214, 123)
        self.draw_rounded_rect(self.screen, btn_color, btn_rect, 20)
        save_txt = self.font_main.render("SAVE MAP (S)", True, (255, 255, 255))
        self.screen.blit(save_txt, (canvas_width + (self.sidebar_width - save_txt.get_width())//2, ui_y + 10))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.save_map()
                    if event.key == pygame.K_f:
                        self.switch_theme("FOREST")
                    if event.key == pygame.K_p:
                        self.switch_theme("SPACE")
                    if event.key == pygame.K_1: self.current_layer_idx = 0
                    if event.key == pygame.K_2: self.current_layer_idx = 1
                    if event.key == pygame.K_3: self.current_layer_idx = 2
                    
                    # Tile Selection with [ and ]
                    if event.key == pygame.K_RIGHTBRACKET: # ]
                        self.selected_tile_id = (self.selected_tile_id + 1) % self.total_tiles
                    if event.key == pygame.K_LEFTBRACKET: # [
                        self.selected_tile_id = (self.selected_tile_id - 1) % self.total_tiles
                
                # Modern Mouse Wheel support (Pygame 2)
                if event.type == pygame.MOUSEWHEEL:
                    # Invert y for intuitive horizontal scroll (scroll down = move right)
                    self.scroll_x -= event.y * self.tile_size * 2
                    # Handle horizontal wheel if available
                    self.scroll_x += event.x * self.tile_size * 2
                    # Constrain bounds
                    self.scroll_x = max(0, min((self.cols * self.tile_size) - self.screen_width, self.scroll_x))
                
                # Compatibility Mouse Wheel support
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4: # Scroll Up (Move Left)
                        self.scroll_x = max(0, self.scroll_x - self.tile_size * 2)
                    if event.button == 5: # Scroll Down (Move Right)
                        self.scroll_x = min((self.cols * self.tile_size) - self.screen_width, self.scroll_x + self.tile_size * 2)
            
            # Middle Mouse Drag to Scroll
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[1]: # Middle Click
                rel_x, _ = pygame.mouse.get_rel()
                self.scroll_x = max(0, min((self.cols * self.tile_size) - self.screen_width, self.scroll_x - rel_x))
            else:
                # Reset relative move when not dragging to avoid large jumps on next click
                pygame.mouse.get_rel()

            # Left Click to Paint, Right Click to Erase
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < self.rows * self.tile_size:
                real_x = mouse_pos[0] + self.scroll_x
                c = real_x // self.tile_size
                r = mouse_pos[1] // self.tile_size
                
                if 0 <= c < self.cols and 0 <= r < self.rows:
                    if mouse_buttons[0]: # Left
                        layer_name = self.layer_names[self.current_layer_idx]
                        self.grids[layer_name][r][c] = self.selected_tile_id
                    elif mouse_buttons[2]: # Right
                        layer_name = self.layer_names[self.current_layer_idx]
                        if layer_name == "ground":
                            self.grids[layer_name][r][c] = 0
                        else:
                            self.grids[layer_name][r][c] = -1
            
            self.draw()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()
