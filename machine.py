from player import Player
from reel import *
from settings import *
from ui import UI
from itertools import groupby
from buttons import ArcadeButton
from animations import *
import pygame

class Machine:
    def __init__(self, state_machine):
        self.state_machine = state_machine

        # Create surfaces
        self.display_surface = pygame.display.get_surface()
        self.reels_surface = pygame.Surface((REELS_ZONE[2], REELS_ZONE[3]))
        self.reels_rect = self.reels_surface.get_rect()
        self.bottom_ui_surface = pygame.Surface((BOTTOM_UI_ZONE[2], BOTTOM_UI_ZONE[3]))
        self.side_ui_surface = pygame.Surface((SIDE_UI_ZONE[2], SIDE_UI_ZONE[3]))

        # Load background
        self.bg = pygame.image.load(BG_IMAGE_PATH)
        self.bg = pygame.transform.smoothscale(self.bg, (WIDTH, HEIGHT))
        self.grid = pygame.image.load(GRID_IMAGE_PATH).convert_alpha()

        self.lines = self.load_images_list(LINES_PATH, alpha=True)

        self.machine_balance = 10000.00
        self.reel_list = {}
        self.can_spin = False
        self.spinning = False
        self.checked_win = True
        self.win_data = None
        self.sip_data = None
        self.bonus_data = None

        # Init empty results 2D array
        self.spin_result = [[] for _ in range(5)]
        self.spin_result_obj = [[] for _ in range(5)]

        self.win_animation = WinAnimation(self)
        self.sip_animation = SipAnimation(self)
        self.bonus_animation = BonusAnimation(self)

        self.spawn_reels()
        self.curr_player = Player()
        self.ui = UI(self.curr_player)
        self.buttons = ArcadeButton()

        self.allow_spin()



    # Load images (surfaces) into dictionary from dictionnary of paths
    def load_images_dict(self, paths, size=None, alpha=False):
        images_surfaces = {}
        for key, path in paths.items():
            image = pygame.image.load(path)

            if alpha:
                image = image.convert_alpha()
            if size:
                image = pygame.transform.smoothscale(image, size)

            images_surfaces[key] = image

        return images_surfaces
    
    # Load images (surfaces) into list from list of paths
    def load_images_list(self, paths, size=None, alpha=False):
        images_surfaces = []
        for path in paths:
            image = pygame.image.load(path)

            if alpha:
                image = image.convert_alpha()
            if size:
                image = pygame.transform.smoothscale(image, size)
            
            images_surfaces.append(image)

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
                self.win_animation.start(self.win_data)

                self.curr_player.last_payout = 0

                self.pay_player()          # Pay the player for the wins
                self.ui.win_text_angle = random.randint(-4, 4)
            
            elif self.sip_data:
                self.sip_animation.start(self.sip_data)

            elif self.bonus_data:
                self.bonus_animation.start(self.bonus_data)

            else:
                # No win, allow new spin
                self.allow_spin()

    # Returns true if the machine is spinning (last reel is still spinning)
    def is_spinning(self):
        return self.reel_list[4].is_spinning

    # Start spin if spacebar is pressed
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.state_machine.next()


        if self.can_spin and self.curr_player.balance >= self.curr_player.bet_size:
            if self.buttons.get_input() == 0:
                self.start_spinning()
                self.spin_time = pygame.time.get_ticks()
                self.curr_player.place_bet()
                self.machine_balance += self.curr_player.bet_size
                self.curr_player.last_payout = None

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

            self.reel_list[reel].symbol_list.update(self.win_animation, self.sip_animation, self.bonus_animation)

            self.reel_list[reel].symbol_list.draw(self.reels_surface)

            # for im in self.reel_list[reel].symbol_list:
            #     pygame.draw.rect(self.reels_surface, BLUE, im.rect, width=1)

    def spawn_reels(self):
        symbols_surfaces = self.load_images_dict(SYMBOLS_PATH, size=(SYMBOL_SIZE, SYMBOL_SIZE), alpha=True)              # Create dictionnary of surfaces
        x_topleft, y_topleft = X_OFFSET/2, -SYMBOL_SIZE    # Top left position of the reel
        # Spawn 5 reels
        for i in range(5):
            self.reel_list[i] = Reel(symbols_surfaces, x_topleft + i*SYMBOL_SIZE + i*X_OFFSET, y_topleft) # Need to create reel class

    def start_spinning(self):
        self.checked_win = False
        self.spin_time = pygame.time.get_ticks()
        self.spinning = True
        self.can_spin = False

        self.win_animation.stop()

        for reel in self.reel_list:
            self.reel_list[reel].start_spin(int(reel) * DELAY_TIME)
    
    def play_animations(self):
        self.win_animation.play()
        self.sip_animation.play()
        self.bonus_animation.play()

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

    # Check if grid contains 3 sip/bonus symbols
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


            
    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.display_surface.blit(self.bg, (0, 0))
        self.reels_surface.blit(self.grid, (0, 0))

        self.draw_reels(delta_time)

        self.play_animations()

        self.display_surface.blit(self.reels_surface, REELS_ZONE)




        # self.ui.update()

        return [self.display_surface.get_rect()]
        # return [self.reels_rect]

        # if self.bonus_animation.playing and self.bonus_animation.state > 0:
        #     return [self.bonus_animation.wheel_rect]
        # else:
        #     return  [self.reels_rect]



        # Balance/payout debugger
        # debug_player_data = self.curr_player.get_data()
        # machine_balance = "{:.2f}".format(self.machine_balance)
        # if self.curr_player.last_payout:
        #     last_payout = "{:.2f}".format(self.curr_player.last_payout)
        # else:
        #     last_payout = "N/A"
        # debug(f"Player balance: {debug_player_data['balance']} | Machine balance: {machine_balance} | Last payout: {last_payout}")