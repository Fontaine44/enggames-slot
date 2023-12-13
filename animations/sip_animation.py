from settings import FPS, NUMBERS_PATH, SYMBOL_SIZE, NUMBERS_WEIGHT
from .animation import *
from time import sleep
import pygame
import random

class SipAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        # Images for sip animation
        self.numbers_images = self.machine.load_images_dict(NUMBERS_PATH, size=(SYMBOL_SIZE, SYMBOL_SIZE))
        self.numbers_keys = list(NUMBERS_PATH.keys())
        self.numbers_weights = [NUMBERS_WEIGHT[k] for k in self.numbers_keys]

        self.sip_number = None
        self.sip_scale_factor = 1.0
        self.reset()
    
    def start(self, sip_data):
        self.sip_data = sip_data
        self.playing = True
        self.set_symbols_state(True, self.sip_data)        # Start first animation
    
    def reset(self):
        self.current_animation_time = 0
        self.state = 0
        self.sip_data = None
    
    def stop(self):
        self.playing = False
        self.reset()

    def play(self):
        if self.playing:
            self.current_animation_time += 1

            # State 0 (highlight)
            if self.state == 0:
                # Go to state 1
                if self.current_animation_time > FPS*2:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1
            
            # State 1 (zoom out)
            elif self.state == 1:
                # Go to state 2
                if self.current_animation_time > FPS:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1
                    self.sip_scale_factor = 1.0

                    # Rescale images
                    for sym_pos in self.sip_data:
                        symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.scale_image(1.0)

                else:
                    # Zoom out
                    self.sip_scale_factor = pygame.math.lerp(self.sip_scale_factor, 0, 0.10)
                    for sym_pos in self.sip_data:
                        symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.scale_image(self.sip_scale_factor)
            
            # State 2 (random numbers)
            if self.state == 2:
                if self.current_animation_time > FPS*3:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1

                elif self.current_animation_time % 10 == 0:
                    # Get a random number image
                    rand_key = random.choices(self.numbers_keys, weights=self.numbers_weights, k=1)[0]
                    self.sip_number = int(rand_key)

                    for sym_pos in self.sip_data:
                        symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.image = self.numbers_images[rand_key]
                    

            # State 3 (wait for the user to take the sips)
            elif self.state == 3:
                if self.current_animation_time > FPS*self.sip_number:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1

            # State 4 (allow new spin or start bonus animation)
            elif self.state == 4:
                self.set_symbols_state(False, self.sip_data)
                
                # Check for bonus
                if self.machine.bonus_data:
                    sleep(self.sip_number)
                    
                    # Reset image to sip symbol
                    for sym_pos in self.sip_data:
                        symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.image = symbol.image.copy()

                    self.stop()
                    self.machine.bonus_animation.start(self.machine.bonus_data)
                else:
                    self.stop()
                    self.machine.allow_spin()   # Allow new spin

    # Toggle state on symbols
    def set_symbols_state(self, activate, sip_data):
        # Turn on/off sip animation on winning symbols
        for sym_pos in sip_data:
            symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
            symbol.sip = activate