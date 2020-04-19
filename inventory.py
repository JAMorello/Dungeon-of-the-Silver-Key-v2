from random import randrange
from colorama import Fore
from tabulate import tabulate
import items
from items import Book, Talisman
from combat import mana_fluctuation


class Inventory:
    def __init__(self):
        self.backpack = dict()

    def add_item(self, item):
        if item.name in self.backpack:
            self.backpack[item.name][1] += 1
        else:
            self.backpack.update({item.name: [item, 1]})

    def use_item(self, item, player):
        if item == "Health Potion":
            self.drop_item(item)
            player.gain_health(items.health_potion['healing'], player)
        if item == "Mana Potion":
            self.drop_item(item)
            mana_fluctuation(player, items.mana_potion['mana_recover'])

    def drop_item(self, item):
        self.backpack[item][1] -= 1
        if self.backpack[item][1] == 0:
            del self.backpack[item]

    def show_inventory(self):
        show_inventory = [['Name', 'Quantity']]
        for item in self.backpack:
            show_inventory.append([item, self.backpack[item][1]])
        print(tabulate(show_inventory, tablefmt="fancy_grid"))

    def use_inventory(self, player=None, inspect=False, use=False):
        self.show_inventory()
        more_actions = ''
        item = ""
        response = True
        while not more_actions:
            if inspect:
                item = input("What item do you want to inspect? (Or else, [Q]uit) ")
                if item in INVENTORY.backpack:
                    self.backpack[item][0].inspect_item()
                else:
                    response = False
            if use:
                item = input("Select usable item (Or else, [Q]uit): ")
                if item in INVENTORY.backpack:
                    INVENTORY.use_item(item, player)
                else:
                    response = False

            if not response:
                if item.lower() == "q":
                    more_actions = "quit"
                else:
                    print("Else you don´t have that object or you didn´t write its name correctly.")
            else:
                more_actions = input("Anything else? [Y/N]: ").upper()
                if more_actions == "Y":
                    more_actions = ""
                    continue


def pickup_item(player, item):
    print(item.found_object)
    item_grabbed = False
    done_picking = False
    while not done_picking:
        action = input("Take it? [Y/N]: ").upper()
        if action == "Y":
            print(Fore.WHITE + item.grab_object)
            INVENTORY.add_item(item)
            if type(item) is Book:
                player.attacks[item.spell] = item.damage
                print(Fore.GREEN + f"You learn {item.spell}!")
            if type(item) is Talisman:
                player.boost_stats(item.stat_boost)
                print(Fore.GREEN + f"You feel stronger!")
            item_grabbed = True
            done_picking = True
        elif action == "N":
            confirmation = input("Are you sure you wish to leave the item here? [Y/N]: ").upper()
            if confirmation == "Y":
                print("You leave the item where it is.")
                done_picking = True
            elif confirmation != "N":
                print("Make up your mind!")
        else:
            print("Make up your mind!")
    return item_grabbed


def pick_key(player, item):
    print(item.found_object)
    done_picking = False
    while not done_picking:
        if "Sun Talisman" and "Ancient Scroll" not in INVENTORY.backpack:
            print(Fore.YELLOW + "You reach for the key, but a force demands you hesitate... visions of a sun and a\n"
                                "scroll flash through your mind. Perhaps there is still more to find in this dungeon...")
            action = input(Fore.WHITE + "Pick up the key, despite your better instincts? Y/N: ").upper()
            if action == "Y":
                print(Fore.WHITE + item.grab_object)
                item.inspect_item()
                INVENTORY.add_item(item)
                player.boost_stats(item.stat_boost)
            elif action == "N":
                print(Fore.WHITE + "You decide to heed your instincts and stay your hand... perhaps the dungeon has "
                                   "some items left that will aid in your journey.")
            else:
                print("Make up your mind!")
            done_picking = True
        else:
            action = input(Fore.WHITE + "Pick up the key? Y/N: ").upper()
            if action == "Y":
                print(Fore.WHITE + item.grab_object)
                item.inspect_item()
                INVENTORY.add_item(item)
                player.boost_stats(item.stat_boost)
            elif action == "N":
                print(Fore.WHITE + "You decide to heed your instincts and stay your hand... perhaps the dungeon has "
                                   "some items left that will aid in your journey.")
            else:
                print("Make up your mind!")
            done_picking = True


def looting_enemy(enemy):
    drop = randrange(enemy.drop_chance)
    if drop >= 3:
        health_potion = items.Potion(items.health_potion)
        print(Fore.GREEN + "The " + enemy.name + " drops a health potion!")
        INVENTORY.add_item(health_potion)
    if drop < 3:
        print(Fore.WHITE + "The " + enemy.name + " did not drop any items.")


INVENTORY = Inventory()
