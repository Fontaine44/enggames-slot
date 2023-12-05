import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rotating Arrow")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load long arrow image
arrow_image = pygame.image.load("graphics/wheel/arrow.svg").convert_alpha()
original_arrow = arrow_image  # Save the original arrow for reference

# Set initial position and angle
arrow_rect = arrow_image.get_rect(bottomleft=(width // 4, height // 2))
angle = 0

# Set rotation speed
rotation_speed = 10

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Rotate arrow around the end
    # rotated_arrow = pygame.transform.rotate(original_arrow, angle)
    rotated_arrow = pygame.transform.rotozoom(original_arrow, angle, 1)
    rotated_rect = rotated_arrow.get_rect(center=arrow_rect.midbottom)
    

    # Draw to the screen
    screen.fill(white)
    screen.blit(rotated_arrow, rotated_rect.topleft)

    # pygame.draw.rect(screen, black, arrow_rect, 2)
    pygame.draw.rect(screen, black, rotated_rect, 2)

    wheel_surface = pygame.draw.circle(screen, black, (width/2, height/2), 20, 0) #(r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
    # screen.blit(self.arrow, (WIDTH/2, HEIGHT/2))

    # Update the display
    pygame.display.flip()

    # Increment angle for the next frame
    angle += rotation_speed

    # Control the frame rate
    pygame.time.Clock().tick(60)
