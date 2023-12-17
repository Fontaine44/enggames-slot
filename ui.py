from settings import *
import pygame
import pygame.freetype
import random

class UI:
    def __init__(self, player, bottom_ui_surface, side_ui_surface):
        self.player = player
        self.bottom_ui_surface = bottom_ui_surface
        self.side_ui_surface = side_ui_surface
        self.bottom_ui_image = pygame.image.load(BOTTOM_UI_IMAGE_PATH).convert_alpha()
        
        self.font = pygame.freetype.Font(FONT_PATH, 60)
        self.refreshed = False      # refresh is True if we need to refresh the background in this tick

    def refresh(self):
        if not self.refreshed:
            self.bottom_ui_surface.blit(self.bottom_ui_image, (0, 0))
            self.refreshed = True
    
    def display_big_message(self, message, size, color):
        self.refresh()

        text_angle = random.randint(-4, 4)
        self.balance_surface, _ = self.font.render(message, size=size, fgcolor=color, rotation=text_angle)
        self.bottom_ui_surface.blit(self.balance_surface, (600, 30))
    
    def display_balance(self):
        self.refresh()

        self.balance_surface, _ = self.font.render(f"{self.player.balance} $", WHITE)
        self.bottom_ui_surface.blit(self.balance_surface, (300, 30))

        self.bet_size_surface, _ = self.font.render(f"{self.player.bet_size} $", WHITE)
        self.bottom_ui_surface.blit(self.bet_size_surface, (300, 107))
