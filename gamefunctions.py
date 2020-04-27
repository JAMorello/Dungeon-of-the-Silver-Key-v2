from pyfiglet import Figlet
# https://github.com/pwaller/pyfiglet
from colorama import Fore, Style, Back
# https://pypi.org/project/colorama/
from tabulate import tabulate
# https://pypi.org/project/tabulate/
from time import sleep
from inventory import INVENTORY
from player import Player

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

    # Old key ascii art
    #
    #  8 8 8 8                     ,ooo.
    #  8a8 8a8                    oP   ?b
    # d888a888zzzzzzzzzzzzzzzzzzzz8     8b
    #  `""^""'                    ?o___oP'

    print(Fore.YELLOW + title)
    print(Fore.YELLOW + title2)
    print(Fore.WHITE + custom_art)


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
        enter_the_dungeon = input("Your mark has been left. Will you enter the dungeon? [Y/N]: ").upper()

        # Enter the dungeon
        if enter_the_dungeon == "Y":
            print("You steel your resolve and descend into the abyss.")
            break

        # Doubt
        elif enter_the_dungeon == "N":
            print("You think back to all those depending on you. Surely, you would'nt let them down so easily?")
            are_you_sure = input("Let those who are counting on you down? [Y/N]: ").upper()

            # Cowardice - Game over
            if are_you_sure == "Y":
                print(Fore.RED + "This world has no room for cowards such as you.")
                player.PlayerHealth = 0
                print("You have been deemed unworthy, perhaps the world will find a more suitable hero to conquer the "
                      "dungeon.")
                game_over(player)
                exit()

            # Resolve - return to initial state
            elif are_you_sure == "N":
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
    """  Essential to game operation. This function allows the player to inspect inventory, use items, and view the map
    outside of combat"""

    # Update the game map
    GAME_MAP[(room.number['id'] % 5) - 1][room.number['id'] // 5] = str(room.number['id'])

    done = False
    while not done:
        action = input(Fore.WHITE + "[I]nspect inventory, [U]se item, [E]xamine room, [G]rab item, [V]iew map, "
                                    "or [C]ontinue?: ").upper()

        # Inspect items in inventory
        if action == "I":
            INVENTORY.use_inventory(inspect=True)

        # Use objects in inventory
        if action == "U":
            INVENTORY.use_inventory(player, use=True)

        # Examine the room (shows the room´s description and his contents)
        if action == "E":
            room.location_check()

        # Grab the left behind item in the room
        if action == "G":
            if not room.contents['taken']:
                room.create_and_pickup_item(player)
            else:
                print("There isn´t any item here")

        # View game map
        if action == "V":
            print(Fore.YELLOW + "You are in room " + str(room.number['id']))
            print(tabulate(GAME_MAP, tablefmt="fancy_grid"))
            print(Fore.LIGHTWHITE_EX + """
              N
            W o E
              S
                           """)

        if action == "C":
            done = True


def calculate_score(player):
    positives = player.damage_done + player.amount_healed
    negatives = player.damage_taken + player.sanity_lost
    score = positives - negatives

    print("\n" + Fore.YELLOW + "You did " + str(player.damage_done) + " points of damage!")
    print(Fore.YELLOW + "You healed for " + str(player.amount_healed) + " points!")
    print(Fore.RED + "You took " + str(player.damage_taken) + " points of damage!")
    print(Fore.RED + "You lost " + str(player.sanity_lost) + " points of sanity!")
    print(Fore.YELLOW + "Your score was: " + str(score) + " points.\n")


# Game over due sanity reaching 0 points or less or dying in a battle
def game_over(player, sanity_drain=False, dead_in_battle=False):
    game_end = Figlet(font='cyberlarge').renderText("Game Over")

    if sanity_drain:
        print(Fore.RED + "The darkness of the dungeon comes rushing in, a terrifying force of overwhelming power. From "
                         "far away, you hear yourself cry out.")
        print(Fore.RED + "You have been driven to madness.\n")
    if dead_in_battle:
        print(Fore.RED + "You gasp for air while drowning in your own blood.\n"
                         "You have died.")

    calculate_score(player)
    print(Fore.RED + game_end)
    exit()


# Winning the game after defeating Nyarlathotep
def victory(player):
    victory_message = Figlet(font='cyberlarge').renderText("YOU STAND VICTORIOUS\n")
    print(Fore.GREEN + victory_message)

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
                      "Speak my name, and it shall unlock all the doors of the cosmos.")

    final_choice = input(Fore.WHITE + "Speak the name? [Y/N]: ").upper()

    if final_choice == "Y":
        print(Fore.GREEN + Style.BRIGHT +
              "                         You shout to the cosmos: " + Fore.BLUE + "YOG-SOTHOTH")
        print(Fore.WHITE + Style.RESET_ALL + Back.RESET +
              "The Silver Key glows with cosmic radiance and your vision fades to white... \n"
              "You know not what awaits you next.\n\n" +
              Fore.BLUE + "[[END OF THE GAME]]")
        exit()
    else:
        print(Fore.WHITE + "Your vision fades to black... when you awake, you stand at the entrance to the dungeon.\n"
                           "The walls, once filled with the names of those who challenged the dungeon, are now clear,\n"
                           "save for one name... """ + Fore.YELLOW + player.username + "\n\n" +
              Fore.BLUE + "[[END OF THE GAME]]")
        exit()
