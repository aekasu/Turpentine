import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, surface):
        super().__init__()

        self.image = surface
        self.rect = surface.get_rect()

        self.movement_speed = 300
        self.velocity = pygame.math.Vector2(0,0)

        self.set_location(x, y)
    
    @property
    def x(self):
        return self.rect.x
    
    @property
    def y(self):
        return self.rect.y

    @property
    def width(self):
        return self.rect.width
    
    @property
    def height(self):
        return self.rect.height

    def set_location(self, x, y):
        self.rect.x, self.rect.y = x, y
    
    def set_size(self, w, h):
        self.rect.width, self.rect.height = w, h
    
    def move(self, dx, dy, dt):
        self.rect.x += dx * self.movement_speed * dt
        self.rect.y += dy * self.movement_speed * dt
    
    def check_event(self, event):
        ...
    
    def update(self, dt):
        self.rect.x += self.velocity.x * self.movement_speed * dt
        self.rect.y += self.velocity.y * self.movement_speed * dt
