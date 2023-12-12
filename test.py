import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fade-Out Transition")

clock = pygame.time.Clock()

def fade_out(last_scene):
    fade_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    for alpha in range(255, -1, -5):
        fade_surface.fill((0, 0, 0, alpha))
        screen.blit(last_scene, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(30)

# Last Scene
last_scene = pygame.Surface((width, height))
last_scene.fill((255, 0, 0))  # Red background

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fade_out(last_scene.copy())  # Use copy to avoid modifying the original scene
