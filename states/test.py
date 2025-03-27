from inputs import ControllerHandler, KeyboardHandler
from entity import Entity, MovingEntity
from states.debug import DebugState
from camera import Camera, SmoothFollowCamera
from state import State
import random
import pygame
import math

class TestState(State):
    def __init__(self, game):
        super().__init__(game, is_overlay=False)
        entity_amount = 50
        max_range = (self.game.GAME_WIDTH - 50, self.game.GAME_HEIGHT - 50)
        entity_surface = pygame.Surface((50,50))
        player_surface = entity_surface.copy()
        entity_surface.fill('red')
        player_surface.fill('green')
        self.entities = [Entity(random.randrange(0, max_range[0]*2), random.randrange(0, max_range[1]*2), entity_surface.copy()) for i in range(entity_amount)]
        self.player = MovingEntity(0,0,player_surface)
        # ---------

        self.camera = SmoothFollowCamera(0, 0, max_range[0]+50, max_range[1]+50)
        self.input_handlers = {
            'keyboard': KeyboardHandler({
                pygame.K_w: 'up',
                pygame.K_a: 'left',
                pygame.K_s: 'down',
                pygame.K_d: 'right',
            }),
            'controller': ControllerHandler()
        }

        # ---------
        d = DebugState(game, 
            player = self.player,
            controller = self.input_handlers['controller'].controller,
        )
        d.enter_state()

    def handle_button_inputs(self, dt):
        # Zoom
        pre_zoom = self.camera.zoom
        dz = float(self.input_handlers['controller'].check_action('right_trigger')) - float(self.input_handlers['controller'].check_action('left_trigger'))
        self.camera.update_zoom(dz * dt)
        if self.camera.zoom in [self.camera.min_zoom, self.camera.max_zoom] and self.camera.zoom != pre_zoom:
            self.input_handlers['controller'].rumble(duration=100)

    def handle_movement_inputs(self, dt):        
        move_x, move_y = 0, 0

        # Keyboard inputs
        if self.input_handlers['keyboard'].check_action('up'):
            self.player.move(0, -1, dt)
        if self.input_handlers['keyboard'].check_action('down'):
            self.player.move(0, 1, dt)
        if self.input_handlers['keyboard'].check_action('left'):
            self.player.move(-1, 0, dt)
        if self.input_handlers['keyboard'].check_action('right'):
            self.player.move(1, 0, dt)

        # Analog controller inputs
        move_y += float(self.input_handlers['controller'].check_action('move_up'))
        move_y -= float(self.input_handlers['controller'].check_action('move_down'))
        move_x += float(self.input_handlers['controller'].check_action('move_left'))
        move_x -= float(self.input_handlers['controller'].check_action('move_right'))

        if move_x or move_y:
            angle_radian = math.radians(self.player.angle)
            dx = -(math.sin(angle_radian) * move_y + math.cos(angle_radian) * move_x)
            dy = -(math.cos(angle_radian) * move_y + -math.sin(angle_radian) * move_x)

            self.player.move(dx, dy, dt)
        
        if (left_turn := float(self.input_handlers['controller'].check_action('turn_left'))):
            self.player.angle += left_turn * self.player.rotation_speed * dt

        if (right_turn := float(self.input_handlers['controller'].check_action('turn_right'))):
            self.player.angle -= right_turn * self.player.rotation_speed * dt
        
        self.player.angle %= 360

    # Base methods
    def check_event(self, event):
        super().check_event(event)

        self.camera.check_event(event)

    def update(self, dt):
        self.camera.empty()
        self.camera.add(*self.entities, self.player)

        self.handle_button_inputs(dt)
        self.handle_movement_inputs(dt)

        self.camera.look_at(self.player.rect.centerx, self.player.rect.centery)
    
    def render(self, surface):
        self.camera.draw(surface)