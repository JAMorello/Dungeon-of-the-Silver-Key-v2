from random import randint
from colorama import Fore

# Base stats of the player at the beginning of the game. It´s boosted with talismans
base_stats = {
    'max_health': 100,
    'max_mana': 100,
    'max_sanity': 100,
    'max_speed': randint(45, 100),
    # Combat action lists of the player. As books are acquired, the players has more options
    'attacks': {"thrust": (25, 30),
                "slash": (10, 65),
                "heal": (25, 40)}

}

# Base core of the player at the beginning of the game
base_score = {
    'damage_done': 0,
    'damage_taken': 0,
    'amount_healed': 0,
    'sanity_lost': 0,
}


class Player:
    def __init__(self, username, location):
        self.username = username
        self.base_stats = base_stats

        self.health = base_stats['max_health']
        self.mana = base_stats['max_mana']
        self.sanity = base_stats['max_sanity']
        self.speed = base_stats['max_speed']
        self.attacks = base_stats['attacks']
        self.location = location

        # Following attributes are score components
        self.damage_done = base_score['damage_done']
        self.damage_taken = base_score['damage_taken']
        self.amount_healed = base_score['amount_healed']
        self.sanity_lost = base_score['sanity_lost']

    def gain_sanity(self):
        if self.sanity < 100:
            self.sanity += 5
            if self.sanity > base_stats['max_sanity']:
                self.sanity = base_stats['max_sanity']
            print(Fore.GREEN + "Somewhat your mind feels a little more stable than before...")

    def gain_health(self, amount, player):
        self.health += amount
        if self.health > base_stats['max_health']:
            self.health = base_stats['max_health']
        print(Fore.GREEN + f"Your gained {amount} points of health...")
        print(Fore.GREEN + f"You have {player.health} points of health.")

    def boost_stats(self, amount):
        # Boost max stats
        self.base_stats['max_health'] += amount
        self.base_stats['max_mana'] += amount
        self.base_stats['max_sanity'] += amount
        self.base_stats['max_speed'] += amount
        # Boost current stats
        self.health += amount
        self.mana += amount
        self.sanity += amount
        self.speed += amount
