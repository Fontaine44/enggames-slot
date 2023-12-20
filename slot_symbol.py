from settings import *
import pygame

class Symbol(pygame.sprite.Sprite):
    def __init__(self, image, sym_type, pos):
        super().__init__()

        self.sym_type = sym_type
        self.original_image = image.copy()
        self.image = image.copy()
        self.rect = self.image.get_rect(topleft=pos)

        # Used for win animations
        self.size = SYMBOL_SIZE
        self.alpha = 255
        self.scale_factor = 1.0
        self.winning = False
        self.sip = False
        self.bonus = False

    def update(self, sip_animation, bonus_animation):
        # Fades out non-winning symbols
        if not bonus_animation.playing and not sip_animation.playing:
            self.pos = self.rect.topleft    # Update pos


    def scale_image(self, scale_factor):
        # Scale image
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale_factor)

        # Update top left position
        new_size = self.image.get_size()
        self.rect.topleft = (
            self.pos[0] + (self.size - new_size[0])/2,
            self.pos[1] + (self.size - new_size[1])/2
        )
