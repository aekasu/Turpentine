import pygame
pygame.joystick.init()

class ActionHandler:
    def __init__(self, key_action_mapping=None):
        self.key_action_mapping = key_action_mapping or {} # pygame.K_a: 'left'
        self.actions = {
            action: False \
            for action in key_action_mapping
        } # 'left': False
    
    def trigger(self, key, value=True):
        if not key or not (action:=self.key_action_mapping.get(key, None)):
            return
        self.actions[action] = value
    
    def reset(self, key):
        self.trigger(key, False)

# used to process inputs to device and trigger actions mapped to any watched inputs
class InputHandler:
    def __init__(self, key_action_mapping):
        self.action_handler = ActionHandler(key_action_mapping)
    
    def process_inputs(self, event):
        pass

    def check_action(self, action):
        return self.action_handler.actions.get(action, False)

class KeyboardHandler(InputHandler):
    def __init__(self, key_action_mapping):
        super().__init__(key_action_mapping)

    def process_inputs(self, event):
        keys = pygame.key.get_pressed()
        for key in self.key_action_mapping:
            if keys[key]:
                self.action_handler.trigger(key)
    
        if event.type == pygame.KEYUP:
            self.action_handler.reset(event.key)

class ControllerHandler(InputHandler):
    def __init__(self, key_action_mapping=None, controller=None):
        self.left_stick_x = 0  
        self.left_stick_y = 1  
        self.right_stick_x = 3  
        self.right_stick_y = 4  

        # used for processing joystick inputs based on axes
        self.axis_mapping = {
            (self.left_stick_y, -1): 'move_up',     
            (self.left_stick_y, 1): 'move_down',
            (self.left_stick_x, -1): 'move_left',  
            (self.left_stick_x, 1): 'move_right',  
            (self.right_stick_x, -1): 'turn_left',   
            (self.right_stick_x, 1): 'turn_right',
            (self.right_stick_y, -1): 'turn_down',
            (self.right_stick_y, 1): 'turn_up',   
        }

        key_action_mapping = key_action_mapping or {}
        key_action_mapping.update(self.axis_mapping) # adds joystick actions to triggerable actions

        super().__init__(key_action_mapping)

        self.controller = controller
        self.deadzone = 0.2
        self.last_rumble = 0
        self.rumble_cooldown = 500

        self.init_controller()
    
    def init_controller(self):
        if self.controller:
            return

        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
        else:
            print('Controller error: no controller found')
    
    def process_inputs(self, event):
        if not self.controller:
            return
        
        # joystick inputs
        for axis_dir, action in self.axis_mapping.items():
            self.action_handler.reset(axis_dir)

            axis, direction = axis_dir
            axis_value = self.controller.get_axis(axis)
            
            if abs(axis_value) < self.deadzone:
                continue

            if (direction < 0 and axis_value < 0) or (direction > 0 and axis_value > 0): 
                self.action_handler.trigger(axis_dir, abs(axis_value))
        
        # button inputs
        if event.type == pygame.JOYBUTTONDOWN and event.joy == self.controller.get_id():
            self.action_handler.trigger(event.button)
        
        elif event.type == pygame.JOYBUTTONUP:
            self.action_handler.reset(event.button) 
    
    def rumble(self, duration=500, intensity=0.7):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rumble < self.rumble_cooldown:
            return

        self.last_rumble = current_time

        if self.controller:
            try:
                self.controller.rumble(intensity, intensity, duration)
            except Exception as e:
                print(f'Controller rumble error: {e}')