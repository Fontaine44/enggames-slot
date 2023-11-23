import pygame

class Symbol(pygame.sprite.Sprite):
    def __init__(self, image, sym_type, pos, idx):
        super().__init__()

        self.image = image.copy()
        self.sym_type = sym_type
        self.pos = pos
        self.idx = idx

        self.rect = self.image.get_rect(topleft = pos)
        self.x_val = self.rect.left

        # Used for win animations
        self.size_x = 300
        self.size_y = 300
        self.alpha = 255
        self.winning = False
        self.bonus = False

    def update(self, win_animation_ongoing, bonus_animation_ongoing):
        # Fades out non-winning symbols
        if win_animation_ongoing:
            if self.winning:
                if self.alpha <= 255:
                    self.alpha += 20
            else:
                if self.alpha > 115:
                    self.alpha -= 20
            # Update alpha value
            self.image.set_alpha(self.alpha)

        elif bonus_animation_ongoing:
            if self.bonus:
                if self.alpha <= 255:
                    self.alpha += 20
            else:
                if self.alpha > 115:
                    self.alpha -= 20
            # Update alpha value
            self.image.set_alpha(self.alpha)