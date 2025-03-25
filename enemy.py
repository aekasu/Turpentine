import pygame
from entity import Entity

class Enemy(Entity):
    def __init__(self, x, y, surface, follow_speed=500, acceleration=600, stop_threshold=5):
        super().__init__(x, y, surface)
        self.target = None
        self.follow_speed = follow_speed  # Max speed
        self.acceleration = acceleration  # Acceleration factor
        self.velocity = pygame.math.Vector2(0, 0)
        self.stop_threshold = stop_threshold  # Avoid jittering when close

    def follow(self, target):
        self.target = target

    def update(self, dt):
        if self.target:
            target_pos = pygame.math.Vector2(self.target.rect.center)
            current_pos = pygame.math.Vector2(self.rect.center)

            # Direction vector
            direction = target_pos - current_pos
            distance = direction.length()

            if distance > self.stop_threshold:
                direction = direction.normalize()
                
                # Accelerate towards player
                self.velocity += direction * self.acceleration * dt

                # Clamp speed
                if self.velocity.length() > self.follow_speed:
                    self.velocity.scale_to_length(self.follow_speed)

                # Move
                self.rect.x += self.velocity.x * dt
                self.rect.y += self.velocity.y * dt
            else:
                # Stop smoothly instead of jittering
                self.velocity *= 0.9  # Gradual slow down
