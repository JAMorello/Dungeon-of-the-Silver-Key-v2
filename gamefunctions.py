from pyfiglet import Figlet
# https://github.com/pwaller/pyfiglet
from colorama import Fore, Style, Back
# https://pypi.org/project/colorama/
from tabulate import tabulate
# https://pypi.org/project/tabulate/
from sys import exit
from time import sleep
from inventory import INVENTORY, pick_key
from player import Player
from gameparser import parse_command

GAME_MAP = [[" ? ", " ? ", " ? ", " ? ", " ? "],
            [" ? ", " ? ", " ? ", " ? ", " ? "],
            [" ? ", " ? ", " ? ", " ? ", " ? "],
            [" ? ", " ? ", " ? ", " ? ", " ? "],
            [" ? ", " ? ", " ? ", " ? ", " ? "]]


def display_title():
    """ This function display the game title and an custom art in the initial screen"""
    title = Figlet(font='doom').renderText("Dungeon of the")  # Old font: cyberlarge
    title2 = Figlet(font='doom').renderText("             Silver Key")

    custom_art = """
             .(*                                                                
           /,*% */((/**                                                         
        ,,&,*/,# .,   %,                                                        
       ,,/ /,,,,,* .( ..  ./                                                    
     ,#  ....*/(##....****************************************///////////*    
       ,,& / ,,,.,/.& ,. ..#                                   ##%  %%%         
        ,,/,% ,/ .,   ,,                                      ,//,,,,.,,        
           /%(, **%%.**                                      .. ,. *,.,,,       
             #/(                                               ,,, ,,,,         
                                                                (/ *(           
    """

    print(Fore.YELLOW + title)
    sleep(1)
    print(Fore.YELLOW + title2)
    sleep(1)
    print(Fore.WHITE + custom_art)
    sleep(3)


def enter_dungeon():
    # Initial description of the dungeon entrance
    print(Fore.WHITE +
          "The entrance to the dungeon is a large, menacing crevice. On the walls, the names and messages of\n"
          "those who came before you are visible. You decide to leave a simple note, and leave your name on\n"
          "the wall with those hundreds that challenged the dungeon before you.\n")

    # Player object
    username = input("Leave your name: ")
    player = Player(username, location="room_thirteen")  # Room 13 is the initial room

    # Player first decision: enter or not the dungeon
    while True:
        enter_the_dungeon = input("Your mark has been left. Will you enter the dungeon? [Yes/No]: ").lower()

        # Enter the dungeon
        if enter_the_dungeon == "yes" or enter_the_dungeon == "y":
            print("You steel your resolve and descend into the abyss.")
            sleep(2)
            break

        # Doubt
        elif enter_the_dungeon == "no" or enter_the_dungeon == "n":
            print("You think back to all those depending on you. Surely, you would'nt let them down so easily?")
            are_you_sure = input("Let those who are counting on you down? [Yes/No]: ").lower()

            # Cowardice - Game over
            if are_you_sure == "yes" or are_you_sure == "y":
                print(Fore.RED + "This world has no room for cowards such as you.")
                player.PlayerHealth = 0
                print("You have been deemed unworthy, perhaps the world will find a more suitable hero to conquer the "
                      "dungeon.")
                sleep(3)
                game_over(player)
                sleep(180)
                exit()

            # Resolve - return to initial state
            elif are_you_sure == "no" or are_you_sure == "n":
                print("The thoughts of those who depend on you bolsters your courage.")
                continue

            # Confusion - return to initial state
            else:
                print("What are you even thinking?")
                continue

        # Confusion - return to initial state
        else:
            print("Make your choice.")
            continue
    return player


def perform_action(player, room):
    """  Essential to game operation. This function allows the player to do a lot of things outside of combat """

    done = False
    while not done:
        action, result = parse_command()

        if result:
            # Use potions in inventory
            if result == "use_health_potion":
                if "Health Potion" in INVENTORY.backpack:
                    INVENTORY.use_item('health', player)
                else:
                    print("You don´t have any Health Potion")
            if result == "use_mana_potion":
                if "Mana Potion" in INVENTORY.backpack:
                    INVENTORY.use_item('mana', player)
                else:
                    print("You don´t have any Mana Potion")

            # Grab the left behind potion in the room
            if result == "take_potion":
                if not room.contents['taken']:
                    room.create_and_pickup_item(player, take_item="potion")
                else:
                    print("There isn´t any item here")

        if action:

            if action[0] == "look":

                # Inspect items in inventory
                if action[1] == "inventory" or action[1] == "inv":
                    INVENTORY.inspect_inventory()

                # Examine the room (shows the room´s description and his contents)
                if action[1] == "room":
                    room.location_check()

                # Shows the available directions to move
                if action[1] == "door":
                    room.available_directions()

                # View game map
                if action[1] == "map":
                    print(Fore.YELLOW + "You are in room " + str(room.number['id']))
                    print(tabulate(GAME_MAP, tablefmt="fancy_grid"))
                    print(Fore.WHITE + "")

            # Grab the left behind potion in the room
            if action[0] == "take":
                if not room.contents['taken']:
                    if action[1] == "potion":
                        room.create_and_pickup_item(player, take_item="potion")
                    if action[1] == "book":
                        room.create_and_pickup_item(player, take_item="book")
                    if action[1] == "talisman":
                        room.create_and_pickup_item(player, take_item="talisman")
                    if action[1] == "key":
                        key = room.create_and_pickup_item(player, take_item="talisman", key=True)
                        pick_key(player, key)
                else:
                    print("There isn´t any item here")

            # This changes the rooms: the players travels from one room to another.
            if action[0] == "move":
                if action[1] not in room.directions['available']:
                    print(Fore.YELLOW + "There is no door in that direction." + Fore.WHITE)
                else:
                    player.location = room.directions['available'][action[1]]
                    done = True


