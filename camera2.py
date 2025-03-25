import pygame
import math

class Camera(pygame.sprite.Group):
    def __init__(self, surface, *sprites):
        super().__init__(*sprites)
        self.target = None
        self.display_surface = surface
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def center_target_camera(self, target=None):
        if not target:
            target = self.target
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def rotate_point(self, x, y, angle_rad):
        """Rotate a point around origin (0,0) by the specified angle (in radians)"""
        cos_val = math.cos(angle_rad)
        sin_val = math.sin(angle_rad)
        new_x = x * cos_val - y * sin_val
        new_y = x * sin_val + y * cos_val
        return new_x, new_y

    def custom_draw(self, angle_rad=None):
        self.center_target_camera()
        if self.target:
            origin = pygame.math.Vector2(self.target.rect.center)
        else:
            origin = pygame.math.Vector2(self.half_w + self.offset.x, self.half_h + self.offset.y)
        
        if angle_rad is None:
            angle_rad = 0
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite == self.target:
                offset_pos = pygame.math.Vector2(sprite.rect.topleft) - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
                continue
            
            rel_x = sprite.rect.centerx - origin.x
            rel_y = sprite.rect.centery - origin.y
            
            rot_x, rot_y = self.rotate_point(rel_x, rel_y, angle_rad)
            
            screen_x = self.half_w + rot_x
            screen_y = self.half_h + rot_y
            
            rotated_image = pygame.transform.rotozoom(sprite.image.copy().convert_alpha(), -math.degrees(angle_rad), 1)
            rotated_rect = rotated_image.get_rect(center=(screen_x, screen_y))
            
            self.display_surface.blit(rotated_image, rotated_rect)