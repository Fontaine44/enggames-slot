from settings import *
from slot_symbol import Symbol
import pygame
import random

class Reel:
    def __init__(self, symbols_surfaces, x, y):
        self.x = x
        self.y = y
        self.symbol_list = pygame.sprite.Group()
        self.shuffled_keys = list(SYMBOLS_PATH.keys())
        random.shuffle(self.shuffled_keys)
        self.weights = [SYMBOLS_WEIGHT[k] for k in self.shuffled_keys]
        self.symbols_surfaces = symbols_surfaces
        self.is_spinning = False

        # Create initial symbols
        for i in range(4):
            symbol = self.get_random_symbol(x, y + i*SYMBOL_SIZE)
            self.symbol_list.add(symbol)
    
    # Returns a random symbol object
    def get_random_symbol(self, x, y):
        rand_key = random.choices(self.shuffled_keys, weights=self.weights, k=1)[0]
        image = self.symbols_surfaces[rand_key]
        return Symbol(image, rand_key, (x, y))

    # Move the symbols and remove and add if necessary
    def animate(self, delta_time):
        if self.is_spinning:
            self.delay_time -= (delta_time * 1000)
            self.spin_time -= (delta_time * 1000)
            stop_reel = self.spin_time < 0

            # Spin the reel
            if self.delay_time <= 0:
                # Lower all symbols by the reel speed
                for symbol in self.symbol_list:
                    symbol.rect.top += REEL_SPEED

                    # If the last symbol is below the reel, remove it, and add a new symbol at the front of the list
                    if symbol.rect.top == SYMBOL_SIZE*3:
                        if stop_reel:
                            self.is_spinning = False
                        
                        symbol.kill()
                        # Spawn random symbol in place of the above
                        new_symbol = self.get_random_symbol(self.x, self.y)
                        self.symbol_list.add(new_symbol)

    def start_spin(self, delay_time):
        self.delay_time = delay_time
        self.spin_time = SPIN_TIME + delay_time
        self.is_spinning = True

    # Gets and returns the symbols and sprites in a given reel
    def reel_spin_result(self):
        spin_symbols_obj = []
        spin_symbols = []
        sprites = self.symbol_list.sprites()
        for i in range(2, -1, -1):
            spin_symbols_obj.append(sprites[i])
            spin_symbols.append(sprites[i].sym_type)
        return spin_symbols, spin_symbols_obj
        