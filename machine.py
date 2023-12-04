from player import Player
from reel import *
from settings import *
from ui import UI
from itertools import groupby
from input import ArcadeButton
import pygame

class Machine:
    def __init__(self):
        # Create surfaces
        self.display_surface = pygame.display.get_surface()
        self.reels_surface = pygame.Surface((REELS_ZONE[2], REELS_ZONE[3]))
        self.bottom_ui_surface = pygame.Surface((BOTTOM_UI_ZONE[2], BOTTOM_UI_ZONE[3]))
        self.side_ui_surface = pygame.Surface((SIDE_UI_ZONE[2], SIDE_UI_ZONE[3]))

        self.machine_balance = 10000.00
        self.reel_list = {}
        self.can_spin = False
        self.spinning = False
        self.checked_win = True
        self.win_data = None
        self.sip_data = None
        self.bonus_data = None
        self.win_animation_ongoing = False
        self.sip_animation_ongoing = False
        self.bonus_animation_ongoing = False

        # Init empty results 2D array
        self.spin_result = [[] for _ in range(5)]
        self.spin_result_obj = [[] for _ in range(5)]

        # Index of the current win animation or state of sip/bonus animation
        self.current_animation = 0

        # Images for sip animation
        self.numbers_images = self.load_images(NUMBERS_PATH, SYMBOL_SIZE)
        self.numbers_keys = list(NUMBERS_PATH.keys())
        self.numbers_weights = [NUMBERS_WEIGHT[k] for k in self.numbers_keys]
        self.sip_number = None
        self.sip_scale_factor = 1.0

        self.spawn_reels()
        self.curr_player = Player()
        self.ui = UI(self.curr_player)
        self.buttons = ArcadeButton()

        self.allow_spin()

        # Import sounds
        # self.spin_sound = pygame.mixer.Sound('audio/spinclip.mp3')
        # self.spin_sound.set_volume(0.15)
        # self.win_three = pygame.mixer.Sound('audio/winthree.wav')
        # self.win_three.set_volume(0.6)
        # self.win_four = pygame.mixer.Sound('audio/winfour.wav')
        # self.win_four.set_volume(0.7)
        # self.win_five = pygame.mixer.Sound('audio/winfive.wav')
        # self.win_five.set_volume(0.8)

    # Load images (surfaces) into dictionary from dictionnary of paths
    def load_images(self, paths, size):
        images_surfaces = {}
        for key, path in paths.items():
            image = pygame.image.load(path).convert_alpha()
            images_surfaces[key] = pygame.transform.scale(image, (size, size))
        return images_surfaces

    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning and animations are done
        self.spinning = self.is_spinning()

        # Wait for reel to finish spinning and check for win
        if not self.checked_win and not self.spinning:
            self.checked_win = True
            self.set_result()       # Set spin_result and spin_result_obj

            self.win_data, self.sip_data, self.bonus_data  = self.check_wins()

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
            
            elif self.sip_data:
                # Reset animation parameters and start animation
                self.sip_animation_ongoing = True
                self.current_animation = 0
                self.current_animation_time = 0
                self.toggle_sip_animation(True, self.sip_data)        # Start sip animation

            elif self.bonus_data:
                self.bonus_animation_ongoing = True
                self.current_animation = 0
                self.current_animation_time = 0

            else:
                # No win, allow new spin
                self.allow_spin()

    # Returns true if the machine is spinning (last reel is still spinning)
    def is_spinning(self):
        return self.reel_list[4].is_spinning

    # Start spin if spacebar is pressed
    def input(self):
        if self.can_spin and self.curr_player.balance >= self.curr_player.bet_size:
            if self.buttons.get_input() == 0:
                self.start_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.curr_player.place_bet()
                self.machine_balance += self.curr_player.bet_size
                self.curr_player.last_payout = None

            keys = pygame.key.get_pressed()

            # Checks for space key, ability to toggle spin, and balance to cover bet size
            if keys[pygame.K_SPACE]:
                self.start_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.curr_player.place_bet()
                self.machine_balance += self.curr_player.bet_size
                self.curr_player.last_payout = None
            
    def draw_reels(self, delta_time):
        for reel in self.reel_list:

            self.reel_list[reel].animate(delta_time)    # Move symbols

            self.reel_list[reel].symbol_list.update(self.win_animation_ongoing, self.sip_animation_ongoing, self.bonus_animation_ongoing, self.current_animation)

            self.reel_list[reel].symbol_list.draw(self.reels_surface)

            # for im in self.reel_list[reel].symbol_list:
            #     pygame.draw.rect(self.reels_surface, BLUE, im.rect, width=1)

    def spawn_reels(self):
        symbols_surfaces = self.load_images(SYMBOLS_PATH, SYMBOL_SIZE)              # Create dictionnary of surfaces
        x_topleft, y_topleft = 0, -SYMBOL_SIZE    # Top left position of the reel
        # Spawn 5 reels
        for i in range(5):
            self.reel_list[i] = Reel(symbols_surfaces, x_topleft + i*SYMBOL_SIZE, y_topleft) # Need to create reel class

    def start_spinning(self):
        self.checked_win = False
        self.spin_time = pygame.time.get_ticks()
        self.spinning = True
        self.can_spin = False

        for reel in self.reel_list:
            self.reel_list[reel].start_spin(int(reel) * 200)
            # self.spin_sound.play()
            self.win_animation_ongoing = False
            self.sip_animation_ongoing = False
            self.bonus_animation_ongoing = False
        
    def allow_spin(self):
        self.can_spin = True
        self.buttons.clear_buffer()

    # Set spin_result with new results (2D arrays of symbol strings)
    def set_result(self):
        for reel in self.reel_list:
            self.spin_result[reel], self.spin_result_obj[reel] = self.reel_list[reel].reel_spin_result()

    # Check for winning lines or sip or bonus and returns lists of wins
    def check_wins(self):         
        # Check for winning lines in the result
        winning_lines = self.check_lines(self.spin_result)

        # Check for winning sip/bonus in the result
        winning_sip, winning_bonus = self.check_sip_bonus(self.spin_result)

        return winning_lines, winning_sip, winning_bonus

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

    # Check if grid contains 3 sip symbols
    def check_sip_bonus(self, result):
        bonus_symbols = []
        sip_symbols = []

        # Check for bonus symbols
        for reel, reel_symbols in enumerate(result):
            for row, symbol in enumerate(reel_symbols):
                if symbol == 'bonus':
                    bonus_symbols.append((reel, row))
                elif symbol == 'sip':
                    sip_symbols.append((reel, row))

        winning_sip = sip_symbols if len(sip_symbols) > 2 else None
        winning_bonus = bonus_symbols if len(bonus_symbols) > 2 else None
        return winning_sip, winning_bonus

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
        
    def toggle_win_animation(self, state, win_data):
        # TODO: display win lines here
        for reel, row in enumerate(win_data[2]):
            self.spin_result_obj[reel][row].winning = state
    
    def toggle_sip_animation(self, state, sip_data):
        # Turn on/off sip animation on winning symbols
        for sym_pos in sip_data:
            symbol = self.spin_result_obj[sym_pos[0]][sym_pos[1]]
            symbol.sip = state

    def toggle_bonus_animation(self, state, bonus_data):
        # Turn on/off bonus animation on winning symbols
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
            
    def draw_paylines(self):
        pass
    
    def sip_animation(self):
        if self.sip_animation_ongoing:
            self.current_animation_time += 1

            # State 0 (highlight)
            if self.current_animation == 0:
                # Go to state 1
                if self.current_animation_time > FPS*2:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.current_animation += 1
            
            # State 1 (zoom out)
            elif self.current_animation == 1:
                # Go to state 2
                if self.current_animation_time > FPS:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.current_animation += 1
                    self.sip_scale_factor = 1.0

                    # Rescale images
                    for sym_pos in self.sip_data:
                        symbol = self.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.scale_image(1.0)

                else:
                    # Zoom out
                    self.sip_scale_factor = pygame.math.lerp(self.sip_scale_factor, 0, 0.10)
                    for sym_pos in self.sip_data:
                        symbol = self.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.scale_image(self.sip_scale_factor)
            
            # State 2 (random numbers)
            if self.current_animation == 2:
                if self.current_animation_time > FPS*3:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.current_animation += 1

                elif self.current_animation_time % 10 == 0:
                    # Get a random number image
                    rand_key = random.choices(self.numbers_keys, weights=self.numbers_weights, k=1)[0]
                    self.sip_number = int(rand_key)

                    for sym_pos in self.sip_data:
                        symbol = self.spin_result_obj[sym_pos[0]][sym_pos[1]]
                        symbol.image = self.numbers_images[rand_key]
                    

            # State 3 (wait for the user to take the sips)
            elif self.current_animation == 3:
                if self.current_animation_time > FPS*self.sip_number*2:
                    # Go to next animation
                    self.current_animation_time = 0
                    self.current_animation += 1

            # State 4 (allow new spin)
            elif self.current_animation == 4:
                self.toggle_sip_animation(False, self.sip_data)
                self.sip_animation_ongoing = False
                # TODO: Check for binus animation here
                self.allow_spin()
    
    def bonus_animation(self):
        pass
            
    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.reels_surface.fill(BLACK)
        self.draw_reels(delta_time)
        self.display_surface.blit(self.reels_surface, REELS_ZONE[:2])
        # self.ui.update()
        self.win_animation()
        self.sip_animation()
        self.bonus_animation()

        # Balance/payout debugger
        # debug_player_data = self.curr_player.get_data()
        # machine_balance = "{:.2f}".format(self.machine_balance)
        # if self.curr_player.last_payout:
        #     last_payout = "{:.2f}".format(self.curr_player.last_payout)
        # else:
        #     last_payout = "N/A"
        # debug(f"Player balance: {debug_player_data['balance']} | Machine balance: {machine_balance} | Last payout: {last_payout}")