from settings import *
from state import State
import pygame

class Video(State):
    def __init__(self, state_machine, sound):
        super().__init__()
        self.state_machine = state_machine
        self.sound = sound

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()

        self.video_time = 0
    
    def start(self):
        self.video_time = 0
        # TODO: start video here

    def update(self, delta_time):
        self.video_time += 1

        if self.video_time == 60: # Video is over
            self.state_machine.next()

        self.display_surface.fill(GREEN)
        return self.display_surface, [self.display_rect]
    
# video with instructions playing full screen
