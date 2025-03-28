<<<<<<< HEAD
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
=======
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
>>>>>>> origin
    
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
<<<<<<< HEAD
        self.camera.draw(surface)
=======
        surface.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Press SPACE to Start", True, (255, 255, 255))
        surface.blit(text, (400, 300))
        pygame.display.flip()
>>>>>>> origin
