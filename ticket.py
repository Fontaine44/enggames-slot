from settings import *
import pygame
import pygame.freetype

class Ticket:
    def __init__(self, state_machine, sound, buttons):
        self.state_machine = state_machine
        self.sound = sound
        self.buttons = buttons
        self.font = pygame.freetype.Font(FONT_PATH, 32)

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()

        self.cashout_screen = pygame.image.load(CASHOUT_IMAGE_PATH).convert_alpha()

        # # text1: CASHING OUT, text2: amount, 
        # # Calculate the position to center the text on the screen
        # x = (width - text_width) // 2
        # y = (height - text_height) // 2
    
    def start(self):
        # Clear input
        self.buttons.clear_buffer()
        
    def check(self):
        self.buttons.refresh_input()

        if self.buttons.green_pressed:
            self.state_machine.next()

    def update(self, delta_time):
        self.check()
        self.display_surface.blit(self.cashout_screen, (0, 0))
        self.font.render_to(self.display_surface, (50, 50), "CASHING OUT", WHITE)
        return self.display_surface, [self.display_rect]
    

# Do you want to print a ticket?

# Do you want to take a souvenir picture?
