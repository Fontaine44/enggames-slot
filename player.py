from settings import *
import random
import string
import secrets

class Player():
    def __init__(self):
        self.id = self.generate_short_id()
        self.balance = 1000
        self.bet_size = 100
        self.last_payout = 0
        self.total_won = 0
        self.total_wager = 0
        self.free_spins = 0
        self.jackpot = random.randrange(5000, 10000)
        self.sips = 0
        self.chugs = 0

    def get_data(self):
        player_data = {}
        player_data['balance'] = "{:.2f}".format(self.balance)
        player_data['bet_size'] = "{:.2f}".format(self.bet_size)
        player_data['last_payout'] = "{:.2f}".format(self.last_payout) if self.last_payout else "N/A"
        player_data['total_won'] = "{:.2f}".format(self.total_won)
        player_data['total_wager'] = "{:.2f}".format(self.total_wager)
        return player_data

    def place_bet(self):
        if self.free_spins > 0:
            self.free_spins -= 1
        else:
            self.bet_size = 100

            if self.balance < 100:
                self.bet_size = self.balance

            self.balance -= self.bet_size
            self.total_wager += self.bet_size

        self.jackpot += 50

    def get_balance(self):
        return self.balance

    def double_money(self):
        self.balance = self.balance * 2
    
    def activate_free_spins(self):
        self.free_spins += 10
    
    def get_jackpot(self):
        self.balance += self.jackpot
        self.jackpot = random.randrange(5000, 10000)

    def bankrupt(self):
        self.balance = 0
    
    def generate_short_id(self, length=6):
        characters = string.ascii_letters + string.digits
        short_id = ''.join(secrets.choice(characters) for _ in range(length))
        return short_id