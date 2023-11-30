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
        self.target_scale = 0  # Target scale for the animation
        self.winning = False
        self.sip = False
        self.bonus = False

    def update(self, win_animation_ongoing, sip_animation_ongoing, bonus_animation_ongoing, state):
        # Fades out non-winning symbols
        if win_animation_ongoing:
            self.win_animation()
        elif sip_animation_ongoing:
            self.sip_animation(state)
        elif bonus_animation_ongoing:
            self.bonus_animation()
        else:
            self.pos = self.rect.topleft    # Update pos

    def win_animation(self):
        if self.winning:
            if self.alpha <= 255:
                self.alpha += 20
        else:
            if self.alpha > 95:
                self.alpha -= 20
        # Update alpha value
        self.image.set_alpha(self.alpha)
    
    def sip_animation(self, state):
        if state == 0:
            if self.sip:
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
            if self.sip:
                self.scale_factor = pygame.math.lerp(self.scale_factor, self.target_scale, 0.05)
                self.scale_image(self.scale_factor)
    
    def bonus_animation():
        pass

    def scale_image(self, scale_factor):
        # Scale image
        self.image = pygame.transform.rotozoom(self.original_image, 0, scale_factor)

        # Update top left position
        new_size = self.image.get_size()
        self.rect.topleft = (
            self.pos[0] + (self.size - new_size[0])/2,
            self.pos[1] + (self.size - new_size[1])/2
        )
