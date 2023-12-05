# from settings import FPS, NUMBERS_PATH, SYMBOL_SIZE, NUMBERS_WEIGHT
from .animation import *
# import pygame
# import random

class BonusAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.reset()
    
    def start(self, bonus_data):
        self.bonus_data = bonus_data
        self.playing = True
    
    def reset(self):
        self.bonus_data = None
    
    def stop(self):
        self.playing = False
        self.reset()

    def play(self):
        if self.playing:
            pass