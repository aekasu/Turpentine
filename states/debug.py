from state import State
from inputs import ControllerHandler

class DebugState(State):
    def __init__(self, game, **kwargs):
        super().__init__(game, True)

        for key, value in kwargs.items():
            setattr(self, key, value)
        
        if not hasattr(self, 'title'):
            self.title = 'Untitled'

    def update(self, dt):
        controller_name = controller_battery = None
        regions = []
        if self.controller.controller:
            controller_name = self.controller.controller.get_name()
            controller_battery = self.controller.controller.get_power_level()
        
        for region in self.camera.regions:
            if self.camera.position_rect in region:
                regions.append(region)

        self.header = [
            f'FPS: {int(self.game.clock.get_fps())}',
            f'Controller: {controller_name} / {controller_battery}',
            f'Coordinates: {self.player.x}, {self.player.y}',
            f'Camera Coords: {self.camera.position_rect.x}, {self.camera.position_rect.y}',
            f'Region: {len(regions) or "No region."}',
            f'Rotation: {int(self.player.angle)}°',
        ]

        self.footer = [
            f'Movement: W, A, S, D',
            f'Rotation: Arrow keys'
        ]

    def render(self, surface):
        font_size = 18
        title_x, title_y = self.camera.viewport.centerx, 0 + font_size // 2
        header_x, header_y = 0, font_size
        footer_x, footer_y = 0, surface.height - font_size
        
        self.game.font.render(surface, self.title, (title_x, title_y), color='yellow', bgcolor='black', center_text=True)

        for line in self.header:
            self.game.font.render(surface, line, (header_x, header_y), bgcolor='black')
            header_y += font_size
        
        for line in self.footer[::-1]:
            self.game.font.render(surface, line, (footer_x,footer_y), bgcolor='black')
            footer_y -= font_size
