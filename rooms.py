from colorama import Fore, Style, Back
from time import sleep
import gamefunctions
import items
import enemies
import inventory
from inventory import INVENTORY, looting_enemy
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

# The ROOMS_MAP dictionary shows all possible doors in the dungeon and prevents players from walking through the walls
# into nonexistent rooms.
ROOMS_MAP = {
    1: {'s': 'room_two', 'e': 'room_six'},
    2: {'n': 'room_one', 'e': 'room_seven'},
    3: {'e': 'room_eight'},
    4: {'s': 'room_five', 'e': 'room_nine'},
    5: {'n': 'room_four'},
    6: {'s': 'room_seven', 'e': 'room_eleven', 'w': 'room_one'},
    7: {'n': 'room_six', 's': 'room_eight', 'e': 'room_twelve', 'w': 'room_two'},
    8: {'n': 'room_seven', 'e': 'room_thirteen', 'w': 'room_three'},
    9: {'s': 'room_ten', 'e': 'room_fourteen', 'w': 'room_four'},
    10: {'n': 'room_nine'},
    11: {'s': 'room_twelve', 'w': 'room_six', 'e': 'room_sixteen'},
    12: {'n': 'room_eleven', 's': 'room_thirteen', 'e': 'room_seventeen', 'w': 'room_seven'},
    13: {'n': 'room_twelve', 's': 'room_fourteen', 'e': 'room_eighteen', 'w': 'room_eight'},
    14: {'n': 'room_thirteen', 's': 'room_fifteen', 'e': 'room_nineteen', 'w': 'room_nine'},
    15: {'n': 'room_fourteen'},
    16: {'s': 'room_seventeen', 'e': 'room_twentyone', 'w': 'room_eleven'},
    17: {'n': 'room_sixteen', 's': 'room_eighteen', 'e': 'room_twentytwo', 'w': 'room_twelve'},
    18: {'n': 'room_seventeen', 'e': 'room_twentythree', 'w': 'room_thirteen'},
    19: {'s': 'room_twenty', 'e': 'room_twentyfour', 'w': 'room_fourteen'},
    20: {'n': 'room_nineteen'},
    21: {'s': 'room_twentytwo', 'w': 'room_sixteen'},
    22: {'n': 'room_twentyone', 'w': 'room_seventeen'},
    23: {'w': 'room_eighteen'},
    24: {'s': 'room_twentyfive', 'w': 'room_nineteen'},
    25: {'n': 'room_twentyfour'}
}


def trigger_room(player):
    """ Essential to game operation. This function determines the player location and executes code for that location
    accordingly. """
    while True:
        room = Room(rooms[player.location])
        room_script(player, room)
        gamefunctions.perform_action(player, room)
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
            if movement_choice not in ROOMS_MAP[room.number['id']]:
                print(Fore.YELLOW + "There is no door in that direction.")
                continue
            else:
                player.location = ROOMS_MAP[room.number['id']][movement_choice]
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
        print(self.directions)

    def create_and_pickup_item(self, player):
        # Pick-up item
        if not self.contents['taken']:
            item_data = self.contents['item_id'].split("/")
            if item_data[0] == 'potion':
                item = items.Potion(items.potion[item_data[1]])
            if item_data[0] == 'book':
                item = items.Book(items.book[item_data[1]])
            if item_data[0] == 'talisman':
                item = items.Talisman(items.talisman[item_data[1]])

            action = inventory.pickup_item(player, item)
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
        room.cleared = True
        rooms[room.number['str_id']]['cleared'] = True

    else:
        # Returning to room
        print(Fore.WHITE + "This room is the same as when you left it.")
        room.create_and_pickup_item(player)


