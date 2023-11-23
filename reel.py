from settings import *
import pygame, random

class Reel:
    def __init__(self, symbols_surfaces, pos):
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(SYMBOLS_PATH.keys())
        random.shuffle(self.shuffled_keys)
        self.weights = [SYMBOLS_WEIGHT[k] for k in self.shuffled_keys]
        self.symbols_surfaces = symbols_surfaces

        self.reel_is_spinning = False

        # Sounds
        # self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
        # self.stop_sound.set_volume(0.5)

        # Init symbols in reel
        for idx in range(5):
            rand_key = random.choices(self.shuffled_keys, weights=self.weights, k=1)[0]
            image = self.symbols_surfaces[rand_key]
            self.symbol_list.add(Symbol(image, rand_key, pos, idx))
            pos = list(pos)
            pos[1] += 300
            pos = tuple(pos)

    def animate(self, delta_time):
        if self.reel_is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            reel_is_stopping = False

            if self.spin_time < 0:
                reel_is_stopping = True

            # Stagger reel spin start animation
            if self.delay_time <= 0:

                # Iterate through all symbols in reel; truncate; add new random symbol on top of stack
                for symbol in self.symbol_list:
                    symbol.rect.bottom += 100

                    # Correct spacing is dependent on the above addition eventually hitting 1200
                    if symbol.rect.top == 1200:
                        if reel_is_stopping:
                            self.reel_is_spinning = False
                            # self.stop_sound.play()

                        symbol_idx = symbol.idx
                        symbol.kill()
                        # Spawn random symbol in place of the above
                        rand_key = random.choices(self.shuffled_keys, weights=self.weights, k=1)[0]
                        image = self.symbols_surfaces[rand_key]
                        new_symbol = Symbol(image, rand_key, ((symbol.x_val), -300), symbol_idx)
                        self.symbol_list.add(new_symbol)

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = 1000 + delay_time
        self.reel_is_spinning = True

    # Gets and returns the symbols and sprites in a given reel
    def reel_spin_result(self):
        spin_symbols_obj = []
        spin_symbols = []
        sprites = self.symbol_list.sprites()
        for i in GAME_INDICES:
            spin_symbols_obj.append(sprites[i])
            spin_symbols.append(sprites[i].sym_type)
        return spin_symbols[::-1], spin_symbols_obj[::-1]

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

        