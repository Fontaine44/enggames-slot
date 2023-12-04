from ..settings import *
from animation import Animation

class SipAnimation(Animation):
    def __init__():
        pass


    # Toogle win animation between win lines
    def win_animation(self):
        if self.win_animation_ongoing:
            self.current_animation_time += 1

            if self.current_animation_time > FPS:
                # Turn off animation current animation
                self.toggle_win_animation(False, self.win_data[self.current_animation])
                # Reset timer
                self.current_animation_time = 0

                # Switch to new animation (switch to sip/bonus or loop back to first line win)
                if self.current_animation == len(self.win_data)-1:
                    self.current_animation = 0  # Reset current animation
                    # Check for sip/bonus data
                    if self.sip_data:
                        self.win_animation_ongoing = False
                        self.sip_animation_ongoing = True
                        self.toggle_sip_animation(True, self.sip_data)
                    elif self.bonus_data:
                        self.win_animation_ongoing = False
                        self.bonus_animation_ongoing = True
                    else:
                        # Turn on next animation
                        self.toggle_win_animation(True, self.win_data[self.current_animation])
                        # Allow new spin
                        self.allow_spin()

                else:
                    # Increment current animation index
                    self.current_animation += 1
                    # Turn on next animation
                    self.toggle_win_animation(True, self.win_data[self.current_animation]) 