from settings import *
from .animation import *

class WinAnimation(Animation):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine
        self.reset()
    
    def start(self, win_data):
        self.win_data = win_data
        self.playing = True
        self.set_symbols_state(self.win_data[self.current_win])        # Start first animation

        # Play the win sound
        self.machine.sound.play_line_sound()

        # Allow spin if no sip/bonus
        if not self.machine.sip_data and not self.machine.bonus_data:
            self.machine.allow_spin()
    
    def reset(self):
        self.current_animation_time = 0
        self.current_win = 0
        self.line_index = None
        self.win_data = None
    
    def stop(self):
        self.playing = False
        self.reset()
    
    def pause(self):
        self.playing = False
    
    def unpause(self):
        self.playing = True

    def play(self, delta_time):
        if self.playing:
            self.current_animation_time += delta_time
            self.draw_line()

            if self.current_animation_time > 1.2:
                # Turn off animation current animation
                self.set_symbols_state([])
                # Reset timer
                self.current_animation_time = 0

                # Switch to new animation (switch to sip/bonus or loop back to first line win)
                if self.current_win == len(self.win_data)-1:
                    self.current_win = 0  # Reset current animation index
                    # Check for sip/bonus data
                    if self.machine.sip_data:
                        self.stop()
                        self.machine.sip_animation.start(self.machine.sip_data)
                    elif self.machine.bonus_data:
                        self.stop()
                        self.machine.bonus_animation.start(self.machine.bonus_data)
                    else:
                        # Turn on next animation
                        self.set_symbols_state(self.win_data[self.current_win])

                else:
                    # Increment current animation index
                    self.current_win += 1
                    # Turn on next animation
                    self.set_symbols_state(self.win_data[self.current_win]) 

    # Toggle state on symbols
    def set_symbols_state(self, win_data):
        # Fade out all symbols
        for reel in self.machine.spin_result_obj:
            for symbol in reel:
                symbol.image.set_alpha(95)
        
        if win_data:
            # Set payline index
            self.line_ind = win_data[0]

            # Fade in winning symbols
            for reel, row in enumerate(win_data[2]):
                symbol = self.machine.spin_result_obj[reel][row]
                symbol.image.set_alpha(255)
        
    def draw_line(self):
        # Draw line
        self.machine.reels_surface.blit(self.machine.lines[self.line_ind], REELS_ZONE)

        # Redraw winning symbols on top of line
        for reel, row in enumerate(self.win_data[self.current_win][2]):
            symbol = self.machine.spin_result_obj[reel][row]
            self.machine.reels_surface.blit(symbol.image, symbol.rect)