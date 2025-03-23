import pygame
from state import State
from camera import Camera
from player import Player
from entity import Entity
from inputs import KeyboardHandler

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

        self.input_handlers = {
            'keyboard': KeyboardHandler(self, self.key_action_mapping)
        }

        self.init_entities()
        self.camera = None
    
    def init_entities(self):
        player_surface = pygame.Surface((60,60))
        player_surface.fill((0,255,0))

        self.entities = [
            Player(0,0, player_surface)
        ]

    def update(self, dt):
        ...
    
    def render(self, surface):
        if not self.camera:
            self.camera = Camera(surface, *self.entities)
            self.camera.target = self.entities[0]
        self.camera.custom_draw()