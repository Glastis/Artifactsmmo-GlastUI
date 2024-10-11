import os

import arcade
import arcade.gui
from arcade import load_texture

import interface.map as map_interface

assets_dir = "assets"
assets_dirs = {
    "map": f"{assets_dir}/maps",
    "monster": f"{assets_dir}/monsters",
    "resource": f"{assets_dir}/resources"
}
assets_extension = "png"

class GameMapView(arcade.View):
    map_data = None
    def __init__(self):
        super().__init__()
        map_data = map_interface.get_map_data()
        default_texture = arcade.load_texture("assets/maps/forest_1.png")
        self.textures = {}
        self.tiles = []
        self.scroll_x = 0
        self.scroll_y = 0
        self.dragging = False
        self.last_mouse_position = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.__load_textures()
        x_values = [tile_data['x'] for tile_data in map_data]
        y_values = [tile_data['y'] for tile_data in map_data]
        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        self.offset_x = -min_x
        self.offset_y = -min_y
        self.max_y = max_y  # Stocker le maximum des Y
        for tile_data in map_data:
            tile = {}
            x = tile_data['x']
            y = tile_data['y']
            skin = tile_data.get('skin', 'forest_1')
            # Obtenir la texture de la tuile
            tile_texture = self.textures['map'].get(skin, default_texture)
            tile['texture'] = tile_texture
            tile['data'] = tile_data
            tile['x'] = x
            tile['y'] = y
            # is the tile already in the list?
            for existing_tile in self.tiles:
                if existing_tile['x'] == x and existing_tile['y'] == y:
                    print (f"Tile {x}, {y} already exists")
            self.tiles.append(tile)

    def __load_textures(self):
        for asset_type, directory in assets_dirs.items():
            self.textures.setdefault(asset_type, {})
            for filename in os.listdir(directory):
                if filename.endswith(f".{assets_extension}"):
                    texture_path = os.path.join(directory, filename)
                    texture_key = filename.split('.')[0]
                    if texture_key not in self.textures[asset_type]:
                        try:
                            self.textures[asset_type][texture_key] = arcade.load_texture(texture_path)
                            # print(f"Texture chargée : {texture_key} depuis {texture_path}")
                        except Exception as e:
                            print(f"Erreur lors du chargement de la texture {texture_key} : {e}")

    def draw_tile(self, tile):
        texture = tile['texture']
        x = tile['x'] + self.offset_x
        y = tile['y'] + self.offset_y
        tile_width = texture.width
        tile_height = texture.height

        # Inverser l'axe Y
        y_inverted = (self.max_y + self.offset_y) - y

        center_x = x * tile_width + tile_width / 2 + self.scroll_x
        center_y = y_inverted * tile_height + tile_height / 2 + self.scroll_y

        # Dessiner la tuile
        arcade.draw_texture_rectangle(center_x, center_y, tile_width, tile_height, texture)

        # Vérifier si la souris est sur cette tuile
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y

        # Calculer les limites de la tuile
        left = center_x - tile_width / 2
        right = center_x + tile_width / 2
        bottom = center_y - tile_height / 2
        top = center_y + tile_height / 2

        # Vérifier si la position de la souris est dans les limites de la tuile
        if left <= mouse_x <= right and bottom <= mouse_y <= top:
            # Dessiner un overlay semi-transparent
            arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, (0, 0, 0, 100))

        # Dessiner le contenu de la tuile s'il y en a
        if tile['data'] and tile['data'].get('content'):
            content_data = tile['data']['content']
            content_type = content_data['type']
            content_code = content_data['code']
            if content_type not in ['monster', 'resource']:
                return
            content_texture = self.textures[content_type].get(content_code)
            if content_texture:
                arcade.draw_texture_rectangle(center_x, center_y, content_texture.width, content_texture.height,
                                              content_texture)

    def on_draw(self):
        arcade.start_render()
        for tile in self.tiles:
            self.draw_tile(tile)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = True
            self.last_mouse_position = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        # Mettre à jour la position de la souris
        self.mouse_x = x
        self.mouse_y = y

        if self.dragging and self.last_mouse_position is not None:
            self.scroll_x += dx
            self.scroll_y += dy
            self.last_mouse_position = (x, y)
