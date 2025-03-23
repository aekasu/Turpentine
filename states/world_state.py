import pygame
from state import State
from camera import Camera
from player import Player
from entity import Entity
from inputs import KeyboardHandler, ControllerHandler
import math

class WorldState(State):
    def __init__(self, game):
        super().__init__(game)

        self.key_action_mapping = {
            pygame.K_w: 'up',
            pygame.K_a: 'left',
            pygame.K_s: 'down',
            pygame.K_d: 'right',
            pygame.K_ESCAPE: 'quit',
        }

        self.actions = {action: False for action in self.key_action_mapping.values()}
        self.last_rumble = 0
        self.rumble_cooldown = 500

        self.init_controls()
        self.init_entities()
        self.camera = None

        self.input_handlers = {
            'keyboard': KeyboardHandler(self, self.key_action_mapping),
            'controller': ControllerHandler(self, self.controller if self.has_controller else None),
        }
    
    def init_controls(self):
        # Controller setup
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
        """Apply rumble to controller if available"""
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
        player_surface = pygame.Surface((60,60))
        player_surface.fill((0,255,0))
        self.player = Player(0, 0, player_surface)

        entity_surface = pygame.Surface((70, 70))
        entity_surface.fill((255,0,0))

        self.entities = [
            self.player,
            Entity(200, 200, entity_surface),
            Entity(-200, 200, entity_surface),
        ]

    def update(self, dt):
        ...
    
    def render(self, surface):
        if not self.camera:
            self.camera = Camera(surface, *self.entities)
            self.camera.target = self.player
        angle_rad = math.radians(self.player.angle)
        self.camera.custom_draw(angle_rad)