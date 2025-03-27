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
        self.offset_x = 0
        self.offset_y = 0

    def init_viewport(self, x, y, w, h):
        self.viewport = pygame.Rect(x, y, w, h)

    def lerp(self, x, y):
        return x, y

    # offset amount for viewport corner to center the look_at coordinates
    def look_at(self, x, y):
        x, y = self.lerp(x, y)
        self.offset_x = x - self.viewport.width // (2 * self.zoom)
        self.offset_y = y - self.viewport.height // (2 * self.zoom)

    def update_zoom(self, amount=0):
        if not amount:
            return
        new_zoom = self.zoom + amount * self.zoom_speed
        self.zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))

    def draw(self, surface):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # subtract centering offsets from sprite's corner coordinates
            screen_x = (sprite.x - self.offset_x) * self.zoom
            screen_y = (sprite.y - self.offset_y) * self.zoom
            # updaate size based on zoom
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

            rotozoomed_image = pygame.transform.rotozoom(sprite.image, self.angle, self.zoom).convert_alpha()
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
        
        