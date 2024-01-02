from settings import *
from state import State
import pygame

class Video(State):
    def __init__(self, state_machine, sound):
        super().__init__()
        self.state_machine = state_machine
        self.sound = sound

        self.state = 0
        self.state_times = [2, 4, 4, 2.5]

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()

        self.surfaces = [pygame.image.load(VIDEO_0_PATH).convert_alpha(),
                        pygame.image.load(VIDEO_1_PATH).convert_alpha(),
                        pygame.image.load(VIDEO_2_PATH).convert_alpha(),
                        pygame.image.load(VIDEO_3_PATH).convert_alpha()]

        self.video_time = 0
    
    def pre_start(self):
        self.video_time = 0
        self.state = 0
        
    def update(self, delta_time):
        self.video_time += delta_time

        if self.state == 4:
            self.state_machine.next()
        else:
            self.display_surface.blit(self.surfaces[self.state], (0, 0))

            if self.video_time > self.state_times[self.state]:
                self.video_time = 0
                self.state += 1
        
        return self.display_surface, [self.display_rect]
