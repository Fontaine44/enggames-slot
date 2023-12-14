from state import State
from settings import *
from printer import print_ticket
import pygame
import pygame.freetype

class Ticket(State):
    def __init__(self, state_machine, sound, buttons):
        super().__init__()
        self.state_machine = state_machine
        self.sound = sound
        self.buttons = buttons
        self.font = pygame.freetype.Font(FONT_PATH, 150)
        self.player = None
        self.state = None
        self.state_time = 0

        # Create surfaces
        self.display_surface = pygame.Surface((WIDTH, HEIGHT))
        self.display_rect = self.display_surface.get_rect()
        
        # State 0
        self.bankrupt_screen = pygame.image.load(BANKRUPT_IMAGE_PATH).convert_alpha()

        # State 1
        self.cashout_screen = pygame.image.load(CASHOUT_IMAGE_PATH).convert_alpha()
        self.amount_surface = None
        self.amount_pos = None

        # State 2
        self.printing_screen = pygame.image.load(PRINTING_IMAGE_PATH).convert_alpha()
        self.key = None
    
    def pre_start(self):
        # Get player and retrieve balance
        self.player = self.state_machine.states[2].curr_player
        self.amount = self.player.get_balance()

        self.state_time = 0

        if self.amount > 0:
            # Go to state 1
            self.state = 1
            amount_str = str(int(self.amount)) + ' $'
            # Render text to a surface
            self.amount_surface, _ = self.font.render(amount_str, WHITE)
            # Get the size of the rendered text
            amount_width, amount_height = self.amount_surface.get_size()
            # Determine position
            self.amount_pos = ((WIDTH-amount_width)//2, (HEIGHT-amount_height)//2)
        else:
            # Go to state 0 (no money)
            self.state = 0

    def start(self):
        # Clear input
        self.buttons.clear_buffer()
    
    # State 0: Sorry better luck next time
    def state0(self):
        self.state_time += 1

        self.display_surface.blit(self.bankrupt_screen, (0, 0))

        if self.state_time >= FPS*10:
            self.state_machine.next()

    # State 1: Congrats, do you want to print voucher
    def state1(self):
        self.state_time += 1

        self.display_surface.blit(self.cashout_screen, (0, 0))
        self.display_surface.blit(self.amount_surface, self.amount_pos)
        
        self.buttons.refresh_input()
        if self.buttons.green_pressed:
            self.state = 2
            self.state_time = 0

        if self.state_time >= FPS*10 or self.buttons.red_pressed:
            self.state_machine.next()
    
    # State 2: Printing voucher
    def state2(self):
        self.state_time += 1
        
        self.display_surface.blit(self.printing_screen, (0, 0))

        if self.state_time > 1:     # Make sure to blit screen one time
            print_ticket("dfs", self.amount, 12, 1)
            self.state = 3
            self.state_time = 0
    
    # State 3: Take souvenir picture
    def state3(self):
        pass

    def update(self, delta_time):
        if self.state == 0:
            self.state0()
        elif self.state == 1:
            self.state1()
        elif self.state == 2:
            self.state2()
        elif self.state == 3:
            self.state3()

        return self.display_surface, [self.display_rect]
    