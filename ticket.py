from settings import *
import pygame

class Ticket:
    def __init__(self, state_machine):
        self.state_machine = state_machine

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()

        self.bg = pygame.image.load(BG_IMAGE_PATH)
        self.bg = pygame.transform.smoothscale(self.bg, (WIDTH, HEIGHT))
    

    def check(self):
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.state_machine.next()


    def update(self, delta_time):
        self.check()
        self.display_surface.blit(self.bg, (0, 0))
        return self.display_surface, [self.display_rect]
