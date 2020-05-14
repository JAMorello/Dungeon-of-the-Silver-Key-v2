from random import randint
from colorama import Fore
from time import sleep
import json

# Load all the attacks data
with open('data/player_attacks.json', 'r') as file:
    attacks = json.load(file)


class Player:
    # Base stats of the player at the beginning of the game. It´s boosted with talismans
    max_stats = {
        'max_health': 100,
        'max_mana': 100,
        'max_sanity': 100,
        'max_speed': randint(45, 100)
    }

    # Combat action lists of the player. As books are acquired, the players has more options
    attacks = attacks

    # Base score of the player at the beginning of the game
    score = {
        'damage_done': 0,
        'damage_taken': 0,
        'amount_healed': 0,
        'sanity_lost': 0,
    }

    def __init__(self, username, location):
        self.username = username
        self.__health = self.max_stats['max_health']
        self.__mana = self.max_stats['max_mana']
        self.__sanity = self.max_stats['max_sanity']
        self.speed = self.max_stats['max_speed']
        self.location = location

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, val):
        if val != 0:
            self.__health += val
            if self.__health > self.max_stats['max_health']:
                self.__health = self.max_stats['max_health']
            if val > 0:
                print(Fore.GREEN + f"Your gained {val} points of health...")
                print(Fore.GREEN + f"You have {self.__health} points of health." + Fore.WHITE)

    @property
    def mana(self):
        return self.__mana

    @mana.setter
    def mana(self, val):
        if val != 0:
            self.__mana += val
            if self.__mana < 0:
                self.__mana = 0
            if self.__mana > self.max_stats['max_mana']:
                self.__mana = self.max_stats['max_mana']
            if val > 0:
                print(Fore.GREEN + f"Your gained {val} points of mana...")
            print(Fore.BLUE + "You have " + str(self.__mana) + " mana remaining." + Fore.WHITE)

    @property
    def sanity(self):
        return self.__sanity

    @sanity.setter
    def sanity(self, tup):
        # TODO: Work on sanity that triggers on entering room (initial and exploit)
        (val, spell) = tup  # Tuple contains a numeric value and a boolean
        self.__sanity += val
        if self.__sanity > self.max_stats['max_sanity']:
            self.__sanity = self.max_stats['max_sanity']
        if not spell:
            print(Fore.GREEN + "Somewhat your mind feels a little more stable than before..." + Fore.WHITE)
        if spell:
            print(Fore.GREEN + "Your sanity is " + str(self.__sanity) + Fore.WHITE)
        sleep(1)

    def boost_stats(self, amount):
        # Boost max stats
        for stat in self.max_stats:
            stat += amount
        # Boost current stats
        # TODO: work on boost: TypeError: can only concatenate str (not "int") to str
        self.__health += amount
        self.__mana += amount
        self.__sanity += amount
        self.speed += amount

    def change_score(self, points=0, damage_done=False, damage_taken=False, amount_healed=False, sanity_lost=False):
        if damage_done:
            self.score['damage_done'] += points
        if damage_taken:
            self.score['damage_taken'] += points
        if amount_healed:
            self.score['amount_healed'] += points
        if sanity_lost:
            self.score['sanity_lost'] += points
