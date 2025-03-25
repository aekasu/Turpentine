import pygame
import math
import random
from state import State
from inputs import KeyboardHandler
from player import Player
from enemy import Enemy
from camera import Camera

class DemoEnemy(Enemy):
    def __init__(self, x, y, surface):
        super().__init__(x, y, surface)
        self.orbit_angle = random.uniform(0, 360)
        self.orbit_speed = random.uniform(0.5, 2.0)
        self.orbit_radius = random.uniform(100, 300)
        self.orbit_center = pygame.math.Vector2(x, y)
    
    def update(self, dt):
        self.orbit_angle += self.orbit_speed * dt * 100
        new_x = self.orbit_center.x + math.cos(math.radians(self.orbit_angle)) * self.orbit_radius
        new_y = self.orbit_center.y + math.sin(math.radians(self.orbit_angle)) * self.orbit_radius
        self.rect.center = (new_x, new_y)

class DemoState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.key_action_mapping = {
            pygame.K_w: 'move_up',
            pygame.K_s: 'move_down',
            pygame.K_a: 'move_left',
            pygame.K_d: 'move_right',
            pygame.K_ESCAPE: 'quit'
        }
        self.actions = {action: False for action in self.key_action_mapping.values()}
        self.input_handlers = {'keyboard': KeyboardHandler(self, self.key_action_mapping)}
        
        self.setup_demo()
    
    def setup_demo(self):
        self.surface = self.game.game_canvas
        self.player = Player(600, 350, pygame.Surface((40, 40)))
        self.player.image.fill((0, 255, 0))
        self.camera = Camera(self.surface, self.player)
        
        self.enemies = pygame.sprite.Group()
        for _ in range(5):
            enemy = DemoEnemy(random.randint(200, 1000), random.randint(200, 600), pygame.Surface((30, 30)))
            enemy.image.fill((255, 0, 0))
            self.enemies.add(enemy)
            self.camera.add(enemy)
        
        self.camera.target = self.player
    
    def check_event(self, event):
        super().check_event(event)
        if self.actions['quit']:
            self.game.exit()
    
    def update(self, dt):
        if self.actions['move_up']:
            self.player.move(0, -1, dt)
        if self.actions['move_down']:
            self.player.move(0, 1, dt)
        if self.actions['move_left']:
            self.player.move(-1, 0, dt)
        if self.actions['move_right']:
            self.player.move(1, 0, dt)
        
        self.enemies.update(dt)
        self.camera.update(dt)
    
    def render(self, surface):
        surface.fill((30, 30, 30))
        self.camera.custom_draw()
        pygame.display.flip()

class StartState(State):
    def __init__(self, game):
        super().__init__(game)
        self.actions = {'start': False}
        self.key_action_mapping = {pygame.K_SPACE: 'start'}
        self.input_handlers = {'keyboard': KeyboardHandler(self, self.key_action_mapping)}
    
    def check_event(self, event):
        super().check_event(event)
        if self.actions['start']:
            self.game.state_stack.append(DemoState(self.game))
    
    def render(self, surface):
        surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Press SPACE to Start", True, (255, 255, 255))
        surface.blit(text, (400, 300))
        pygame.display.flip()