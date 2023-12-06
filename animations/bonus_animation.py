from settings import *
from .animation import *
import pygame
from pygame import gfxdraw
# import random

class BonusAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.reels_surface = machine.reels_surface

        self.wheel_img = pygame.image.load(WHEEL_PATH).convert_alpha()
        self.wheel_img = pygame.transform.smoothscale(self.wheel_img, (WHEEL_SIZE, WHEEL_SIZE))
        self.arrow_img = pygame.image.load(ARROW_PATH).convert_alpha()
        self.arrow_img = pygame.transform.smoothscale(self.arrow_img, (ARROW_SIZE, ARROW_SIZE))

        self.reset()
    
    def start(self, bonus_data):
        self.bonus_data = bonus_data
        self.playing = True
        self.set_symbols_state(True, self.bonus_data)        # Start first animation
    
    def reset(self):
        self.current_animation_time = 0
        self.state = 0
        self.bonus_data = None
        self.wheel = None
    
    def stop(self):
        self.playing = False
        self.reset()

    def play(self):
        if self.playing:
            self.current_animation_time += 1

            # State 0 (highlight)
            if self.state == 0:
                # Go to state 1
                if self.current_animation_time > FPS*1:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.state += 1
                    self.wheel = Wheel(self)

            # State 1 (wheel)
            elif self.state == 1:
                self.wheel.draw()


    # Toggle state on symbols
    def set_symbols_state(self, activate, bonus_data):
        # Turn on/off bonus animation on winning symbols
        for sym_pos in bonus_data:
            symbol = self.machine.spin_result_obj[sym_pos[0]][sym_pos[1]]
            symbol.bonus = activate


class Wheel():
    def __init__(self, bonus):
        self.reels = bonus.reels_surface

        self.centerx = REELS_ZONE[0] + REELS_ZONE[2]//2
        self.centery = REELS_ZONE[1] + REELS_ZONE[3]//2

        self.original_arrow = bonus.arrow_img
        # Set initial position and angle
        self.arrow_rect = self.original_arrow.get_rect(bottomleft=(self.centerx-ARROW_SIZE//2, self.centery))

        self.wheel_img = bonus.wheel_img
        self.wheel_rect = self.wheel_img.get_rect(center=(self.centerx, self.centery))
        
        self.angle = 0
        self.spin_time = 0
        self.rotation_speed = 8

        self.desired_angle = 90
        self.slowdown_drift = 105
        self.full_speed_angle = FPS*2*self.rotation_speed
        self.slowdown_angle = -(360-(self.full_speed_angle % 360) + self.full_speed_angle + self.desired_angle + self.slowdown_drift)
        self.real_angle = self.desired_angle + self.rotation_speed - 1 - (self.desired_angle%self.rotation_speed)
        self.decrement_factor = 0.03
    
    def draw(self):
        # Rotate arrow around the end
        rotated_arrow = pygame.transform.rotozoom(self.original_arrow, self.angle, 1)
        rotated_rect = rotated_arrow.get_rect(center=self.arrow_rect.midbottom)

        # Blit Arrow and Wheel
        self.reels.blit(self.wheel_img, self.wheel_rect.topleft)
        self.reels.blit(rotated_arrow, rotated_rect.topleft)

        # # Small black dot
        # gfxdraw.aacircle(self.reels, self.centerx, self.centery, DOT_SIZE, BLACK)
        # gfxdraw.filled_circle(self.reels, self.centerx, self.centery, DOT_SIZE, BLACK)

        self.spin_time += 1

        if self.angle <= self.slowdown_angle:
            self.rotation_speed = pygame.math.lerp(self.rotation_speed, 0, self.decrement_factor)

        self.angle -= self.rotation_speed
        
        if self.rotation_speed < 0.1:
            print("done")
            print((-self.angle%360))
            print(self.spin_time)
            self.rotation_speed = 0