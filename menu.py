from settings import *
from state import State
import pygame

class Menu(State):
    def __init__(self, state_machine, sound, buttons):
        super().__init__()
        self.state_machine = state_machine
        self.sound = sound
        self.buttons = buttons

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()
    
    def start(self):
        # TODO: start leaderboard scrolling here
        self.buttons.clear_buffer()

    def check(self):
        self.buttons.refresh_input()

        if self.buttons.green_pressed:
            self.state_machine.next()

    def update(self, delta_time):
        self.check()
        self.display_surface.fill(RED)
        return self.display_surface, [self.display_rect]
    

# Leader board scrolling

# Bottom with instructions for red/green buttons