from state import State
from settings import *
from printer import print_ticket
import pygame
import pygame.freetype
import cv2
from time import sleep

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

        # State 3
        self.photo_screen = pygame.image.load(PHOTO_IMAGE_PATH).convert_alpha()
        self.countdown_1 = pygame.image.load(COUNTDOWN_1_PATH).convert_alpha()
        self.countdown_2 = pygame.image.load(COUNTDOWN_2_PATH).convert_alpha()
        self.countdown_3 = pygame.image.load(COUNTDOWN_3_PATH).convert_alpha()
        self.webcam_rect = ((WIDTH-WEBCAM_WIDTH)//2, (HEIGHT-WEBCAM_HEIGHT)//2, WEBCAM_WIDTH, WEBCAM_HEIGHT)
        self.cap = None
        self.take_photo = False
        self.photo_countdown = 0

    
    def pre_start(self):
        # Get player and retrieve balance
        self.player = self.state_machine.states[2].player
        self.amount = self.player.get_balance()

        self.take_photo = False
        self.cap = None

        self.buttons.clear_buffer()

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
        pass

    # State 0: Sorry better luck next time
    def state0(self, delta_time):
        self.state_time += delta_time

        self.display_surface.blit(self.bankrupt_screen, (0, 0))

        if self.state_time >= 10:
            self.state_machine.next()
        
        return self.display_surface, [self.display_rect]

    # State 1: Congrats, do you want to print voucher
    def state1(self, delta_time):
        self.state_time += delta_time

        self.display_surface.blit(self.cashout_screen, (0, 0))
        self.display_surface.blit(self.amount_surface, self.amount_pos)
        
        if self.state_time > 1:
            self.buttons.refresh_input()
            if self.buttons.green_pressed:
                self.state = 2
                self.state_time = 0

            if self.state_time >= 30 or self.buttons.red_pressed:
                self.state_machine.next()
        
        return self.display_surface, [self.display_rect]
    
    # State 2: Printing voucher
    def state2(self, delta_time):
        self.state_time += delta_time
        
        self.display_surface.blit(self.printing_screen, (0, 0))

        if self.state_time > 0.3:     # Make sure to blit screen one time
            # TODO: print ticket with good id and stats
            print_ticket("dfs", self.amount, 12, 1)
            self.state = 3
            self.state_time = 0
            self.buttons.clear_buffer()
        
        return self.display_surface, [self.display_rect]
    
    # State 3: Take souvenir picture
    def state3(self, delta_time):
        self.state_time += delta_time

        # Print background first
        if self.state_time <= 4:
            self.display_surface.blit(self.photo_screen, (0, 0))

        # Create webcam object once
        if self.state_time >= 1 and not self.cap:
            try:
                self.cap = cv2.VideoCapture(WEBCAM_PORT, cv2.CAP_DSHOW)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)
            except:
                self.cap = None
                self.state_machine.next()
                print("Failed to init webcam object")

        # Capture and blit frame
        if self.state_time > 1 and self.cap:

            # Capture a frame from the camera
            ret, frame = self.cap.read()
            
            # Check for succesful capture
            if ret:
                # Convert the OpenCV frame to Pygame surface
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.transpose(frame)
                frame = cv2.flip(frame, 0)
                frame_surface = pygame.surfarray.make_surface(frame)
                # Blit the frame onto the Pygame screen
                self.display_surface.blit(frame_surface, self.webcam_rect)
            else:
                print("Failed to capture webcam")
                self.cap.release()
                self.state_machine.next()


            # Check if countdown is on or check for input
            if self.take_photo:
                self.photo_countdown += delta_time

                if self.photo_countdown <= 1:
                    self.display_surface.blit(self.countdown_3, (0, 0))
                elif 1 < self.photo_countdown <= 2 :
                    self.display_surface.blit(self.countdown_2, (0, 0))
                elif self.photo_countdown < 3:
                    self.display_surface.blit(self.countdown_1, (0, 0))
                elif self.photo_countdown >= 3.5:
                    # TODO: save picture and show it for 15 seconds or next button press
                    sleep(5)
                    self.cap.release()
                    self.state_machine.next()
            else:
                # Check for button press
                self.buttons.refresh_input()
                if self.buttons.green_pressed:
                    self.photo_countdown = 0
                    self.take_photo = True
            
            
        if self.state_time <= 4:
            return self.display_surface, [self.display_rect]
        elif self.state_time >= 30 and not self.take_photo:
            self.cap.release()
            self.state_machine.next()
        
        return self.display_surface, [self.webcam_rect]

    def update(self, delta_time):
        if self.state == 0:
            return self.state0(delta_time)
        elif self.state == 1:
            return self.state1(delta_time)
        elif self.state == 2:
            return self.state2(delta_time)
        elif self.state == 3:
            return self.state3(delta_time)
    