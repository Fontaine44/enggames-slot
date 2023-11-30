import pygame
import sys

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Smooth Scale-Down Animation")

# Define a custom sprite class
class MySprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.scale_factor = 1.0
        self.target_scale = 0.5  # Target scale for the animation

    def update(self):
        # Linear interpolation (lerp) to smoothly transition between scale factors
        self.scale_factor = pygame.math.lerp(self.scale_factor, self.target_scale, 0.05)
        # Scale the original image
        self.image = pygame.transform.rotozoom(self.original_image, 0, self.scale_factor)

# Load sprite image
sprite_image = pygame.image.load("graphics//symbols//wah.png")

# Create a sprite group
sprite_group = pygame.sprite.Group()

# Create an instance of the custom sprite class
my_sprite = MySprite(sprite_image, (100, 100))

# Add the sprite to the group
sprite_group.add(my_sprite)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_DOWN:
                # Trigger the scale-down animation
                my_sprite.target_scale = 0.1  # You can adjust the target scale as needed

    sprite_group.update()

    screen.fill((255, 255, 255))

    # Draw all sprites in the group
    sprite_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
