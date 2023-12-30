from random import randrange
import pygame

class Sound:
    def __init__(self):
        # Load sounds
        # self.main_sound = pygame.mixer.Sound('audio/track.mp3')
        # self.main_sound.set_volume(0.3)
        self.line_sound = pygame.mixer.Sound('audio/line.mp3')
        self.sip_sounds = [
            pygame.mixer.Sound('audio/sip1.mp3'),
            pygame.mixer.Sound('audio/sip2.mp3'),
            pygame.mixer.Sound('audio/sip3.mp3')
        ]
        self.bonus_sound = pygame.mixer.Sound('audio/bonus.mp3')
        self.wheel_sound = pygame.mixer.Sound('audio/wheel.mp3')
        self.prize_sound = pygame.mixer.Sound('audio/prize.mp3')
        self.chug_sound = pygame.mixer.Sound('audio/chug.mp3')
        self.bankrupt_sound = pygame.mixer.Sound('audio/bankrupt.mp3')
        self.jackpot_sound = pygame.mixer.Sound('audio/jackpot.mp3')
        self.camera_sound = pygame.mixer.Sound('audio/camera.mp3')

    def start_main_sound(self):
        return
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

    def play_chug_sound(self):
        self.chug_sound.play()
        self.wheel_prize = self.chug_sound

    def play_bankrupt_sound(self):
        self.bankrupt_sound.play()
        self.wheel_prize = self.bankrupt_sound
    
    def play_prize_sound(self):
        self.prize_sound.play()
        self.wheel_prize = self.prize_sound
    
    def play_jackpot_sound(self):
        self.jackpot_sound.play()
        self.wheel_prize = self.jackpot_sound
    
    def stop_wheel_prize(self):
        self.wheel_prize.stop()
        self.wheel_prize = None
    
    def play_camera_sound(self):
        self.camera_sound.play()

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