# TODO: Functions relative to game in general:
    # do_look(): in general ("look"); to object, to room, to direction (cleaner())
    # do_examine(): ("examine") "Examine what?"; with obj, do_look(). ¿What if more info?
    # inventory: do not show if there isnt any item


def calculate_score(player):
    positives = player.damage_done + player.amount_healed
    negatives = player.damage_taken + player.sanity_lost
    score = positives - negatives

    print("\n\n" + Fore.YELLOW + "You did " + str(player.damage_done) + " points of damage!")
    sleep(0.25)
    print(Fore.YELLOW + "You healed for " + str(player.amount_healed) + " points!")
    sleep(0.25)
    print(Fore.RED + "You took " + str(player.damage_taken) + " points of damage!")
    sleep(0.25)
    print(Fore.RED + "You lost " + str(player.sanity_lost) + " points of sanity!")
    sleep(0.25)
    print(Fore.YELLOW + "Your score was: " + str(score) + " points.\n")
    sleep(1)


# Game over due sanity reaching 0 points or less or dying in a battle
def game_over(player, sanity_drain=False, dead_in_battle=False):
    game_end = Figlet(font='cyberlarge').renderText("Game Over")

    if sanity_drain:
        print(Fore.RED + "The darkness of the dungeon comes rushing in, a terrifying force of overwhelming power. From "
                         "far away, you hear yourself cry out.")
        print(Fore.RED + "You have been driven to madness.\n")
        sleep(1.5)
    if dead_in_battle:
        print(Fore.RED + "You gasp for air while drowning in your own blood.\n"
                         "You have died.")
        sleep(1.5)

    calculate_score(player)
    print(Fore.RED + game_end)
    exit()


# Winning the game after defeating Nyarlathotep
def victory(player):
    victory_message = Figlet(font='cyberlarge').renderText("YOU STAND VICTORIOUS\n")
    print(Fore.GREEN + victory_message)
    sleep(2)

    calculate_score(player)

    sleep(5)
    print(Fore.WHITE + "                                             ...                                             ")
    sleep(1)
    print(Fore.WHITE + "                                             ...                                             ")
    sleep(1)
    print(Fore.WHITE + "                                             ...                                             ")
    sleep(1)

    print(Fore.BLUE + "You hear a voice, loud and silent, swaying in an unearthly rhythm... " +
          Fore.GREEN + player.username +
          Fore.BLUE + "...\n You have conquered a mighty foe, risking life and limb to prove your worth...\n"
                      "Consider it acknowledged. For your deeds, I bid you keep that Silver Key.\n"
                      "Speak my name, and it shall unlock all the doors of the cosmos." + Fore.WHITE)
    sleep(2)
    final_choice = input("Speak the name? [Yes/No]: ").lower()

    if final_choice == "yes" or final_choice == "y":
        print(Fore.GREEN + Style.BRIGHT +
              "\n                         You shout to the cosmos: " + Fore.YELLOW + "YOG-SOTHOTH")
        sleep(1)
        print(Fore.WHITE + Style.RESET_ALL + Back.RESET +
              "\nThe Silver Key glows with cosmic radiance and your vision fades to white... \n"
              "You know not what awaits you next.\n\n")
    else:
        print(Fore.WHITE + "Your vision fades to black... when you awake, you stand at the entrance to the dungeon.\n"
                           "The walls, once filled with the names of those who challenged the dungeon, are now clear,\n"
                           "save for one name... """ + Fore.YELLOW + player.username + "\n\n")
    sleep(2)
    print(Fore.BLUE + Style.BRIGHT +"[[END OF THE GAME]]")
    sleep(180)
    exit()
