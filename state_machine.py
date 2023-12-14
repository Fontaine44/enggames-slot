from machine import Machine
from menu import Menu
from ticket import Ticket
from video import Video
from time import sleep

class StateMachine:
    def __init__(self, sound, buttons):
        self.sound = sound
        self.buttons = buttons
        self.current_state = 1
        self.menu = Menu(self, self.sound, self.buttons)
        self.ticket = Ticket(self, self.sound, self.buttons)
        self.video = Video(self, self.buttons)
        self.states = [self.menu, self.video, None, self.ticket]

        self.update = self.draw

        self.alpha = 0

    def next(self):
        # Increment state
        self.current_state += 1

        self.update = self.transition
        
        # Check for reset
        if self.current_state == len(self.states):
            self.current_state = 0

        if self.current_state == 2:
            self.states[2]= Machine(self, self.sound, self.buttons)
        
        self.states[self.current_state].pre_start()
        
        sleep(0.2)

    def draw(self, delta_time):
        return self.states[self.current_state].update(delta_time)

    def transition(self, delta_time):
        self.alpha += 3
        if self.alpha < 255:
            self.states[self.current_state-1].display_surface.set_alpha(255-self.alpha)   # Fade out
            self.states[self.current_state].display_surface.set_alpha(self.alpha)         # Fade in
        else:
            # Transition is over
            self.alpha = 0
            self.update = self.draw
            self.states[self.current_state].start()

        return self.draw(delta_time)

    def close(self):
        try:
            self.machine.buttons.ser.close()
        except:
            pass


# State 0: Leaderboard/Main Menu
# State 1: Video instructions + 1000$ gift
# State 2: Actual Slot Machine
# State 3: Cashout Ticket + Photo or sorry
# back to state 0