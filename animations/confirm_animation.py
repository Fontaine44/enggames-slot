from settings import *
from .animation import *
from time import sleep
import pygame

class ConfirmAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.buttons = machine.buttons

        # Images
        self.blur = pygame.image.load(BLUR_IMAGE_PATH).convert_alpha()

        self.screen_num = None
        self.win_playing = True
        self.reset()
    
    def start(self, screen_num):
        self.playing = True
        self.screen_num = screen_num
        self.machine.disallow_spin()

        # Pause win animation if playing
        if self.machine.win_animation.playing:
            self.win_was_playing = True
            self.machine.win_animation.pause()
    
    def reset(self):
        self.current_animation_time = 0
        self.screen_num = None

    def stop(self):
        self.playing = False
        self.reset()

    def play(self, delta_time):
        if self.playing:
            self.current_animation_time += 1

            self.display_images()
        
            if self.current_animation_time == FPS*2:
                self.machine.buttons.clear_buffer()
            
            if self.current_animation_time > FPS*2:
                self.check_input()
    
    def display_images(self):
        self.machine.display_surface.blit(self.machine.bottom_ui_surface, BOTTOM_UI_ZONE)
        self.machine.display_surface.blit(self.machine.side_ui_surface, SIDE_UI_ZONE)
        self.machine.display_surface.blit(self.blur, (0, 0))

        if self.screen_num == 0:
            pass

    def check_input(self):
        self.buttons.refresh_input()

        if self.buttons.red_pressed:
            self.red_pressed()
        elif self.buttons.green_pressed:
            self.green_pressed()
    
    def red_pressed(self):
        if self.screen_num == 0:
            self.stop()
            self.machine.state_machine.next()

    def green_pressed(self):
        if self.screen_num == 0:
            self.machine.display_surface.blit(self.machine.bottom_ui_surface, BOTTOM_UI_ZONE)
            self.machine.display_surface.blit(self.machine.side_ui_surface, SIDE_UI_ZONE)
            self.stop()

            # Restart win animation if it was playing
            if self.win_was_playing:
                self.machine.win_animation.unpause()
                
            self.machine.allow_spin()
            sleep(0.1)

# Screen 0: confirm cash-out
