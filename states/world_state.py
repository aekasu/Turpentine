import pygame
import random
import math
from state import State
from camera import Camera
from player import Player
from enemy import Enemy
from inputs import KeyboardHandler, ControllerHandler

class WorldState(State):
    def __init__(self, game):
        super().__init__(game)

        self.key_action_mapping = {
            pygame.K_w: 'up',
            pygame.K_a: 'left',
            pygame.K_s: 'down',
            pygame.K_d: 'right',
            pygame.K_j: 'turn_left',
            pygame.K_l: 'turn_right',
            pygame.K_ESCAPE: 'quit',
        }

        self.actions = {
            'up': False, 'left': False, 'down': False, 'right': False, 'quit': False,
            'forward': False, 'backward': False, 'strafe_left': False, 'strafe_right': False,
            'turn_left': False, 'turn_right': False, 'pause': False
        }

        self.last_rumble = 0
        self.rumble_cooldown = 500
        self.player_speed = 1  # Pixels per second
        self.rotation_speed = 180  # Degrees per second

        self.init_controls()
        self.init_entities()
        self.camera = None

        self.spawn_timer = 0
        self.spawn_interval = 1000  # 1 second per enemy
        self.enemy_lifetime = 15000  # 15 seconds per enemy
        self.enemies = []

        self.input_handlers = {
            'keyboard': KeyboardHandler(self, self.key_action_mapping),
            'controller': ControllerHandler(self, self.controller if self.has_controller else None),
        }
    
    def init_controls(self):
        self.has_controller = False
        self.controller = None
        
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()
        
        if joystick_count > 0:
            self.has_controller = True
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            print(f"Using controller: {self.controller.get_name()}")
        else:
            print("No controller detected. You can still play with keyboard.")
    
    def rumble(self, duration=500, intensity=0.7):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rumble < self.rumble_cooldown:
            return
        
        self.last_rumble = current_time
        
        if self.has_controller:
            try:
                self.controller.rumble(intensity, intensity, duration)
                print(f"Rumbling at intensity {intensity} for {duration}ms")
            except Exception as e:
                print(f"Rumble error: {e}")

    def init_entities(self):
        player_surface = pygame.Surface((20, 20))
        player_surface.fill((0, 255, 0))
        self.player = Player(0, 0, player_surface)

        self.entities = [self.player]

    def spawn_enemy(self):
        enemy_surface = pygame.Surface((10, 10))
        enemy_surface.fill((255, 0, 0))

        # Random spawn position away from player
        spawn_distance = 300
        angle = random.uniform(0, math.pi * 2)
        x = self.player.x + math.cos(angle) * spawn_distance
        y = self.player.y + math.sin(angle) * spawn_distance

        enemy = Enemy(x, y, enemy_surface)
        enemy.spawn_time = pygame.time.get_ticks()  # Track spawn time
        enemy.follow(self.player)

        self.enemies.append(enemy)
        self.entities.append(enemy)
        if self.camera:
            self.camera.add(enemy)  # Add to camera group

    def update(self, dt):
        current_time = pygame.time.get_ticks()

        # Enemy spawning logic
        if current_time - self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = current_time
            self.spawn_enemy()

        # Remove old enemies
        self.enemies = [
            enemy for enemy in self.enemies if current_time - enemy.spawn_time < self.enemy_lifetime
        ]
        self.entities = [self.player] + self.enemies

        if self.camera:
            self.camera.empty()  # Clear camera group
            self.camera.add(*self.entities)  # Re-add valid entities

        # Process movement inputs
        if self.actions['up']:
            self.player.move(0, -self.player_speed, dt)
        if self.actions['down']:
            self.player.move(0, self.player_speed, dt)
        if self.actions['left']:
            self.player.move(-self.player_speed, 0, dt)
        if self.actions['right']:
            self.player.move(self.player_speed, 0, dt)

        move_x = 0
        move_y = 0

        angle_rad = math.radians(self.player.angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        if self.actions['forward']:
            move_x += cos_a * self.player_speed
            move_y += sin_a * self.player_speed
        if self.actions['backward']:
            move_x -= cos_a * self.player_speed
            move_y -= sin_a * self.player_speed
        if self.actions['strafe_left']:
            move_x += sin_a * self.player_speed
            move_y -= cos_a * self.player_speed
        if self.actions['strafe_right']:
            move_x -= sin_a * self.player_speed
            move_y += cos_a * self.player_speed
        
        self.player.move(move_x, move_y, dt)
        
        self.player.angle += self.rotation_speed * dt * float(self.actions['turn_left'])
        self.player.angle -= self.rotation_speed * dt * float(self.actions['turn_right'])
        self.player.angle %= 360

        if self.actions['quit']:
            self.game.running = False

        if self.actions['pause']:
            print("Game paused")
            self.actions['pause'] = False

        for entity in self.entities:
            entity.update(dt)
            if entity is not self.player:
                entity.follow(self.player)

            if entity != self.player and self.player.rect.colliderect(entity.rect):
                self.rumble()

    def render(self, surface):
        if not self.camera:
            self.camera = Camera(surface, *self.entities)
            self.camera.target = self.player

        angle_rad = math.radians(self.player.angle)
        self.camera.custom_draw(angle_rad)
