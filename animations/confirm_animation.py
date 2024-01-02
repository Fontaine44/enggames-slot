from settings import *
from .animation import *
import pygame

class ConfirmAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.buttons = machine.buttons

        # Images
        self.blur = pygame.image.load(BLUR_IMAGE_PATH).convert_alpha()
        self.confirm_0 = pygame.image.load(CASHOUT_CONFIRM_PATH).convert_alpha()
        self.confirm_1 = pygame.image.load(SIP_CONFIRM_PATH).convert_alpha()

        self.screen_num = None
        self.win_playing = False
        self.sip_playing = False
        self.reset()
    
    def start(self, screen_num):
        self.playing = True
        self.screen_num = screen_num
        self.machine.disallow_spin()

        # Pause win animation if playing
        if self.machine.win_animation.playing:
            self.win_playing = True
            self.machine.win_animation.pause()
        
        # Pause sip animation if playing
        if self.machine.sip_animation.playing:
            self.sip_playing = True
            self.machine.sip_animation.pause()

        # Start police sound
        if screen_num == 1:
            self.machine.sound.stop_main_sound()
            self.machine.sound.play_police_sound()
    
    def reset(self):
        self.current_animation_time = 0
        self.screen_num = None
        self.win_playing = False
        self.sip_playing = False

    def stop(self):
        self.playing = False
        self.reset()

    def play(self, delta_time):
        if self.playing:
            self.current_animation_time += 1

            self.display_images()
        
            if self.current_animation_time == FPS:
                self.machine.buttons.clear_buffer()
            
            if self.current_animation_time > FPS:
                self.check_input()
    
    def display_images(self):
        self.machine.display_surface.blit(self.machine.bottom_ui_surface, BOTTOM_UI_ZONE)
        self.machine.display_surface.blit(self.machine.side_ui_surface, SIDE_UI_ZONE)
        self.machine.display_surface.blit(self.blur, (0, 0))

        if self.screen_num == 0:
            self.machine.display_surface.blit(self.confirm_0, (0, 0))
        elif self.screen_num == 1:
            self.machine.display_surface.blit(self.confirm_1, (0, 0))

    def check_input(self):
        self.buttons.refresh_input()

        if self.buttons.red_pressed:
            self.red_pressed()
        elif self.buttons.green_pressed:
            self.green_pressed()
    
    def red_pressed(self):
        if self.screen_num == 0:
            self.machine.sound.stop_police_sound()
            self.machine.sound.play_main_sound()
            self.stop()
            self.machine.state_machine.next()
        elif self.screen_num == 1:
            self.machine.sound.stop_police_sound()
            self.machine.sound.play_main_sound()
            self.stop()
            self.machine.state_machine.next()

    def green_pressed(self):
        if self.screen_num == 0:
            self.machine.display_surface.blit(self.machine.bottom_ui_surface, BOTTOM_UI_ZONE)
            self.machine.display_surface.blit(self.machine.side_ui_surface, SIDE_UI_ZONE)

            # Restart win animation if it was playing
            if self.win_playing:
                self.machine.win_animation.unpause()
            
            self.stop()
            self.machine.allow_spin()
            pygame.time.delay(200)

        elif self.screen_num == 1:
            self.machine.display_surface.blit(self.machine.bottom_ui_surface, BOTTOM_UI_ZONE)
            self.machine.display_surface.blit(self.machine.side_ui_surface, SIDE_UI_ZONE)

            # Restart sip animation if it was playing
            if self.sip_playing:
                self.machine.sip_animation.unpause()
            
            self.machine.sound.stop_police_sound()
            self.machine.sound.play_main_sound()
            self.stop()
            pygame.time.delay(200)
# Screen 0: confirm cash-out
# Screen 1: confirm sips
