import json
from random import randint

# Load all the enemies data
with open('data/enemies.json', 'r') as file:
    enemy = json.load(file)


class Enemy:
    def __init__(self, enemy_dict):
        self.name = enemy_dict['name']
        self.adjective = enemy_dict['adjective']
        self.description = enemy_dict['description']
        self.signature_move = enemy_dict['signature move']
        self.sanity_move = enemy_dict['sanity move']
        self.special_move = enemy_dict['special move']
        self.speed = randint(*enemy_dict['speed'])
        self.__health = enemy_dict['health']
        self.drop_chance = enemy_dict['drop chance']
        self.attacks = enemy_dict['attacks']

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, val):
        self.__health += val

    def monster_appears(self, player):  # This method is used to announce the start of a non-boss fight
        print(self.adjective + self.name + " appears before you.\n" + self.description)
        print("It's speed is " + str(self.speed) + " and your speed is " + str(player.speed) + ".")
