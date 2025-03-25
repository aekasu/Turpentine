import pygame
import math

class Camera(pygame.sprite.Group):
    def __init__(self, x, y, w, h, *sprites):
        super().__init__(*sprites)

        self.init_viewport(x, y, w, h)

        self.zoom = 1
        self.angle = 0

    def init_viewport(self, x, y, w, h):
        self.viewport = pygame.Rect(x, y, w, h)
    
    def look_at(self, x, y):
        self.viewport.centerx = x
        self.viewport.centery = y

    def draw(self, surface):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            rotozoomed_rect = pygame.Rect(
                (sprite.x - self.viewport.x) * self.zoom, 
                (sprite.y - self.viewport.y) * self.zoom, 
                sprite.w*self.zoom, 
                sprite.h*self.zoom
            )

            # if not self.viewport.colliderect(rotozoomed_rect):
            #      continue
            
            rotozoomed_image = pygame.transform.rotozoom(sprite.image, self.angle, self.zoom).convert_alpha()
            surface.blit(rotozoomed_image, rotozoomed_rect)

    def check_event(self, event):
        for sprite in self.sprites():
            sprite.check_event(event)