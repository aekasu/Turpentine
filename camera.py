import pygame
import math
from entity import Entity

class Tile(Entity):
    def __init__(self, x, y, surface):
        super().__init__(x, y, surface)

class Region:
    def __init__(self, x, y, w, h, tile_size):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.rect = pygame.Rect(x, y, w, h)
        self.tile_size = tile_size

        #
        ground = pygame.Surface((self.tile_size,)*2)
        ground.fill('yellow')

        self.tiles = {
            0: ground,
        }

    def __contains__(self, target_rect):
        return self.rect.colliderect(target_rect)
    
    def get_tile(self, x, y):
        return Tile(x, y, self.tiles[0])
    
    def get_tiles(self, target_rect):
        tiles = []
        for tile_x in range(target_rect.x, target_rect.x+target_rect.width, self.tile_size):
            for tile_y in range(target_rect.y, target_rect.y+target_rect.height, self.tile_size):
                tiles.append(self.get_tile(tile_x, tile_y))
        return tiles
    
    def check_event(self, event):
        ...

class Camera(pygame.sprite.Group):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.init_viewport(x, y, w, h)
        self.zoom = 1
        self.zoom_speed = 1
        self.min_zoom = 0.5
        self.max_zoom = 1.5
        self.angle = 0
        self.offset = pygame.math.Vector2()
        self.regions = []

    @property
    def position_rect(self):
        # Return the rectangle in world coordinates that represents what's visible in the viewport
        return pygame.Rect(
            self.offset.x,  # Left
            self.offset.y,  # Top
            self.viewport.width / self.zoom,  # Width in world coordinates
            self.viewport.height / self.zoom  # Height in world coordinates
        )

    def init_viewport(self, x, y, w, h):
        self.viewport = pygame.Rect(x, y, w, h)

    def lerp(self, x, y):
        return x, y

    # calculate viewport coordinate offset to center look_at coordinates
    def look_at(self, x, y):
        x, y = self.lerp(x, y)
        self.offset.x = x - self.viewport.width // (2 * self.zoom)
        self.offset.y = y - self.viewport.height // (2 * self.zoom)

    def update_zoom(self, amount=0):
        if not amount:
            return
        new_zoom = self.zoom + amount * self.zoom_speed
        self.zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))

    def draw_region(self, surface, region):
        if not self.position_rect in region:
            return
        
        tiles = region.get_tiles(self.position_rect)

        for tile in tiles:
            surface.blit(tile.image, tile.rect)

    # rotate point around center
    def rotate_point(self, x, y, cx, cy, angle):
        angle_rad = math.radians(angle)
        
        # offset sprite coordinates by viewport center
        temp_x = x - cx
        temp_y = y - cy
        
        # rotate the point based on angle
        rotated_x = temp_x * math.cos(angle_rad) - temp_y * math.sin(angle_rad)
        rotated_y = temp_x * math.sin(angle_rad) + temp_y * math.cos(angle_rad)
        
        # revert offset
        return rotated_x + cx, rotated_y + cy

    def draw_sprite(self, surface, sprite):        
        total_rotation = self.angle - sprite.angle

        rotated_x, rotated_y = self.rotate_point(
            sprite.x, sprite.y, 
            self.viewport.centerx / self.zoom + self.offset.x, 
            self.viewport.centery / self.zoom + self.offset.y, 
            self.angle
        )

        screen_x = (rotated_x - self.offset.x) * self.zoom
        screen_y = (rotated_y - self.offset.y) * self.zoom
        screen_w = sprite.w * self.zoom
        screen_h = sprite.h * self.zoom

        rotozoomed_rect = pygame.Rect(
            screen_x + self.viewport.x,
            screen_y + self.viewport.y,
            screen_w,
            screen_h
        )

        if not self.viewport.colliderect(rotozoomed_rect):
            return

        rotozoomed_image = pygame.transform.rotozoom(sprite.image, -total_rotation, self.zoom).convert_alpha()
        surface.blit(rotozoomed_image, rotozoomed_rect)
    
    def draw(self, surface):
        for region in self.regions:
            self.draw_region(surface, region)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.draw_sprite(surface, sprite)

    def check_event(self, event):
        for region in self.regions:
            region.check_event(event)

        for sprite in self.sprites():
            sprite.check_event(event)

class SmoothFollowCamera(Camera):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.follow_speed = 0.1
        self._lerp_x, self._lerp_y = self.viewport.center

    def lerp(self, x, y):
        self._lerp_x += (x - self._lerp_x) * self.follow_speed
        self._lerp_y += (y - self._lerp_y) * self.follow_speed
        return self._lerp_x, self._lerp_y