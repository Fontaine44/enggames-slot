from machine import Machine
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
        self.machine = Machine()
        self.delta_time = 0
    
    def quit(self):
        if self.machine.buttons.ser is not None:
            self.machine.buttons.ser.close()
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

            # self.screen.blit(self.bg_image, (0, 0))
            # self.screen.fill(BLACK)
            # slot_zone = pygame.draw.rect(self.screen, RED, REELS_ZONE) # Slot
            # bottom_zone = pygame.draw.rect(self.screen, GREEN, BOTTOM_UI_ZONE) # Balance
            # side_zone = pygame.draw.rect(self.screen, BLUE, SIDE_UI_ZONE) # Info
            rects_to_update = self.machine.update(self.delta_time)
            # self.screen.blit(self.grid_image, (0, 0))

            pygame.display.update(rects_to_update)

            self.clock.tick(FPS)

def main():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        game.machine.input.ser.close()

if __name__ == '__main__':
    main()

# import cProfile as profile
# profile.run('main()')