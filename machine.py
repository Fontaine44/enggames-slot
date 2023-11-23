from player import Player
from reel import *
from settings import *
from ui import UI
from itertools import groupby
import pygame

class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.machine_balance = 10000.00
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.win_animation_ongoing = False
        self.bonus_animation_ongoing = False

        # Init empty results 2D array
        self.spin_result = [[] for _ in range(5)]
        self.spin_result_obj = [[] for _ in range(5)]

        # Index of the current win animation
        self.current_animation = 0

        self.spawn_reels()
        self.curr_player = Player()
        self.ui = UI(self.curr_player)

        # Import sounds
        # self.spin_sound = pygame.mixer.Sound('audio/spinclip.mp3')
        # self.spin_sound.set_volume(0.15)
        # self.win_three = pygame.mixer.Sound('audio/winthree.wav')
        # self.win_three.set_volume(0.6)
        # self.win_four = pygame.mixer.Sound('audio/winfour.wav')
        # self.win_four.set_volume(0.7)
        # self.win_five = pygame.mixer.Sound('audio/winfive.wav')
        # self.win_five.set_volume(0.8)

    def load_symbols(self):
        symbols_surfaces = {}
        for key, path in SYMBOLS_PATH.items():
            symbols_surfaces[key] = pygame.image.load(path).convert_alpha()
        return symbols_surfaces

    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning and animations are done
        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        # Wait for reel to finish spinning and check for win
        if not self.can_toggle and [self.reel_list[reel].reel_is_spinning for reel in self.reel_list].count(False) == 5:
            self.can_toggle = True
            self.set_result()       # Set spin_result and spin_result_obj

            self.win_data, self.bonus_data  = self.check_wins(self.spin_result)

            if self.win_data:
                # Reset animation parameters
                self.win_animation_ongoing = True
                self.current_animation = 0
                self.current_animation_time = 0
                self.toggle_win_animation(True, self.win_data[self.current_animation])        # Start first animation

                self.curr_player.last_payout = 0
                # Play the win sound
                # self.play_win_sound(self.win_data)
                self.pay_player()          # Pay the player for the wins
                self.ui.win_text_angle = random.randint(-4, 4)
            
            elif self.bonus_data:
                self.bonus_animation_ongoing = True

    def input(self):
        keys = pygame.key.get_pressed()

        # Checks for space key, ability to toggle spin, and balance to cover bet size
        if keys[pygame.K_SPACE] and self.can_toggle and self.curr_player.balance >= self.curr_player.bet_size:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()
            self.curr_player.place_bet()
            self.machine_balance += self.curr_player.bet_size
            self.curr_player.last_payout = None
            
    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):
        symbols_surfaces = self.load_symbols()
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 5:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft
            
            self.reel_list[self.reel_index] = Reel(symbols_surfaces, (x_topleft, y_topleft)) # Need to create reel class
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False

            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False
                self.bonus_animation_ongoing = False

    # Set spin_result with new results (2D arrays of symbol strings)
    def set_result(self):
        for reel in self.reel_list:
            self.spin_result[reel], self.spin_result_obj[reel] = self.reel_list[reel].reel_spin_result()

    # Check for winning lines or winning bonus and returns lists of wins
    def check_wins(self, result):         
        # Check for winning lines in the result
        winning_lines = self.check_lines(result)

        # Check for winning bonus in the result
        winning_bonus = self.check_bonus(result)

        return winning_lines, winning_bonus

    # Returns list of winning paylines
    def check_lines(self, result):
        # Initialize a list to store winning lines
        winning_lines = []

        # Iterate through the line patterns
        for ind, line in enumerate(PAYLINES):
            line_symbols = [result[reel][row] for reel, row in enumerate(line)]
            count = self.count_line(line_symbols)
            if count >= 3:
                symbol = line_symbols.pop(0)

                # Add winning line if not chug or sip
                if symbol not in ['bonus', 'sip']:
                    # Record the winning line
                    winning_line = [ind, symbol, line[:count]]
                    winning_lines.append(winning_line)

        return winning_lines
    
    # Check if grid contains 3 bonus symbols
    def check_bonus(self, result):
        bonus_count = 0
        sip_count = 0

        bonus_symbols = []
        sip_symbols = []

        # Check for bonus symbols
        for reel, reel_symbols in enumerate(result):
            for row, symbol in enumerate(reel_symbols):
                if symbol == 'bonus':
                    bonus_count += 1
                    bonus_symbols.append((reel, row))
                elif symbol == 'sip':
                    sip_count += 1
                    sip_symbols.append((reel, row))
        
        # Add winning bonus to the list
        winning_bonus = []
        if bonus_count >= 3:
            winning_bonus.append(['bonus', bonus_symbols])
        if sip_count >= 3:
            winning_bonus.append(['sip', sip_symbols])

        return winning_bonus

    # Count the number of identic symbols at the beginning of a payline
    def count_line(self, line):
        groups = groupby(line)
        _, group = next(groups)
        return len(list(group))

    # Pays the player for a single win (line)
    def pay_player(self):
        spin_payout = 0
        for win in self.win_data:
            win_symbol = win[1]
            symbol_mult = SYMBOLS_PAY[win_symbol]
            multiplier = (len(win[2]) - 2) * symbol_mult
            spin_payout += self.curr_player.bet_size * multiplier

        # Add the payout to the player's balance
        self.curr_player.balance += spin_payout
        self.machine_balance -= spin_payout
        self.curr_player.last_payout += spin_payout
        self.curr_player.total_won += spin_payout

    # You need to provide sounds and load them in the Machine init function for this to work!
    def play_win_sound(self, win_data):
        sum = 0
        for item in win_data.values():
            sum += len(item[1])
        if sum == 3: self.win_three.play()
        elif sum == 4: self.win_four.play()
        elif sum > 4: self.win_five.play()
        
    def toggle_win_animation(self, state, win):
        # TODO: display win lines here
        for reel, row in enumerate(win[2]):
            self.spin_result_obj[reel][row].winning = state
    
    def toggle_bonus_animation(self, state, bonus):
        for symbol in bonus[1]:
            reel = symbol[0]
            row = symbol[1]
            self.spin_result_obj[reel][row].bonus = state


    # Toogle win animation between win lines
    def win_animation(self):
        if self.win_animation_ongoing:
            self.current_animation_time += 1

            if self.current_animation_time > 60:
                # Turn off animation current animation
                self.toggle_win_animation(False, self.win_data[self.current_animation])
                # Reset timer
                self.current_animation_time = 0

                # Switch to new animation (switch to bonus or loop back to first line win)
                if self.current_animation == len(self.win_data)-1:
                    # Check for bonus data
                    if self.bonus_data:
                        self.win_animation_ongoing = False
                        self.bonus_animation_ongoing = True
                    else:
                        # Reset to first line win
                        self.current_animation = 0
                        # Turn on next animation
                        self.toggle_win_animation(True, self.win_data[self.current_animation])   
                else:
                    # Increment current animation index
                    self.current_animation += 1
                    # Turn on next animation
                    self.toggle_win_animation(True, self.win_data[self.current_animation]) 
            
    def draw_paylines(self):
        pass
    
    def bonus_animation(self):
        if self.bonus_animation_ongoing:
            print("Bonus")
            self.toggle_bonus_animation(True, self.bonus_data[0])
            
    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update(self.win_animation_ongoing, self.bonus_animation_ongoing)
        self.ui.update()
        self.win_animation()
        self.bonus_animation()

        # Balance/payout debugger
        # debug_player_data = self.curr_player.get_data()
        # machine_balance = "{:.2f}".format(self.machine_balance)
        # if self.curr_player.last_payout:
        #     last_payout = "{:.2f}".format(self.curr_player.last_payout)
        # else:
        #     last_payout = "N/A"
        # debug(f"Player balance: {debug_player_data['balance']} | Machine balance: {machine_balance} | Last payout: {last_payout}")