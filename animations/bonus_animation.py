from settings import *
from .animation import *
from random import randrange
import pygame

class BonusAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.reels_surface = machine.reels_surface

        self.centerx = REELS_ZONE[0] + REELS_ZONE[2]//2
        self.centery = REELS_ZONE[1] + REELS_ZONE[3]//2

        self.wheel_img = pygame.image.load(WHEEL).convert_alpha()
        self.wheel_img = pygame.transform.smoothscale(self.wheel_img, (WHEEL_SIZE, WHEEL_SIZE))
        self.wheel_rect = self.wheel_img.get_rect(center=(self.centerx, self.centery))

        self.arrow_img = pygame.image.load(ARROW).convert_alpha()
        self.arrow_img = pygame.transform.smoothscale(self.arrow_img, (ARROW_SIZE, ARROW_SIZE))
        self.arrow_rect = self.wheel_img.get_rect(center=(self.centerx, self.centery))

        self.reset()
    
    def start(self, bonus_data):
        self.bonus_data = bonus_data
        self.playing = True
        self.set_symbols_state(True, self.bonus_data)        # Start first animation
        self.machine.sound.play_bonus_sound()
    
    def reset(self):
        self.win = None
        self.current_animation_time = 0
        self.state = 0
        self.bonus_data = None
        self.wheel = None
    
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
                    self.next_state()
                    self.wheel = Wheel(self)

            # State 1 (fade in wheel)
            elif self.state == 1:
                self.wheel.draw_1()
                if self.wheel.alpha > 255 and self.current_animation_time > 2:
                    self.machine.buttons.clear_buffer()
                    self.next_state()

            # State 2 (wait for input button press)
            elif self.state == 2:
                angle = self.wheel.draw_2()
                spin = self.get_input()
                if spin:
                    self.machine.sound.play_wheel_sound()
                    self.next_state()

            # State 3 (spin wheel)
            elif self.state == 3:
                angle = self.wheel.draw_3()
                if angle is not None:
                    self.machine.sound.stop_wheel_sound()
                    # Determine win here
                    self.next_state()
            
            # State 4 (give reward/punish)
            elif self.state == 4:
                self.wheel.draw_4()
                if self.current_animation_time > 3:
                    self.next_state()
            
            # State 5 (fade out wheel)
            elif self.state == 5:
                self.wheel.draw_5()
                if self.wheel.alpha < 0:
                    self.stop()
                    self.machine.allow_spin()   # Allow new spin
    
    def get_input(self):
        self.machine.buttons.refresh_input()
        return self.machine.buttons.green_pressed

    # Toggle state on symbols
    def set_symbols_state(self, activate, bonus_data):
        # Turn on/off bonus animation on winning symbols
        for sym_pos in bonus_data:
            symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
            symbol.bonus = activate

    def next_state(self):
        self.current_animation_time = 0
        self.state += 1


class Wheel():
    def __init__(self, bonus):
        self.bonus = bonus
        self.reels = bonus.reels_surface

        self.alpha = 0

        self.centerx = bonus.centerx
        self.centery = bonus.centery

        self.original_arrow = bonus.arrow_img
        self.arrow_rect = self.original_arrow.get_rect(bottomleft=(self.centerx-ARROW_SIZE//2, self.centery))

        self.wheel_img = bonus.wheel_img.copy()
        self.wheel_rect = bonus.wheel_rect
        
        self.angle = 0
        self.rotation_speed = 8

        self.desired_angle = randrange(0, 360)
        self.slowdown_drift = 105
        self.full_speed_angle = FPS*2*self.rotation_speed
        self.slowdown_angle = -(360-(self.full_speed_angle % 360) + self.full_speed_angle + self.desired_angle + self.slowdown_drift)
        self.decrement_factor = 0.03

    def draw_1(self):
        self.alpha += 4
        self.wheel_img.set_alpha(self.alpha)
        self.original_arrow.set_alpha(self.alpha)

        # Blit Arrow and Wheel
        self.reels.blit(self.wheel_img, self.wheel_rect.topleft)
        self.reels.blit(self.original_arrow, self.arrow_rect.midleft)

    def draw_2(self):
        # Blit Arrow and Wheel
        self.reels.blit(self.wheel_img, self.wheel_rect.topleft)
        self.reels.blit(self.original_arrow, self.arrow_rect.midleft)

    def draw_3(self):
        # Rotate arrow around the end
        self.rotated_arrow = pygame.transform.rotozoom(self.original_arrow, self.angle, 1)
        self.rotated_rect = self.rotated_arrow.get_rect(center=self.arrow_rect.midbottom)

        # Blit Arrow and Wheel
        self.reels.blit(self.wheel_img, self.wheel_rect.topleft)
        self.reels.blit(self.rotated_arrow, self.rotated_rect.topleft)

        if self.angle <= self.slowdown_angle:
            self.rotation_speed = pygame.math.lerp(self.rotation_speed, 0, self.decrement_factor)

        self.angle -= self.rotation_speed
        
        if self.rotation_speed < 0.1:
            self.rotation_speed = 0     # Stop wheel
            return (-self.angle%360)
        
        return None

    def draw_4(self):
        # TODO: Draw reward here in UI

        # Blit Arrow and Wheel
        self.reels.blit(self.wheel_img, self.wheel_rect.topleft)
        self.reels.blit(self.rotated_arrow, self.rotated_rect.topleft)

    def draw_5(self):
        self.alpha -= 6
        self.wheel_img.set_alpha(self.alpha)
        self.rotated_arrow.set_alpha(self.alpha)

        # Blit Arrow and Wheel
        self.reels.blit(self.wheel_img, self.wheel_rect.topleft)
        self.reels.blit(self.rotated_arrow, self.rotated_rect.topleft)