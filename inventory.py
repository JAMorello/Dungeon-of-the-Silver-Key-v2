from random import randrange
from colorama import Fore
from tabulate import tabulate
import items
from items import Book, Talisman
from time import sleep


class Inventory:
    def __init__(self):
        self.backpack = dict()

    def add_item(self, item):
        if item.name in self.backpack:
            self.backpack[item.name][1] += 1
        else:
            self.backpack.update({item.name: [item, 1]})

    def drop_item(self, item):
        self.backpack[item][1] -= 1
        if self.backpack[item][1] == 0:
            del self.backpack[item]

    def use_item(self, item, player):
        if item == "health":
            self.drop_item("Health Potion")
            player.health = items.potion['health_potion']['healing']
        if item == "mana":
            self.drop_item("Mana Potion")
            player.mana = items.potion['mana_potion']['mana_recover']

    def show_inventory(self):
        show_inventory = [['Name', 'Quantity']]
        if self.backpack:
            for item in self.backpack:
                show_inventory.append([item, self.backpack[item][1]])
            print(tabulate(show_inventory, tablefmt="fancy_grid"))
            return True
        else:
            print("You don´t have any items!")
            return False

    def inspect_inventory(self):
        any_item = self.show_inventory()
        if any_item:
            more_actions = ''
            response = True
            while not more_actions:
                item = input("What item do you want to inspect? (Or else, [Q]uit) ")
                if item in INVENTORY.backpack:
                    self.backpack[item][0].inspect_item()
                else:
                    response = False

                if not response:
                    if item.lower() == "q" or item.lower() == "quit":
                        more_actions = "quit"
                    else:
                        print("Else you don´t have that object or you didn´t write its name correctly.")
                else:
                    more_actions = input("Anything else? [Yes/No]: ").lower()
                    if more_actions == "yes" or more_actions == "y":
                        more_actions = ""


def pickup_item(player, item):
    print(item.found_object)
    item_grabbed = False
    done_picking = False
    while not done_picking:
        action = input("Take it? [Yes/No]: ").lower()
        if action == "yes" or action == "y":
            print(Fore.WHITE + item.grab_object)
            INVENTORY.add_item(item)
            sleep(1)
            if type(item) is Book:
                player.attacks[item.spell.lower()]["learned"] = True
                print(Fore.GREEN + f"You learn {item.spell}!" + Fore.WHITE)
                sleep(1)
            if type(item) is Talisman:
                player.boost_stats(item.stat_boost)
                print(Fore.GREEN + f"You feel stronger!" + Fore.WHITE)
                sleep(1)
            item_grabbed = True
            done_picking = True
        elif action == "no" or action == "n":
            confirmation = input("Are you sure you wish to leave the item here? [Yes/No]: ").lower()
            if confirmation == "yes" or confirmation == "y":
                print("You leave the item where it is.")
                done_picking = True
            elif confirmation != "no" or confirmation != "n":
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
                                "scroll flash through your mind. Perhaps there is still more to find in this dungeon..."
                  + Fore.WHITE)
            sleep(1)
            action = input("Pick up the key, despite your better instincts? [Yes/No]: ").lower()
            if action == "yes" or action == "y":
                print(Fore.WHITE + item.grab_object)
                sleep(1)
                INVENTORY.add_item(item)
                player.boost_stats(item.stat_boost)
                print(Fore.GREEN + f"You feel stronger!" + Fore.WHITE)
            elif action == "no" or action == "n":
                print(Fore.WHITE + "You decide to heed your instincts and stay your hand... perhaps the dungeon has "
                                   "some items left that will aid in your journey.")
                sleep(1)
            else:
                print("Make up your mind!")
            done_picking = True
        else:
            action = input("Pick up the key? [Yes/No]: ").lower()
            if action == "yes" or action == "y":
                print(Fore.WHITE + item.grab_object)
                item.inspect_item()
                sleep(1)
                INVENTORY.add_item(item)
                player.boost_stats(item.stat_boost)
                print(Fore.GREEN + f"You feel stronger!" + Fore.WHITE)
            elif action == "no" or action == "n":
                print(Fore.WHITE + "You decide to heed your instincts and stay your hand... perhaps the dungeon has "
                                   "some items left that will aid in your journey.")
                sleep(1)
            else:
                print("Make up your mind!")
            done_picking = True


def looting_enemy(enemy):
    drop = randrange(enemy.drop_chance)
    if drop >= 3:
        health_potion = items.Potion(items.potion['health_potion'])
        print(Fore.GREEN + "The " + enemy.name + " drops a health potion!" + Fore.WHITE)
        INVENTORY.add_item(health_potion)
    if drop < 3:
        print(Fore.WHITE + "The " + enemy.name + " did not drop any items.")
    sleep(1)


INVENTORY = Inventory()
