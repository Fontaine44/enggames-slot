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

# Play the win sound in cooldowns win
# self.play_win_sound(self.win_data)

# After each start_spin call
# self.spin_sound.play()

# You need to provide sounds and load them in the Machine init function for this to work!
def play_win_sound(self, win_data):
    sum = 0
    for item in win_data.values():
        sum += len(item[1])
    if sum == 3: self.win_three.play()
    elif sum == 4: self.win_four.play()
    elif sum > 4: self.win_five.play()
