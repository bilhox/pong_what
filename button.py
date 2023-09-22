import pygame

class Button():

    def __init__(self):

        self._rect = pygame.Rect([0,0],[0,0])
        self._initial_rect = self._rect.copy()

        self._colors = {"nothing":[200, 200, 200], "hover":[150, 150, 150], "clicked":[100, 100, 100]}

        self._surfaces = {}
        self._current_surface = None

        self.clicked = False

        self.state = "nothing"

        self.target = lambda : None

        self.scale_factor = 1
        self._current_scale_factor = 1

        self.scaling_duration = 0.8
        self._scaling_timer = 0

        self._update_surfaces()
        self._update_surface()

    
    def set_colors(self, colors : dict[str, list]) -> None:

        self._colors = colors
        self._update_surfaces()
    
    def set_position(self, position : pygame.Vector2) -> None:

        self._rect.topleft = position
        self._initial_rect.topleft = position

    def get_position(self) -> pygame.Vector2:

        return self._rect.topleft
    
    def set_size(self, size : pygame.Vector2) -> None:

        self._rect.size = size
        self._initial_rect.size = size
        self._update_surfaces()
    
    def get_size(self) -> pygame.Vector2:

        return self._rect.size
    
    def _update_surfaces(self):

        for key, color in self._colors.items():

            surf = pygame.Surface(self._rect.size)
            surf.fill(color)

            self._surfaces[key] = surf
        
        self._update_surface()

    def _update_surface(self):

        self._current_surface = pygame.transform.scale_by(self._surfaces[self.state], self._current_scale_factor)
    
    def update(self, dt):

        if self.clicked and self._scaling_timer <= self.scaling_duration:

            self._current_scale_factor = 1 + (self.scale_factor - 1) * (1 - (1 - self._scaling_timer / self.scaling_duration)**3)
            self._current_surface = pygame.transform.scale_by(self._surfaces[self.state], self._current_scale_factor)
            self._rect.size = pygame.Vector2(self._initial_rect.size) * self._current_scale_factor
            self._rect.center = self._initial_rect.center
            self._scaling_timer += dt

    
    def events(self, event : pygame.Event) -> None:

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self._rect.collidepoint(event.pos):
                self.state = "clicked"
                self.clicked = True
            else:
                self.state = "nothing"
            
            self._update_surface()
        
        elif event.type == pygame.MOUSEBUTTONUP:

            if self.clicked and self._rect.collidepoint(event.pos):
                self.target()
                self.state = "hover"
            
            if self.clicked:
                self.clicked = False
                self._scaling_timer = 0
                self._current_scale_factor = 1
                self._rect.size = pygame.Vector2(self._initial_rect.size) * self._current_scale_factor
                self._rect.center = self._initial_rect.center
                self._current_surface = pygame.transform.scale_by(self._surfaces[self.state], self._current_scale_factor)

            
            self._update_surface()
        
        elif event.type == pygame.MOUSEMOTION:

            if self._rect.collidepoint(event.pos):
                if not self.clicked:
                    self.state = "hover"
                else:
                    self.state = "clicked"
            else:
                self.state = "nothing"

            self._update_surface()
        
    def draw(self, dest : pygame.Surface) -> None:

        dest.blit(self._current_surface, self._rect.topleft)
