from colorama import Fore, Style
from time import sleep
import json
import items
import enemies
from gamefunctions import perform_action, victory
from inventory import INVENTORY, pickup_item, looting_enemy
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

with open('rooms.json', 'r') as file:
    rooms = json.load(file)


def trigger_room(player):
    """ Essential to game operation. This function determines the player location and executes code for that location
    accordingly. """
    while True:
        room = Room(rooms[player.location])
        room_script(player, room)
        perform_action(player, room)
        if "Silver Key" not in INVENTORY.backpack:
            room.available_directions()
            travel_to_room(player, room)
        else:
            room_twentysix_script(player)


def travel_to_room(player, room):
    """ Essential to game operation. This function changes the rooms: the players travels from one room to another. """
    while True:
        movement_choice = input(Fore.WHITE + "Choose a door: ").lower()
        if movement_choice in ['n', 's', 'e', 'w']:
            # detects if there's door in that direction using ROOMS_MAP
            if movement_choice not in room.directions['available']:
                print(Fore.YELLOW + "There is no door in that direction.")
                continue
            else:
                player.location = room.directions['available'][movement_choice]
                break
        else:
            print("Enter a valid option.")


class Room:
    def __init__(self, room_dict):
        self.number = room_dict['number']
        # self.script = room_dict['script']
        self.description = room_dict['description']
        self.cleared = room_dict['cleared']
        self.directions = room_dict['directions']
        self.enemy = room_dict['enemy']
        self.contents = room_dict['contents']

    def location_check(self):
        print(Fore.YELLOW + "You are in room " + str(self.number['id']))
        print(Fore.WHITE + self.description)
        if self.cleared:
            if self.enemy['name'] != "" and not self.enemy['alive']:
                print("You see a dead " + str(self.enemy['name']))
            if not self.contents['taken']:
                print(Fore.WHITE + "This room contains a " + str(self.contents['item_name']) + ".")

    def available_directions(self):
        print(self.directions['string'])

    def create_and_pickup_item(self, player):
        # Pick-up item
        item = ''
        if not self.contents['taken']:
            item_data = self.contents['item_id'].split("/")
            if item_data[0] == 'potion':
                item = items.Potion(items.potion[item_data[1]])
            if item_data[0] == 'book':
                item = items.Book(items.book[item_data[1]])
            if item_data[0] == 'talisman':
                item = items.Talisman(items.talisman[item_data[1]])

            action = pickup_item(player, item)
            if action:
                self.contents['taken'] = True  # Change current state
                rooms[self.number['str_id']]['contents']['taken'] = True  # Change future state

    def create_and_combat_enemy(self, player):
        if self.enemy['name'] != "" and self.enemy['alive']:
            monster = enemies.Enemy(enemies.enemy[self.enemy['id']])
            monster.monster_appears(player)
            start_combat(player, monster)
            looting_enemy(monster)
            self.enemy['alive'] = False
            rooms[self.number['str_id']]['enemy']['alive'] = False


def room_script(player, room):
    if not room.cleared:
        # Entering room
        room.location_check()
        player.gain_sanity()

        # Combat
        room.create_and_combat_enemy(player)

        # Pick-up item
        room.create_and_pickup_item(player)

        # Room cleared
        room.cleared = True  # Change current state
        rooms[room.number['str_id']]['cleared'] = True  # Change for future instance of the room

    else:
        # Returning to room
        print(Fore.WHITE + "This room is the same as when you left it.")
        room.create_and_pickup_item(player)


def room_twentysix_script(player):
    print(Fore.YELLOW + """

                 Bands and rays of color utterly foreign to any spectrum of the universe
                 play and weave and interlace before you, and you become conscious of 
                 a frightful velocity of motion.

                          """)
    sleep(1)
    print(Fore.YELLOW + """
                        You find yourself floating in the endless abyss...

    """)
    print("                                             ...                                                           ")
    sleep(1)
    print("                                             ...                                                           ")
    sleep(1)
    print("                                             ...                                                           ")
    sleep(1)
    print(Fore.RED + Style.BRIGHT + """
 
                                AN UNSPEAKABLE PRESENCE APPROACHES
                                
     """)
    sleep(1)
    print(Fore.RED + """
          You are stricken with hopelessness. An unspeakable Servant of The Nameless Mist has appeared. 
                    It is a being of immense and terrifying power. It is unfathomably fast.\n""")
    print(Fore.YELLOW + "Your speed is a mere: " + str(player.speed))

    # Combat
    nyarlathotep = enemies.Enemy(enemies.enemy['nyarlathotep'])
    nyarlathotep.monster_appears(player)
    start_combat(player, nyarlathotep)

    print(Fore.GREEN + Style.BRIGHT + """

                            THE SERVANT OF THE NAMELESS ABYSS IS STRUCK DOWN

    """)
    victory(player)
    exit()
