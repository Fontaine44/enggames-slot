from settings import *
import pygame

class Video:
    def __init__(self, state_machine):
        self.state_machine = state_machine

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()
    

    def check(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.state_machine.next()


    def update(self, delta_time):
        self.check()
        self.display_surface.fill(GREEN)
        return self.display_surface, [self.display_rect]
