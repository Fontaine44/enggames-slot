from settings import *
from .animation import *
import pygame
import random
from time import sleep

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
        self.set_symbols_state(self.sip_data)        # Start first animation
    
    def reset(self):
        self.current_animation_time = 0
        self.state = 0
        self.sip_data = None
    
    def stop(self):
        self.playing = False
        self.reset()

    def play(self, delta_time):
        if self.playing:
            self.current_animation_time += delta_time

            # State 0 (highlight)
            if self.state == 0:
                # Go to state 1
                if self.current_animation_time > 2:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1
                    self.machine.sound.play_sip_sound()
            
            # State 1 (zoom out)
            elif self.state == 1:
                # Go to state 2
                if self.current_animation_time > 1:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.current_animation_steps = -1
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
                self.current_animation_steps += 1

                if self.current_animation_time > 2:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1
                    self.machine.ui.display_balance()
                    self.machine.ui.display_message(f"TAKE {self.sip_number} SIPS", 120, PINK)

                elif self.current_animation_steps % 6 == 0:
                    # Get a random number image
                    rand_key = random.choices(self.numbers_keys, weights=self.numbers_weights, k=1)[0]
                    self.sip_number = int(rand_key)

                    for sym_pos in self.sip_data:
                        symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.image = self.numbers_images[rand_key]
                    

            # State 3 (wait for the user to take the sips)
            elif self.state == 3:
                if self.current_animation_time > self.sip_number:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1

                    # Random sips check
                    if random.randint(1, 3) == 1:
                        sleep(2)
                        self.machine.confirm_animation.start(1)

            # State 4 (allow new spin or start bonus animation)
            elif self.state == 4:
                
                # Check for bonus
                if self.machine.bonus_data:
                    if self.current_animation_time > self.sip_number:
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
    def set_symbols_state(self, sip_data):
        # Fade out all symbols
        for reel in self.machine.spin_result_obj:
            for symbol in reel:
                symbol.image.set_alpha(95)
        
        # Fade in winning symbols
        for reel, row in sip_data:
            symbol = self.machine.spin_result_obj[reel][row]
            symbol.image.set_alpha(255)