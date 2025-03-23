import pygame
from state import State
from states.world_state import WorldState
from inputs import KeyboardHandler

class StartState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.key_action_mapping = {
            pygame.K_SPACE: 'start',
            pygame.K_RETURN: 'start',
            pygame.K_ESCAPE: 'quit'
        }
        
        self.actions = {
            'start': False,
            'quit': False
        }
        
        self.input_handlers = {
            'keyboard': KeyboardHandler(self, self.key_action_mapping)
        }
        
    
    def update(self, dt):
        if self.actions['start']:
            self.actions['start'] = False
            self.exit_state()
            world_state = WorldState(self.game)
            world_state.enter_state()
        
        if self.actions['quit']:
            self.game.exit()
    
    def render(self, surface):
        surface.fill((0, 0, 0))
        
        if self.game.font:
            self.game.font.render(
                surface, 
                "Turpentine", 
                (self.game.SCREEN_WIDTH // 2 - 50, self.game.SCREEN_HEIGHT // 2 - 30), 
                size=2
            )
            
            self.game.font.render(
                surface, 
                "Press SPACE or ENTER to start", 
                (self.game.SCREEN_WIDTH // 2 - 100, self.game.SCREEN_HEIGHT // 2 + 20), 
                size=1
            )
            
            self.game.font.render(
                surface, 
                "Press ESC to quit", 
                (self.game.SCREEN_WIDTH // 2 - 50, self.game.SCREEN_HEIGHT // 2 + 50), 
                size=1
            )