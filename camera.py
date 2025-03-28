import pygame
import math

class Camera(pygame.sprite.Group):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.init_viewport(x, y, w, h)
        self.zoom = 0.5
        self.zoom_speed = 1
        self.min_zoom = 0.5
        self.max_zoom = 1.5
        self.angle = 0
        self.offset = pygame.math.Vector2()

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

    def draw(self, surface):        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # calculate relative rotation using the sprite's actual rotation and perceived rotation through camera angle            
            total_rotation = self.angle - sprite.angle
            if hasattr(sprite, 'forward_vector'):
                # print(self.angle, sprite.angle)
                ...

            rotated_x, rotated_y = self.rotate_point(
                sprite.x, sprite.y, 
                self.viewport.centerx / self.zoom + self.offset.x, 
                self.viewport.centery / self.zoom + self.offset.y, 
                self.angle
            )

            # offset sprite image coordinates using viewport centering offset
            screen_x = (rotated_x - self.offset.x) * self.zoom
            screen_y = (rotated_y - self.offset.y) * self.zoom
            screen_w = sprite.w * self.zoom
            screen_h = sprite.h * self.zoom

            
            # offset sprite location for viewport detection
            rotozoomed_rect = pygame.Rect(
                screen_x + self.viewport.x,
                screen_y + self.viewport.y,
                screen_w,
                screen_h
            )

            if not self.viewport.colliderect(rotozoomed_rect):
                continue

            rotozoomed_image = pygame.transform.rotozoom(sprite.image, -total_rotation, self.zoom).convert_alpha()
            surface.blit(rotozoomed_image, rotozoomed_rect)

    def check_event(self, event):
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