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
        self.bonus = False

    def update(self, win_animation_ongoing, bonus_animation_ongoing, bonus_state=0):
        # Fades out non-winning symbols
        if win_animation_ongoing:
            if self.winning:
                if self.alpha <= 255:
                    self.alpha += 20
            else:
                if self.alpha > 95:
                    self.alpha -= 20
            # Update alpha value
            self.image.set_alpha(self.alpha)

        elif bonus_animation_ongoing:
            if bonus_state == 0:
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
            elif bonus_state == 1:
                if self.bonus:
                    self.scale_factor = pygame.math.lerp(self.scale_factor, self.target_scale, 0.02)
                    self.scale_image()
        else:
            self.pos = self.rect.topleft

    def scale_image(self):
        # Scale image
        self.image = pygame.transform.rotozoom(self.original_image, 0, self.scale_factor)

        # Update top left position
        new_size = self.image.get_size()
        self.rect.topleft = (
            self.pos[0] + (self.size - new_size[0])/2,
            self.pos[1] + (self.size - new_size[1])/2
        )

        # if self.animation_phase == 1:
        #     # Phase 1: Fade out
        #     self.alpha = max(0, self.alpha - 5)
        #     if self.alpha == 0:
        #         self.animation_phase = 0  # Move to the next phase

        # elif self.animation_phase == 2:
        #     # Phase 2: Scale down
        #     self.scale_factor = max(0.1, self.scale_factor - 0.01)
        #     if self.scale_factor == 0.1:
        #         self.animation_phase = 0  # Move to the next phase

        # elif self.animation_phase == 0:
        #     # Pause between phases
        #     if self.animation_timer > 0:
        #         self.animation_timer -= 1
        #     else:
        #         # Reset timer and move to the next phase
        #         self.animation_timer = 60  # 1 second pause
        #         if self.alpha > 0:
        #             self.animation_phase = 1  # Start fading out
        #         elif self.scale_factor > 0.1:
        #             self.animation_phase = 2  # Start scaling down

        # # Update the sprite image with the current alpha and scale
        # self.image.set_alpha(self.alpha)
        # self.image = pygame.transform.rotozoom(self.original_image, 0, self.scale_factor)
