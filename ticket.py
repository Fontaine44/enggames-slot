from settings import *
import pygame

class Ticket:
    def __init__(self, state_machine, sound, buttons):
        self.state_machine = state_machine
        self.sound = sound
        self.buttons = buttons

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()

        self.bg = pygame.image.load(BG_IMAGE_PATH)
        self.bg = pygame.transform.smoothscale(self.bg, (WIDTH, HEIGHT))
    
    def start(self):
        # Clear input
        self.buttons.clear_buffer()
        
    def check(self):
        self.buttons.refresh_input()

        if self.buttons.green_pressed:
            self.state_machine.next()

    def update(self, delta_time):
        self.check()
        self.display_surface.blit(self.bg, (0, 0))
        return self.display_surface, [self.display_rect]
    

# Do you want to print a ticket?

# Do you want to take a souvenir picture?