# def room_one_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Pick-up item
#         mana_potion = items.Potion(items.mana_potion)
#         action = inventory.pickup_item(player, mana_potion)
#         if action:
#             room.contents = ""
#             rooms['room_one']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_one']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_one']['contents'] != "":
#             # Pick-up item
#             mana_potion = items.Potion(items.mana_potion)
#             action = inventory.pickup_item(player, mana_potion)
#             if action:
#                 room.contents = ""
#                 rooms['room_one']['contents'] = ""
#
#
# def room_two_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         golem = enemies.Enemy(enemies.clay_golem)
#         golem.monster_appears(player)
#         start_combat(player, golem)
#         looting_enemy(golem)
#         room.enemy['alive'] = False
#         rooms['room_one']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_two']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_three_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         hunting_horror = enemies.Enemy(enemies.hunting_horror)
#         hunting_horror.monster_appears(player)
#         start_combat(player, hunting_horror)
#         looting_enemy(hunting_horror)
#         room.enemy['alive'] = False
#         rooms['room_three']['enemy']['alive'] = False
#
#         # Pick-up item
#         sun_talisman = items.Talisman(items.sun_talisman)
#         action = inventory.pickup_item(player, sun_talisman)
#         if action:
#             room.contents = ""
#             rooms['room_three']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_three']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_three']['contents'] != "":
#             # Pick-up item
#             sun_talisman = items.Talisman(items.sun_talisman)
#             action = inventory.pickup_item(player, sun_talisman)
#             if action:
#                 room.contents = ""
#                 rooms['room_three']['contents'] = ""
#
#
# def room_four_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Pick-up item
#         health_potion = items.Potion(items.health_potion)
#         action = inventory.pickup_item(player, health_potion)
#         if action:
#             room.contents = ""
#             rooms['room_four']['contents'] = ""
#         # Room cleared
#         room.cleared = True
#         rooms['room_four']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_four']['contents'] != "":
#             # Pick-up item
#             health_potion = items.Potion(items.health_potion)
#             action = inventory.pickup_item(player, health_potion)
#             if action:
#                 room.contents = ""
#                 rooms['room_four']['contents'] = ""
#
#
# def room_five_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         moon_beast = enemies.Enemy(enemies.moon_beast)
#         moon_beast.monster_appears(player)
#         start_combat(player, moon_beast)
#         looting_enemy(moon_beast)
#         room.enemy['alive'] = False
#         rooms['room_five']['enemy']['alive'] = False
#
#         # Pick-up item
#         ornate_tome = items.Book(items.ornate_tome)
#         action = inventory.pickup_item(player, ornate_tome)
#         if action:
#             room.contents = ""
#             rooms['room_five']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_five']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_five']['contents'] != "":
#             # Pick-up item
#             ornate_tome = items.Book(items.ornate_tome)
#             action = inventory.pickup_item(player, ornate_tome)
#             if action:
#                 room.contents = ""
#                 rooms['room_five']['contents'] = ""
#
#
# def room_six_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_six']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_seven_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         shoggoth = enemies.Enemy(enemies.shoggoth)
#         shoggoth.monster_appears(player)
#         start_combat(player, shoggoth)
#         looting_enemy(shoggoth)
#         room.enemy['alive'] = False
#         rooms['room_seven']['enemy']['alive'] = False
#
#         # Pick-up item
#         ancient_scroll = items.Book(items.ancient_scroll)
#         action = inventory.pickup_item(player, ancient_scroll)
#         if action:
#             room.contents = ""
#             rooms['room_seven']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_seven']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_seven']['contents'] != "":
#             # Pick-up item
#             ancient_scroll = items.Book(items.ancient_scroll)
#             action = inventory.pickup_item(player, ancient_scroll)
#             if action:
#                 room.contents = ""
#                 rooms['room_seven']['contents'] = ""
#
#
# def room_eight_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         lesser_spawn = enemies.Enemy(enemies.lesser_spawn)
#         lesser_spawn.monster_appears(player)
#         start_combat(player, lesser_spawn)
#         looting_enemy(lesser_spawn)
#         room.enemy['alive'] = False
#         rooms['room_eight']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_eight']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_nine_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_nine']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_ten_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Pick-up item
#         mana_potion = items.Potion(items.mana_potion)
#         action = inventory.pickup_item(player, mana_potion)
#         if action:
#             room.contents = ""
#             rooms['room_ten']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_ten']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_ten']['contents'] != "":
#             # Pick-up item
#             mana_potion = items.Potion(items.mana_potion)
#             action = inventory.pickup_item(player, mana_potion)
#             if action:
#                 room.contents = ""
#                 rooms['room_ten']['contents'] = ""
#
#
# def room_eleven_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         golem = enemies.Enemy(enemies.clay_golem)
#         golem.monster_appears(player)
#         start_combat(player, golem)
#         looting_enemy(golem)
#         room.enemy['alive'] = False
#         rooms['room_eleven']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_eleven']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_twelve_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Pick-up item
#         health_potion = items.Potion(items.health_potion)
#         action = inventory.pickup_item(player, health_potion)
#         if action:
#             room.contents = ""
#             rooms['room_twelve']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twelve']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_twelve']['contents'] != "":
#             # Pick-up item
#             health_potion = items.Potion(items.health_potion)
#             action = inventory.pickup_item(player, health_potion)
#             if action:
#                 room.contents = ""
#                 rooms['room_twelve']['contents'] = ""
#
#
# def room_thirteen_script(player, room):
#     # Starting room
#     room.location_check()
#
#     if not room.cleared:
#         if player.sanity < 100:
#             player.gain_sanity()
#             rooms['room_thirteen']['cleared'] = True
#
#
# def room_fourteen_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         golem = enemies.Enemy(enemies.clay_golem)
#         golem.monster_appears(player)
#         start_combat(player, golem)
#         looting_enemy(golem)
#         room.enemy['alive'] = False
#         rooms['room_fourteen']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_fourteen']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_fifteen_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Pick-up key
#         silver_key = items.Talisman(items.silver_key)
#         action = inventory.pick_key(player, silver_key)
#         if action:
#             room.contents = ""
#             rooms['room_fifteen']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_fifteen']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_fifteen']['contents'] != "":
#             # Pick-up item
#             silver_key = items.Talisman(items.silver_key)
#             action = inventory.pick_key(player, silver_key)
#             if action:
#                 room.contents = ""
#                 rooms['room_fifteen']['contents'] = ""
#
#
# def room_sixteen_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_sixteen']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_seventeen_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         lesser_spawn = enemies.Enemy(enemies.lesser_spawn)
#         lesser_spawn.monster_appears(player)
#         start_combat(player, lesser_spawn)
#         looting_enemy(lesser_spawn)
#         room.enemy['alive'] = False
#         rooms['room_seventeen']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_seventeen']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_eighteen_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         golem = enemies.Enemy(enemies.clay_golem)
#         golem.monster_appears(player)
#         start_combat(player, golem)
#         looting_enemy(golem)
#         room.enemy['alive'] = False
#         rooms['room_eighteen']['enemy']['alive'] = False
#
#         # Pick-up item
#         health_potion = items.Potion(items.health_potion)
#         action = inventory.pickup_item(player, health_potion)
#         if action:
#             room.contents = ""
#             rooms['room_eighteen']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_eighteen']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_eighteen']['contents'] != "":
#             # Pick-up item
#             health_potion = items.Potion(items.health_potion)
#             action = inventory.pickup_item(player, health_potion)
#             if action:
#                 room.contents = ""
#                 rooms['room_eighteen']['contents'] = ""
#
#
# def room_nineteen_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_nineteen']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_twenty_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         lesser_spawn = enemies.Enemy(enemies.lesser_spawn)
#         lesser_spawn.monster_appears(player)
#         start_combat(player, lesser_spawn)
#         looting_enemy(lesser_spawn)
#         room.enemy['alive'] = False
#         rooms['room_twenty']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twenty']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_twentyone_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         flying_polyp = enemies.Enemy(enemies.flying_polyp)
#         flying_polyp.monster_appears(player)
#         start_combat(player, flying_polyp)
#         looting_enemy(flying_polyp)
#         room.enemy['alive'] = False
#         rooms['room_twentyone']['enemy']['alive'] = False
#
#         # Pick-up item
#         cursed_tome = items.Book(items.cursed_tome)
#         action = inventory.pickup_item(player, cursed_tome)
#         if action:
#             room.contents = ""
#             rooms['room_twentyone']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twentyone']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_twentyone']['contents'] != "":
#             # Pick-up item
#             cursed_tome = items.Book(items.cursed_tome)
#             action = inventory.pickup_item(player, cursed_tome)
#             if action:
#                 room.contents = ""
#                 rooms['room_twentyone']['contents'] = ""
#
#
# def room_twentytwo_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twentytwo']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_twentythree_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         dimensional_shambler = enemies.Enemy(enemies.dimensional_shambler)
#         dimensional_shambler.monster_appears(player)
#         start_combat(player, dimensional_shambler)
#         looting_enemy(dimensional_shambler)
#         room.enemy['alive'] = False
#         rooms['room_twentythree']['enemy']['alive'] = False
#
#         # Pick-up item
#         ancient_spellbook = items.Book(items.ancient_spellbook)
#         action = inventory.pickup_item(player, ancient_spellbook)
#         if action:
#             room.contents = ""
#             rooms['room_twentythree']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twentythree']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_twentythree']['contents'] != "":
#             # Pick-up item
#             ancient_spellbook = items.Book(items.ancient_spellbook)
#             action = inventory.pickup_item(player, ancient_spellbook)
#             if action:
#                 room.contents = ""
#                 rooms['room_twentythree']['contents'] = ""
#
#
# def room_twentyfour_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Combat
#         lesser_spawn = enemies.Enemy(enemies.lesser_spawn)
#         lesser_spawn.monster_appears(player)
#         start_combat(player, lesser_spawn)
#         looting_enemy(lesser_spawn)
#         room.enemy['alive'] = False
#         rooms['room_twentyfour']['enemy']['alive'] = False
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twentyfour']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#
#
# def room_twentyfive_script(player, room):
#     if not room.cleared:
#         # Entering room
#         room.location_check()
#         player.gain_sanity()
#
#         # Pick-up item
#         health_potion = items.Item(items.health_potion)
#         action = inventory.pickup_item(player, health_potion)
#         if action:
#             room.contents = ""
#             rooms['room_twentyfive']['contents'] = ""
#
#         # Room cleared
#         room.cleared = True
#         rooms['room_twentyfive']['cleared'] = True
#
#     else:
#         # Returning to room
#         print(Fore.WHITE + "This room is the same as when you left it.")
#         if rooms['room_twentythree']['contents'] != "":
#             # Pick-up item
#             health_potion = items.Potion(items.health_potion)
#             action = inventory.pickup_item(player, health_potion)
#             if action:
#                 room.contents = ""
#                 rooms['room_twentyfive']['contents'] = ""
#
#
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
# 
#                                AN UNSPEAKABLE PRESENCE APPROACHES
#                                
#     """)
    sleep(1)
    print(Fore.RED + """
          You are stricken with hopelessness. An unspeakable Servant of The Nameless Mist has appeared. 
                    It is a being of immense and terrifying power. It is unfathomably fast.""")
    print(Fore.YELLOW + "Your speed is a mere: " + str(player.speed))

    # Combat
    nyarlathotep = enemies.Enemy(enemies.nyarlathotep)
    nyarlathotep.monster_appears(player)
    start_combat(player, nyarlathotep)

    print(Fore.GREEN + Style.BRIGHT + """

                            THE SERVANT OF THE NAMELESS ABYSS IS STRUCK DOWN

    """)
    gamefunctions.victory(player)
    exit()


