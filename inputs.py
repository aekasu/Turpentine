import pygame

class InputHandler:
    def __init__(self, state):
        self.state = state
        self.game = self.state.game
    
    def process_inputs(self, event):
        pass

class KeyboardHandler(InputHandler):
    def __init__(self, state, key_action_mapping):
        super().__init__(state)

        self.key_action_mapping = key_action_mapping

    def process_inputs(self, event):
        keys = pygame.key.get_pressed()
        for key, action in self.key_action_mapping.items():
            if keys[key]:
                self.state.actions[action] = True
    
        if event.type == pygame.KEYUP:
            for key, action in self.key_action_mapping.items():
                if event.key == key:
                    self.state.actions[action] = False

class ControllerHandler(InputHandler):
    def __init__(self, state, controller=None):
        super().__init__(state)

        self.controller = controller
        self.has_controller = controller is not None

        # Axis definitions
        self.left_stick_x = 0  
        self.left_stick_y = 1  
        self.right_stick_x = 3  
        self.right_stick_y = 4  

        self.axis_action_mapping = {
            (self.left_stick_y, -1): 'forward',     
            (self.left_stick_y, 1): 'backward',     
            (self.left_stick_x, -1): 'strafe_left',  
            (self.left_stick_x, 1): 'strafe_right',  
            (self.right_stick_x, -1): 'turn_left',   
            (self.right_stick_x, 1): 'turn_right',   
        }

        self.button_action_mapping = {
            0: 'pause',
        }
        
        self.deadzone = 0.2
    
    def process_inputs(self, event):
        if not self.has_controller:
            return
        
        try:
            for axis_dir, action in self.axis_action_mapping.items():
                axis, direction = axis_dir
                value = self.controller.get_axis(axis)

                if abs(value) < self.deadzone:
                    self.state.actions[action] = False
                    continue
                
                if (direction < 0 and value < 0) or (direction > 0 and value > 0):
                    self.state.actions[action] = abs(value) 
                else:
                    self.state.actions[action] = False
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.joy == self.controller.get_id():
                    for button, action in self.button_action_mapping.items():
                        if event.button == button:
                            self.state.actions[action] = True
            
            elif event.type == pygame.JOYBUTTONUP:
                if event.joy == self.controller.get_id():
                    for button, action in self.button_action_mapping.items():
                        if event.button == button:
                            self.state.actions[action] = False
                            
        except Exception as e:
            print(f'Controller error: {e}')