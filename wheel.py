import pygame
from pygame import gfxdraw
import math
from settings import *
import ctypes, pygame, sys

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):

        # General setup
        pygame.init()
        # flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, 16, vsync=1)
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MGCIL DRINKING SLOT MACHINE')
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.delta_time = 0


        self.arrow_image = pygame.image.load(ARROW_PATH).convert_alpha()
        self.arrow_image = pygame.transform.smoothscale(self.arrow_image, (ARROW_SIZE, ARROW_SIZE))
        self.original_arrow = self.arrow_image

        self.centerx = WIDTH//2
        self.centery = HEIGHT//2

        # Set initial position and angle
        self.arrow_rect = self.arrow_image.get_rect(bottomleft=(self.centerx-ARROW_SIZE//2, self.centery))
        
        self.angle = 0
        self.spin_time = 0
        self.rotation_speed = 8

        self.desired_angle = 96
        self.slowdown_drift = 105
        self.full_speed_angle = FPS*2*self.rotation_speed
        self.slowdown_angle = -(360-(self.full_speed_angle % 360) + self.full_speed_angle + self.desired_angle + self.slowdown_drift)
        self.real_angle = self.desired_angle + self.rotation_speed - 1 - (self.desired_angle%self.rotation_speed)
        print(self.real_angle)
        self.decrement_factor = 0.03


    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while 1:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.quit()

            # Time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            # Rotate arrow around the end
            # rotated_arrow = pygame.transform.rotate(original_arrow, angle)
            rotated_arrow = pygame.transform.rotozoom(self.original_arrow, self.angle, 1)
            rotated_rect = rotated_arrow.get_rect(center=self.arrow_rect.midbottom)

            self.screen.fill(WHITE)

            # Red circle
            gfxdraw.aacircle(self.screen, self.centerx, self.centery, WHEEL_SIZE, RED)
            gfxdraw.filled_circle(self.screen, self.centerx, self.centery, WHEEL_SIZE, RED)
            
            # Arrow
            self.screen.blit(rotated_arrow, rotated_rect.topleft)
            # pygame.draw.rect(self.screen, BLACK, rotated_rect, 2)
            
            # Small black dot
            gfxdraw.aacircle(self.screen, self.centerx, self.centery, DOT_SIZE, BLACK)
            gfxdraw.filled_circle(self.screen, self.centerx, self.centery, DOT_SIZE, BLACK)

            pygame.display.flip()

            self.spin_time += 1

            if self.angle <= self.slowdown_angle:
                self.rotation_speed = pygame.math.lerp(self.rotation_speed, 0, self.decrement_factor)

            self.angle -= self.rotation_speed
            
            current_angle = (-self.angle%360)
            abc =  self.desired_angle-1 <= current_angle and current_angle >= self.desired_angle+1
            if self.rotation_speed < 0.1:
                print("done")
                print((-self.angle%360))
                print(self.spin_time)
                self.rotation_speed = 0
                exit()

            self.clock.tick(FPS)
        

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()