rooms = {
    'room_one': {
        'number': {'id': 1,
                   'str_id': "room_one"},
        # 'script': room_one_script,
        'description': "Blast marks and dark stains litter the walls of this room. In the center lies a robed skeleton "
                       "grasping a blue potion",
        'cleared': False,
        'directions': "There are doors to the [S]outh and [E]ast",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "Mana Potion",
                     'item_id': "potion/mana_potion",
                     'taken': False}
    },
    'room_two': {
        'number': {'id': 2,
                   'str_id': "room_two"},
        # 'script': room_two_script,
        'description': "A bare stone room, with a single clay golem wandering on the far side.",
        'cleared': False,
        'directions': "There are doors to the [N]orth and [E]ast",
        'enemy': {'name': 'Golem',
                  'id': "clay_golem",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_three': {
        'number': {'id': 3,
                   'str_id': "room_three"},
        # 'script': room_three_script,
        'description': "There is a foul muck covering the floor. A group of corpses lie in the center of the room,\n"
                       "strangely positioned. From the far side of the room, you feel a foul presence.",
        'cleared': False,
        'directions': "There is a door to the [E]ast.",
        'enemy': {'name': "Hunting Horror",
                  'id': "hunting_horror",
                  'alive': True},
        'contents': {'item_name': "Talisman",
                     'item_id': "talisman/sun_talisman",
                     'taken': False}
    },
    'room_four': {
        'number': {'id': 4,
                   'str_id': "room_four"},
        # 'script': room_four_script,
        'description': "Damaged and collapsed shelves decorate the walls, and overturned cauldrons and shattered flasks"
                       " litter the floor.\n" 
                       "It appears to be an ancient alchemical storeroom.",
        'cleared': False,
        'directions': "There are doors to the [S]outh and [E]ast",
        'enemy': {'type': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "Health Potion",
                     'item_id': "potion/health_potion",
                     'taken': False}

},
    'room_five': {
        'number': {'id': 5,
                   'str_id': "room_five"},
        # 'script': room_five_script,
        'description': " The room is littered with the bodies of fallen Lesser Spawn.\n"
                       "In the center, the corpse of a long dead warrior clutches something.\n" 
                       "Between you and the skeleton stands a Moon-Beast.",
        'cleared': False,
        'directions': "There is a door to the [N]orth",
        'enemy': {'name': "Moon-Beast",
                  'id': "moon_beast",
                  'alive': True},
        'contents': {'item_name': "Ornate Tome",
                     'item_id': "book/ornate_tome",
                     'taken': False}

    },
    'room_six': {
        'number': {'id': 6,
                   'str_id': "room_six"},
        # 'script': room_six_script,
        'description': "This room is barren and nondescript, with only a few skeletons to keep you company.",
        'cleared': False,
        'directions': "There are doors to the [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_seven': {
        'number': {'id': 7,
                   'str_id': "room_seven"},
        # 'script': room_seven_script,
        'description': " The room is empty, save for a lone pedestal holding an ancient scroll.\n"
                       "Before you reach the pedestal, a thick tar-like liquid flows from the walls\n"
                       "and amasses into a horrible shape.",
        'cleared': False,
        'directions': "There are doors to the [N]orth, [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "Shoggoth",
                  'id': "shoggoth",
                  'alive': True},
        'contents': {'item_name': "Ancient Scroll",
                     'item_id': "book/ancient_scroll",
                     'taken': False}
    },
    'room_eight': {
        'number': {'id': 8,
                   'str_id': "room_eight"},
        # 'script': room_eight_script,
        'description': "You see bare stone room, with a single Lesser Spawn on the far side.",
        'cleared': False,
        'directions': "There are doors to the [N]orth, [W]est and [E]ast",
        'enemy': {'name': "Lesser Spawn",
                  'id': "lesser_spawn",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_nine': {
        'number': {'id': 9,
                   'str_id': "room_nine"},
        # 'script': room_nine_script,
        'description': "This room is barren and nondescript, with only a few skeletons to keep you company.",
        'cleared': False,
        'directions': "There are doors to the [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_ten': {
        'number': {'id': 10,
                   'str_id': "room_ten"},
        # 'script': room_ten_script,
        'description': "Damaged and collapsed shelves decorate the walls, and overturned cauldrons and shattered flasks"
                       " litter the floor.\n" 
                       "It appears to be an ancient alchemical storeroom.",
        'cleared': False,
        'directions': "There is a door to the [N]orth",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "Mana Potion",
                     'item_id': "potion/mana_potion",
                     'taken': False}
    },
    'room_eleven': {
        'number': {'id': 11,
                   'str_id': "room_eleven"},
        # 'script': room_eleven_script,
        'description': "You see bare stone room, with a single clay golem wandering on the far side.",
        'cleared': False,
        'directions': "There are doors to the [S]outh, [W]est, and [E]ast",
        'enemy': {'name': "Golem",
                  'id': "clay_golem",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_twelve': {
        'number': {'id': 12,
                   'str_id': "room_twelve"},
        # 'script': room_twelve_script,
        'description': "Damaged and collapsed shelves decorate the walls, and overturned cauldrons and shattered flasks"
                       " litter the floor.\n" 
                       "It appears to be an ancient alchemical storeroom.",
        'cleared': False,
        'directions': "There are doors to the [N]orth, [S]outh, [E]ast, and [W]est.",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "Health Potion",
                     'item_id': "potion/health_potion",
                     'taken': False}
    },
    'room_thirteen': {
        'number': {'id': 13,
                   'str_id': "room_thirteen"},
        # 'script': room_thirteen_script,
        'description': "You see a barren room made of ancient stone riddled with moss and pockmarks.\n"
                       "There seems to be no enemies or items in this room.",
        'cleared': False,
        'directions': "There are door to the [N]orth, [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_fourteen': {
        'number': {'id': 14,
                   'str_id': "room_fourteen"},
        # 'script': room_fourteen_script,
        'description': "You see bare stone room, with a single clay golem wandering on the far side.",
        'cleared': False,
        'directions': "There are doors to the [N]orth, [S]outh, [W]est, and [E]ast",
        'enemy': {'name': "Golem",
                  'id': "clay_golem",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_fifteen': {
        'number': {'id': 15,
                   'str_id': "room_fifteen"},
        # 'script': room_fifteen_script,
        'description': "This room is large and ornate, with carvings of every sort adorning the walls.\n"
                       "In the center is a large pedestal with a single Silver Key laying upon it",
        'cleared': False,
        'directions': "There is a door to the [N]orth",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "Silver Key",
                     'item_id': "talisman/silver_key",
                     'taken': False}
    },
    'room_sixteen': {
        'number': {'id': 16,
                   'str_id': "room_sixteen"},
        # 'script': room_sixteen_script,
        'description': "This room is barren and nondescript, with only a few skeletons to keep you company.",
        'cleared': False,
        'directions': "There are doors to the [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_seventeen': {
        'number': {'id': 17,
                   'str_id': "room_seventeen"},
        # 'script': room_seventeen_script,
        'description': "You see bare stone room, with a single Lesser Spawn on the far side.",
        'cleared': False,
        'directions': "There are doors to the [N]orth, [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "Lesser Spawn",
                  'id': "lesser_spawn",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_eighteen': {
        'number': {'id': 18,
                   'str_id': "room_eighteen"},
        # 'script': room_eighteen_script,
        'description': "You see bare stone room, with a single clay golem wandering on the far side.",
        'cleared': False,
        'directions': "There are doors to the [N]orth, [W]est, and [E]ast",
        'enemy': {'name': "Golem",
                  'id': "clay_golem",
                  'alive': True},
        'contents': {'item_name': "Health Potion",
                     'item_id': "potion/health_potion",
                     'taken': False}
    },
    'room_nineteen': {
        'number': {'id': 19,
                   'str_id': "room_nineteen"},
        # 'script': room_nineteen_script,
        'description': "This room is barren and nondescript, with only a few skeletons to keep you company.",
        'cleared': False,
        'directions': "There are doors to the [S]outh, [E]ast, and [W]est",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_twenty': {
        'number': {'id': 20,
                   'str_id': "room_twenty"},
        # 'script': room_twenty_script,
        'description': "You see bare stone room, with a single Lesser Spawn on the far side.",
        'cleared': False,
        'directions': "There is a door to the [N]orth",
        'enemy': {'name': "Lesser Spawn",
                  'id': "lesser_spawn",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_twentyone': {
        'number': {'id': 21,
                   'str_id': "room_twentyone"},
        # 'script': room_twentyone_script,
        'description': "A stale wind sweeps past you as you enter the room.\n" 
                       "On the far side there is a pedestal with an strange book upon it.\n" 
                       "You have a feeling that you are not alone.",
        'cleared': False,
        'directions': "There are doors to the [S]outh and [W]est",
        'enemy': {'name': "Flying Polyp",
                  'id': "flying_polyp",
                  'alive': True},
        'contents': {'item_name': "Cursed Tome",
                     'item_id': "book/cursed_tome",
                     'taken': False}
    },
    'room_twentytwo': {
        'number': {'id': 22,
                   'str_id': "room_twentytwo"},
        # 'script': room_twentytwo_script,
        'description': "This room is barren and nondescript, with only a few skeletons to keep you company.",
        'cleared': False,
        'directions': "There are doors to the [N]orth and [W]est",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_twentythree': {
        'number': {'id': 23,
                   'str_id': "room_twentythree"},
        # 'script': room_twentythree_script,
        'description': "In the center room, a skeleton lays holding something.\n"
                       "As the door closes, you see a rift open on the far side of the room.\n" 
                       "A horrifying figure emerges.",
        'cleared': False,
        'directions': "There is a door to the [W]est",
        'enemy': {'name': "Dimensional Shambler",
                  'id': "dimensional_shambler",
                  'alive': True},
        'contents': {'item_name': "Ancient Spellbook",
                     'item_id': "book/ancient_spellbook",
                     'taken': False}
    },
    'room_twentyfour': {
        'number': {'id': 24,
                   'str_id': "room_twentyfour"},
        # 'script': room_twentyfour_script,
        'description': "You see bare stone room, with a single Lesser Spawn on the far side.",
        'cleared': False,
        'directions': "There are doors to the [S]outh and [W]est",
        'enemy': {'name': "Lesser Spawn",
                  'id': "lesser_spawn",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    },
    'room_twentyfive': {
        'number': {'id': 25,
                   'str_id': "room_twentyfive"},
        # 'script': room_twentyfive_script,
        'description': "Damaged and collapsed shelves decorate the walls, and overturned cauldrons and shattered flasks"
                       " litter the floor.\n" 
                       "It appears to be an ancient alchemical storeroom.",
        'cleared': False,
        'directions': "There is a door to the [N]orth",
        'enemy': {'name': "",
                  'id': "",
                  'alive': False},
        'contents': {'item_name': "Health Potion",
                     'item_id': "potion/health_potion",
                     'taken': False}
    },
    'room_twentysix': {
        'number': {'id': 26,
                   'str_id': "room_twentysix"},
        # 'script': room_twentysix_script,
        'description': Fore.RED + Style.BRIGHT + Back.RED + "You find yourself in the endless abyss... THE AVATAR OF"
                                                            " NYARLATHOTEP HAS AWOKEN" + Style.RESET_ALL,
        'cleared': False,
        'directions': "There are no doors, there is no escape. Defeat your enemy.",
        'enemy': {'name': "unspeakable sight",
                  'id': "nyarlathotep",
                  'alive': True},
        'contents': {'item_name': "",
                     'item_id': "",
                     'taken': True}
    }
}
