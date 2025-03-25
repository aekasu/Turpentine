from state import State
from inputs import ControllerHandler

class DebugState(State):
    def __init__(self, game, **kwargs):
        super().__init__(game, True)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, dt):
        controller_name = None
        if self.controller:
            controller_name = self.controller.get_name()

        self.lines = [
            f'FPS: {int(self.game.clock.get_fps())}',
            f'Controller: {controller_name}',
            f'Coordinates: {self.player.x}, {self.player.y}',
            f'Rotation: {int(self.player.angle)}°',
        ]

    def render(self, surface):
        x, y = 0, 0
        for line in self.lines:
            self.game.font.render(surface, line, (x,y), bgcolor='black', size=1)
            y += 15