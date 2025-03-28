class State:
    def __init__(self, game, is_overlay=False):
        self.game = game
        self.prev_state = None
        self.actions = {}
        self.key_action_mapping = {}
        self.is_overlay = is_overlay
        self.input_handlers = {}

    def check_event(self, event):
        for input_handler in self.input_handlers:
            try:
                self.input_handlers[input_handler].process_inputs(event)
            except Exception as e:
                print(f'Input handler error for "{input_handler}": {e}')

    def update(self, dt):
        ...
    
    def render(self, surface):
        ...
    
    def reset_actions(self):
        for input_handler in self.input_handlers:
            self.input_handlers[input_handler].reset_actions()

    def enter_state(self):
        stack = self.game.state_stack
        if self.is_overlay:
            stack = self.game.overlay_state_stack
        
        if len(stack) >= 1:
            self.prev_state = stack[-1]
        
        stack.append(self)
    
    def exit_state(self):
        if self.is_overlay:
            self.game.overlay_state_stack.pop()
        else:
            self.game.state_stack.pop()
        
