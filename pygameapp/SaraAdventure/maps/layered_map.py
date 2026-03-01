import pygame

class MapLayer:
    def __init__(self, name, tileset_path, tile_grid, tile_size=32):
        self.name = name
        try:
            self.tileset = pygame.image.load(tileset_path).convert_alpha()
            # Set colorkey for transparency if it's an item/foreground layer
            # Grass usually doesn't need colorkey if it fills the screen
            if name != 'ground': 
                self.tileset.set_colorkey(self.tileset.get_at((0,0)))
        except pygame.error:
            # Create a placeholder if file not found
            self.tileset = pygame.Surface((tile_size, tile_size))
            self.tileset.fill((200, 200, 200) if name != 'grass' else (34, 139, 34))
            
        self.tile_grid = tile_grid
        self.tile_size = tile_size

    def draw(self, surface):
        tiles_per_row = self.tileset.get_width() // self.tile_size
        for row_index, row in enumerate(self.tile_grid):
            for col_index, tile_id in enumerate(row):
                if tile_id is not None:
                    # Calculate source rect based on tile_id
                    src_x = (tile_id % tiles_per_row) * self.tile_size
                    src_y = (tile_id // tiles_per_row) * self.tile_size
                    src_rect = pygame.Rect(src_x, src_y, self.tile_size, self.tile_size)
                    
                    dest_rect = pygame.Rect(
                        col_index * self.tile_size,
                        row_index * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    surface.blit(self.tileset, dest_rect, src_rect)

class LayeredMap:
    def __init__(self, width=20, height=20, tile_size=32):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.layers = {}
        self.layer_order = ['grass', 'road', 'path', 'items']

    def add_layer(self, name, tileset_path, tile_grid):
        self.layers[name] = MapLayer(name, tileset_path, tile_grid, self.tile_size)

    def draw(self, surface):
        for name in self.layer_order:
            if name in self.layers:
                self.layers[name].draw(surface)

    @staticmethod
    def from_json(filepath):
        import json, os
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get grid dimensions from the first layer
        grid = data['layers'][0]['grid']
        height = len(grid)
        width = len(grid[0])
        
        map_obj = LayeredMap(width, height, data.get('tile_width', 32))
        
        # We'll use the layer names from the JSON, but keep the order
        map_obj.layer_order = []
        
        map_dir = os.path.dirname(filepath)
        for layer_data in data['layers']:
            name = layer_data['name']
            relative_tileset = layer_data['tileset']
            # Join with map_dir to handle relative paths in JSON
            tileset_path = os.path.normpath(os.path.join(map_dir, relative_tileset))
            
            # Convert grid -1 to None for transparency
            grid = [
                [None if val == -1 else val for val in row]
                for row in layer_data['grid']
            ]
            
            map_obj.add_layer(name, tileset_path, grid)
            map_obj.layer_order.append(name)
            
        return map_obj

    def get_tile_at(self, layer_name, x, y):
        """Returns the tile_id at the given pixel coordinates (x, y) for a specific layer."""
        # Find layer by name
        target_layer = self.layers.get(layer_name)
        if not target_layer:
            return None
        
        col = int(x // self.tile_size)
        row = int(y // self.tile_size)
        
        if 0 <= row < self.height and 0 <= col < self.width:
            return target_layer.tile_grid[row][col]
        return None
