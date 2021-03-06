from colorama import Fore, Style
from time import sleep
import json
import items
import enemies
from gamefunctions import perform_action, victory, GAME_MAP
from inventory import INVENTORY, pickup_item, pick_key, looting_enemy
from combat import start_combat

# Map:
# ------------------------
# | 1   6   11   16   21 |
# |   |   |    |    |    |                                  N
# | 2   7   12   17   22 |                                W o E
# |---|   |    |    |----|                                  S
# | 3   8   13   18   23 |         ----
# |---|---|    |----|----|        | 26 | (Boss room reached by teleport, from Room 15)
# | 4   9   14   19   24 |         ----
# |   |   |    |    |    |
# | 5 | 10| 15 | 20 | 25 |
# -----------------------
# Important rooms: 3 (Miniboss), 5 (Miniboss), 7 (Miniboss), 13 (START), 15 (Key Item), 21 (Miniboss), 23 (Miniboss)
# Room 5 'ornate_tome'  Room 21 'cursed_tome' Room 7 'ancient_scroll' Room 23 'ancient_spellbook'
# Rooms 4, 12, 18, 25 'health_potion' Rooms 1, 10 'mana_potion'
# Room 15 'silver_key' Room 3 'sun_talisman'

# Load all the rooms data
with open('data/rooms.json', 'r') as file:
    rooms = json.load(file)


def trigger_room(player):
    """ This function determines the player location and executes code for that location accordingly. """
    while True:

        room = Room(rooms[player.location])
        room_script(player, room)

        # Update the game map
        if room.number['id'] % 5 == 0:
            num = 1
        else:
            num = 0
        GAME_MAP[(room.number['id'] % 5) - 1][(room.number['id'] // 5) - num] = str(room.number['id'])

        perform_action(player, room)
        if "Silver Key" in INVENTORY.backpack:
            room_twentysix_script(player)


class Room:
    def __init__(self, room_dict):
        self.number = room_dict['number']
        self.description = room_dict['description']
        self.cleared = room_dict['cleared']
        self.directions = room_dict['directions']
        self.enemy = room_dict['enemy']
        self.contents = room_dict['contents']

    def location_check(self):
        print(Fore.YELLOW + "You are in room " + str(self.number['id']))
        sleep(1)
        print(Fore.WHITE + self.description)
        sleep(1)
        if self.cleared:
            if self.enemy['name'] != "" and not self.enemy['alive']:
                print("You see a dead " + str(self.enemy['name']))
            if not self.contents['taken']:
                print(Fore.WHITE + "This room contains a " + str(self.contents['item_name']) + ".")
            sleep(1)

    def available_directions(self):
        print(self.directions['string'])
        sleep(1)

    def create_and_pickup_item(self, player, take_item="", key=False):
        # Pick-up item
        item = ''
        if not self.contents['taken']:
            item_data = self.contents['item_id'].split("/")
            if item_data[0] == 'potion' or take_item == 'potion':
                item = items.Potion(items.potion[item_data[1]])
            if item_data[0] == 'book' or take_item == 'book':
                item = items.Book(items.book[item_data[1]])
            if item_data[0] == 'talisman' or take_item == 'talisman':
                item = items.Talisman(items.talisman[item_data[1]])

            if not key:
                action = pickup_item(player, item)
                if action:
                    self.contents['taken'] = True  # Change current state
                    rooms[self.number['str_id']]['contents']['taken'] = True  # Change future state
            else:
                return item

    def create_and_combat_enemy(self, player):
        if self.enemy['name'] != "" and self.enemy['alive']:
            monster = enemies.Enemy(enemies.enemy[self.enemy['id']])
            monster.monster_appears(player)
            sleep(2)
            start_combat(player, monster)
            looting_enemy(monster)
            sleep(1)
            self.enemy['alive'] = False
            rooms[self.number['str_id']]['enemy']['alive'] = False


def room_script(player, room):
    if not room.cleared:
        # Entering room
        room.location_check()
        player.sanity = (5, False)  # Recovering sanity

        # Combat
        room.create_and_combat_enemy(player)

        # Pick-up item
        if room.number['id'] == 15:
            key = room.create_and_pickup_item(player, take_item="talisman", key=True)
            pick_key(player, key)
        else:
            room.create_and_pickup_item(player)

        # Room cleared
        room.cleared = True  # Change current state
        rooms[room.number['str_id']]['cleared'] = True  # Change for future instance of the room

    else:
        # Returning to room
        print(Fore.WHITE + "This room is the same as when you left it.")


def room_twentysix_script(player):
    print(Fore.YELLOW + """

                 Bands and rays of color utterly foreign to any spectrum of the universe
                 play and weave and interlace before you, and you become conscious of 
                 a frightful velocity of motion.

                          """)
    sleep(2)
    print(Fore.YELLOW + """
                        You find yourself floating in the endless abyss...

    """)
    print("                                             ...                                                           ")
    sleep(1.5)
    print("                                             ...                                                           ")
    sleep(1.5)
    print("                                             ...                                                           ")
    sleep(1.5)
    print(Fore.RED + Style.BRIGHT + """
 
                                AN UNSPEAKABLE PRESENCE APPROACHES
                                
     """ + Style.NORMAL)
    sleep(3)
    print(Fore.RED + """
          You are stricken with hopelessness. An unspeakable Servant of The Nameless Mist has appeared. 
                    It is a being of immense and terrifying power. It is unfathomably fast.\n""")
    print(Fore.YELLOW + "Your speed is a mere: " + str(player.speed) + Fore.WHITE)
    sleep(2)
    # Combat
    nyarlathotep = enemies.Enemy(enemies.enemy['nyarlathotep'])
    nyarlathotep.monster_appears(player)
    start_combat(player, nyarlathotep)
    sleep(1)
    print(Fore.GREEN + Style.BRIGHT + """

                            THE SERVANT OF THE NAMELESS ABYSS IS STRUCK DOWN

    """)
    sleep(2)
    victory(player)
    exit()
