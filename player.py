from entity import Entity
import pygame
import math

class Player(Entity):
    def __init__(self, x, y, surface):
        super().__init__(x, y, surface)

        self.movement_speed = 400
        self.angle = 0
        
        self.forward_vector = pygame.math.Vector2(0, -1)  # Default facing up
    
    def set_angle(self, angle):
        self.angle = angle % 360
        radians = pygame.math.radians(self.angle)
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