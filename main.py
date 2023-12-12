from state_machine import StateMachine
from settings import *
import ctypes
import pygame
import sys

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):

        # General Setup
        pygame.init()
        # flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, 16, vsync=1)

        pygame.display.set_caption('MGCIL DRINKING SLOT MACHINE')
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])
        self.clock = pygame.time.Clock()

        self.state_machine = StateMachine()

        self.delta_time = 0
    
    def quit(self):
        self.state_machine.close()
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

            rects_to_update = self.state_machine.update(self.delta_time)
            pygame.display.update(rects_to_update)

            self.clock.tick(FPS)

def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        game.state_machine.close()

if __name__ == '__main__':
    main()

# import cProfile as profile
# profile.run('main()')