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
        self.set_symbols_state(True, self.win_data[self.current_win])        # Start first animation

        # Play the win sound
        self.machine.sound.line_sound.play()

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

    def play(self):
        if self.playing:
            self.current_animation_time += 1
            self.draw_line()

            if self.current_animation_time > FPS*1.2:
                # Turn off animation current animation
                self.set_symbols_state(False, self.win_data[self.current_win])
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
                        self.set_symbols_state(True, self.win_data[self.current_win])

                else:
                    # Increment current animation index
                    self.current_win += 1
                    # Turn on next animation
                    self.set_symbols_state(True, self.win_data[self.current_win]) 

    # Toggle state on symbols
    def set_symbols_state(self, state, win_data):
        if state:
            # Set line index
            self.line_ind = self.win_data[self.current_win][0]

        # Turn animation on symbols
        for reel, row in enumerate(win_data[2]):
            self.machine.spin_result_obj[reel][row].winning = state

    def draw_line(self):
        # Draw line
        self.machine.reels_surface.blit(self.machine.lines[self.line_ind], REELS_ZONE)

        # Redraw winning symbols on top of line
        for reel, row in enumerate(self.win_data[self.current_win][2]):
            symbol = self.machine.spin_result_obj[reel][row]
            self.machine.reels_surface.blit(symbol.image, symbol.rect)