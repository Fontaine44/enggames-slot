from machine import Machine
from menu import Menu
from ticket import Ticket
from video import Video
from time import sleep

class StateMachine:
    def __init__(self):
        self.num_states = 4
        self.current_ind = 0
        self.machine = Machine(self)
        self.menu = Menu(self)
        self.ticket = Ticket(self)
        self.video = Video(self)

        self.current_state = self.machine

    def next(self):
        # Increment state
        self.current_ind += 1
        
        # Check for reset
        if self.current_ind == self.num_states:
            self.current_ind = 0

        if self.current_ind == 0:
            self.current_state = self.menu
        elif self.current_ind == 1:
            self.current_state = self.video
        elif self.current_ind == 2:
            self.machine = Machine(self)
            self.current_state = self.machine
        elif self.current_ind == 3:
            self.current_state = self.ticket
        
        sleep(0.2)

    def update(self, delta_time):
        return self.current_state.update(delta_time)

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