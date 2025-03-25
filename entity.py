import pygame
from inputs import ActionHandler, ControllerHandler

"""
    rewrite the entirety of this file to include dt, 
    and actually use or remove methods from entity base class
"""

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
    def w(self):
        return self.rect.width
    
    @property
    def h(self):
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

class MovingEntity(Entity):
    def __init__(self, x, y, surface):
        super().__init__(x, y, surface)

        self.movement_speed = 400
        self.rotation_speed = 180
        self.angle = 0
        self.forward_vector = pygame.math.Vector2(0, -1)  # up by default
    
    def set_angle(self, angle): #
        self.angle = angle % 360
        radians = math.radians(self.angle)
        self.forward_vector = pygame.math.Vector2(
            -math.sin(radians),
            -math.cos(radians) 
        )
    
    def change_angle(self, delta_angle):
        self.set_angle(self.angle + delta_angle)
    
    def move_forward(self, dt):
        self.velocity = self.forward_vector.copy()
    
    def move_backward(self, dt):
        self.velocity = -self.forward_vector.copy()
    
    def move_right(self, dt):
        right_vector = self.forward_vector.rotate(90)
        self.velocity = right_vector.copy()
    
    def move_left(self, dt):
        left_vector = self.forward_vector.rotate(-90)
        self.velocity = left_vector.copy()
    
    def update(self, dt):
        super().update(dt)
        
        self.velocity = pygame.math.Vector2(0, 0)
