from machine import Machine
from settings import *
import ctypes, pygame, sys

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MGCIL DRINKING SLOT MACHINE')
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        self.grid_image = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()
        self.machine = Machine()
        self.delta_time = 0

        # Sound
        # main_sound = pygame.mixer.Sound('audio/track.mp3')
        # main_sound.play(loops = -1)
    
    def quit(self):
        if self.machine.buttons.ser is not None:
            self.machine.buttons.ser.close()
        pygame.quit()
        sys.exit()

    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.quit()

            # Time variables
            self.delta_time = (pygame.time.get_ticks() - self.start_time) / 1000
            self.start_time = pygame.time.get_ticks()

            pygame.display.update()
            # self.screen.blit(self.bg_image, (0, 0))
            # self.screen.fill(BLACK)
            pygame.draw.rect(self.screen, RED, REELS_ZONE) # Slot
            pygame.draw.rect(self.screen, GREEN, BOTTOM_UI_ZONE) # Balance
            pygame.draw.rect(self.screen, BLUE, SIDE_UI_ZONE) # Info
            self.machine.update(self.delta_time)
            # self.screen.blit(self.grid_image, (0, 0))
            self.clock.tick(FPS)
            # print(self.clock.get_fps())

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