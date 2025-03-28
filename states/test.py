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
        entity_surface = pygame.Surface((50,50)).convert_alpha()
        player_surface = pygame.Surface((30, 30)).convert_alpha()
        entity_surface.fill('red')
        player_surface.fill('green')
        self.entities = [Entity(random.randrange(0, max_range[0]*2), random.randrange(0, max_range[1]*2), entity_surface.copy()) for i in range(entity_amount)]
        self.player = MovingEntity(0,0,player_surface)
        # ---------

        self.camera = Camera(0, 0, max_range[0]+50, max_range[1]+50)
        self.input_handlers = {
            'keyboard': KeyboardHandler({
                pygame.K_w: 'up',
                pygame.K_a: 'left',
                pygame.K_s: 'down',
                pygame.K_d: 'right',
                pygame.K_LEFT: 'rotate_left',
                pygame.K_RIGHT: 'rotate_right',
                pygame.K_UP: 'zoom_in',
                pygame.K_DOWN: 'zoom_out'
            }),
            'controller': ControllerHandler()
        }

        # ---------
        d = DebugState(game, 
            title = 'Camera Test',
            camera = self.camera,
            player = self.player,
            controller = self.input_handlers['controller'],
            keyboard = self.input_handlers['keyboard']
        )
        d.enter_state()

    def handle_button_inputs(self, dt):
        # Keyboard inputs
        dz = float(self.input_handlers['keyboard'].check_action('zoom_in')) - float(self.input_handlers['keyboard'].check_action('zoom_out'))
        dz *= 1

        # Analog controller inputs
        dz += float(self.input_handlers['controller'].check_action('right_trigger')) - float(self.input_handlers['controller'].check_action('left_trigger'))
        

        # Process the values
        pre_zoom = self.camera.zoom
        self.camera.update_zoom(dz * dt)

        if self.input_handlers['controller'].controller:
            if self.camera.zoom in [self.camera.min_zoom, self.camera.max_zoom] and self.camera.zoom != pre_zoom:
                self.input_handlers['controller'].rumble(duration=100)

    def handle_movement_inputs(self, dt):        
        move_x, move_y = 0, 0

        # Keyboard inputs
        if self.input_handlers['keyboard'].check_action('up'):
            move_y += 1
        if self.input_handlers['keyboard'].check_action('down'):
            move_y -= 1
        if self.input_handlers['keyboard'].check_action('left'):
            move_x += 1
        if self.input_handlers['keyboard'].check_action('right'):
            move_x -= 1
        if self.input_handlers['keyboard'].check_action('rotate_left'):
            self.player.angle += 1 * self.player.rotation_speed * dt
        if self.input_handlers['keyboard'].check_action('rotate_right'):
            self.player.angle -= 1 * self.player.rotation_speed * dt
        
        # Analog controller inputs
        move_y += float(self.input_handlers['controller'].check_action('move_up'))
        move_y -= float(self.input_handlers['controller'].check_action('move_down'))
        move_x += float(self.input_handlers['controller'].check_action('move_left'))
        move_x -= float(self.input_handlers['controller'].check_action('move_right'))

        # Process the values
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
        self.camera.angle = self.player.angle

        self.handle_button_inputs(dt)
        self.handle_movement_inputs(dt)

        self.camera.look_at(self.player.rect.centerx, self.player.rect.centery)
    
    def render(self, surface):
        self.camera.draw(surface)