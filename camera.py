import pygame

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
    
    def custom_draw(self):
        self.center_target_camera()

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)