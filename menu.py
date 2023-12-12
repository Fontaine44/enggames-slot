from settings import *
import pygame

class Menu:
    def __init__(self, state_machine):
        self.state_machine = state_machine

        # Create surfaces
        self.display_surface = pygame.display.get_surface()
        self.display_rect = self.display_surface.get_rect()
    

    def check(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.state_machine.next()


    def update(self, delta_time):
        self.check()
        self.display_surface.fill(RED)
        return self.display_rect
