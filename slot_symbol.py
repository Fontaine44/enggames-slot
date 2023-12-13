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
        if bonus_animation.playing:
            self.bonus_animation(bonus_animation.state)
        elif sip_animation.playing:
            pass
        else:
            self.pos = self.rect.topleft    # Update pos
        
    def bonus_animation(self, state):
        if state == 0:
            if self.bonus:
                # Glow
                if self.alpha <= 255:
                    self.alpha += 20
            else:
                # Fade out
                if self.alpha > 95:
                    self.alpha -= 20
            # Update alpha value
            self.image.set_alpha(self.alpha)

        elif state == 1:
            # Fade out
            if self.alpha > 95:
                self.alpha -= 5
            # Update alpha value
            self.image.set_alpha(self.alpha)
        
        elif state == 5:
            if self.bonus:
                # Glow
                if self.alpha <= 255:
                    self.alpha += 2
            # Update alpha value
            self.image.set_alpha(self.alpha)


    def scale_image(self, scale_factor):
        # Scale image
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale_factor)

        # Update top left position
        new_size = self.image.get_size()
        self.rect.topleft = (
            self.pos[0] + (self.size - new_size[0])/2,
            self.pos[1] + (self.size - new_size[1])/2
        )
