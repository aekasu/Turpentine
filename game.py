import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame, time

class Font:
    def __init__(self, font_path):
        self.small = pygame.font.Font(font_path, 10)
        self.medium = pygame.font.Font(font_path, 15)
        self.large = pygame.font.Font(font_path, 20)
        self.font_sizes = [self.small, self.medium, self.large]
    
    def render(self, surface, text, location, color=(255, 255, 255), bgcolor=None, size=1):
        font = self.font_sizes[size]
        surface.blit(font.render(text, False, color=color, bgcolor=bgcolor), location)

class Game:
    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1200, 700
        self.GAME_WIDTH, self.GAME_HEIGHT = self.SCREEN_WIDTH, self.SCREEN_HEIGHT
        self.SCREEN_TITLE = 'Turpentine'
        self.ASSET_DIR = os.path.join('assets')
        self.SPRITE_DIR = os.path.join(self.ASSET_DIR, 'sprites')
        self.FONT_DIR = os.path.join(self.ASSET_DIR, 'fonts')
        self.INIT_FONT = 'munro'
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}

        self.fps = 60
        self.dt, self.prev_time = 0, 0
        self.state_stack = []
        self.overlay_state_stack = []
        self.assets = {}
        
        self.init_pygame()

        self.load_assets()
        self.load_states()
        self.running = self.playing = True


    def init_pygame(self):
        pygame.init()
        pygame.display.set_caption(self.SCREEN_TITLE)

        self.pygame_instance = pygame
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.game_canvas = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        self.clock = pygame.time.Clock()
    
    @property
    def current_state(self):
        try:
            return self.state_stack[-1]
        except IndexError:
            print('Error: Game stack empty.')
            self.exit()
            self.quit()
            exit()
    
    def load_states(self):
        self.start_state = StartState(self) #
        self.state_stack.append(self.start_state)
    
    def load_assets(self):
        self.font = None

        for directory in [self.SPRITE_DIR, self.FONT_DIR]:
            for root, _, files in os.walk(directory):
                for file in files:
                    s = os.path.splitext(file)
                    ext = s[1].lower()
                    filename = s[0]
                    file_path = os.path.join(root, file)

                    if ext in self.image_extensions:
                        try:
                            asset = pygame.image.load(file_path).convert()
                        except pygame.error as e:
                            print(f'Error loading image "{file_path}": {e}')            

                    if directory == self.SPRITE_DIR:
                        key = 'sprites'
                        asset.set_colorkey((0,0,0))

                    elif directory == self.FONT_DIR:
                        key = 'fonts'
                        asset = Font(file_path)
                        if filename == self.INIT_FONT:
                            self.font = asset

                    self.assets[key] = asset
        
        if not self.font:
            print(f'Font "{self.INIT_FONT}" was not found.')
        else:
            print('Assets loaded.')
    
    # Mainloop
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit()
            
            self.current_state.check_event(event)
    
    def refresh_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
    
    def update(self):
        self.current_state.update(self.dt)
        for overlay in self.overlay_state_stack:
            overlay.update(self.dt)
    
    def render(self):
        self.game_canvas.fill('black')
        self.current_state.render(self.game_canvas)
        
        for overlay in self.overlay_state_stack:
            overlay.render(self.game_canvas)
        
        self.screen.blit(self.game_canvas, (0,0))
        pygame.display.update()
        self.clock.tick(self.fps)
    
    def mainloop(self):
        while self.playing:
            self.check_events()
            self.refresh_dt()
            self.update()
            self.render()
    
    def exit(self):
        self.playing = self.running = False
    
    def quit(self):
        pygame.quit()

if __name__ == '__main__':
    from states.test import StartState

    g = Game()
    while g.running:
        g.mainloop()
    g.quit()