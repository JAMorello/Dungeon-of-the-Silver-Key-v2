import gamefunctions
import rooms
import colorama

# Original coded by Mili-NT (Python 3.6.0, January 2019)
# Modifications made by JAMorello (Python 3.8.2, April 2020)
# Credits to H.P. Lovecraft and r/LearnPython


if __name__ == '__main__':
    colorama.init()
    gamefunctions.display_title()
    player = gamefunctions.enter_dungeon()
    # First action of the player
    rooms.trigger_room(player)
