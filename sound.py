from random import randrange
import pygame

# Sound in Game init
# main_sound = pygame.mixer.Sound('audio/track.mp3')
# main_sound.play(loops = -1)

# Import sounds in Machine init
# self.spin_sound = pygame.mixer.Sound('audio/spinclip.mp3')
# self.spin_sound.set_volume(0.15)
# self.win_three = pygame.mixer.Sound('audio/winthree.wav')
# self.win_three.set_volume(0.6)
# self.win_four = pygame.mixer.Sound('audio/winfour.wav')
# self.win_four.set_volume(0.7)
# self.win_five = pygame.mixer.Sound('audio/winfive.wav')
# self.win_five.set_volume(0.8)

# After each start_spin call
# self.spin_sound.play()


class Sound:
    def __init__(self):
        # Load sounds
        self.main_sound = pygame.mixer.Sound('audio/track.mp3')
        self.main_sound.set_volume(0.5)
        self.line_sound = pygame.mixer.Sound('audio/line.mp3')
        self.sip_sounds = [
            pygame.mixer.Sound('audio/sip1.mp3'),
            pygame.mixer.Sound('audio/sip2.mp3'),
            pygame.mixer.Sound('audio/sip3.mp3')
        ]
        self.bonus_sound = pygame.mixer.Sound('audio/bonus.mp3')
        self.wheel_sound = pygame.mixer.Sound('audio/wheel.mp3')
        self.prize_sound = pygame.mixer.Sound('audio/prize.mp3')

    def start_main_sound(self):
        self.main_sound.play(loops = -1)
    
    def play_line_sound(self):
        self.line_sound.play()

    def play_sip_sound(self):
        self.sip_sounds[randrange(0, 3)].play()

    def play_bonus_sound(self):
        self.bonus_sound.play()
    
    def play_wheel_sound(self):
        self.wheel_sound.play()
    
    def stop_wheel_sound(self):
        self.wheel_sound.stop()
        self.prize_sound.play()


# # You need to provide sounds and load them in the Machine init function for this to work!
# def play_win_sound(self, win_data):
#     sum = 0
#     for item in win_data.values():
#         sum += len(item[1])
#     if sum == 3: self.win_three.play()
#     elif sum == 4: self.win_four.play()
#     elif sum > 4: self.win_five.play()

# Sounds in Reel init
# self.stop_sound = pygame.mixer.Sound('audio/stop.mp3')
# self.stop_sound.set_volume(0.5)

# Sound when reel stop
# self.stop_sound.play()