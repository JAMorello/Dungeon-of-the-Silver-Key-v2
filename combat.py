from colorama import Fore
from random import randint, choice
import gamefunctions
from player import Player
from time import sleep


def start_combat(player, enemy):
    print(Fore.MAGENTA + "Combat started!" + Fore.WHITE)
    sleep(1)
    combat_ongoing = True
    turn_order = check_speed(player, enemy)

    while combat_ongoing:
        for participant in turn_order:
            damage = 0
            if participant is player:
                damage = player_attack(participant)
                deal_damage(damage, attacker=player, defender=enemy)
                if not check_health(player, enemy, show=False):
                    combat_ongoing = check_health(player, enemy)
                    break
            if participant is enemy:
                damage = enemy_attack(player, participant)
                deal_damage(damage, attacker=enemy, defender=player)
            if damage != 0:
                combat_ongoing = check_health(player, enemy)
            sleep(1.5)


def check_speed(player, enemy):
    if player.speed >= enemy.speed:
        return [player, enemy]
    else:
        return [enemy, player]


def enemy_attack(player, enemy):
    move, enemy_damage_range = choice(list(enemy.attacks.items()))
    if move[:3] == "[S]":  # if the attack affects the sanity
        print(Fore.RED + enemy.sanity_move + " you feel your sanity slipping.")
        sanity_fluctuation(player, -enemy_damage_range)
        enemy_damage = 0
    else:  # If it is a physical attack
        enemy_damage = randint(*enemy_damage_range)
        if move[:2] == "[N]":  # If it is the special attack of Nyarlathotep
            print(Fore.RED + enemy.special_move)
        else:
            print(Fore.RED + enemy.signature_move + move + ", dealing " + str(enemy_damage), "damage")
    return enemy_damage


def player_attack(player):
    # List of available player physical attacks and spells
    move_list = list()
    for move in player.attacks:
        if player.attacks[move]['learned']:
            move_list.append(move)

    # Player enters their move of choice
    move = ''
    while move not in player.attacks:
        print(Fore.WHITE + 'Select your action: ', ', '.join(move_list))
        move = input(">> ").lower()

        if move not in player.attacks:
            print("Please select an action available to you!")

    move = player.attacks[move]  # For easy access to move data
    player_damage = 0  # Initialize damage. Default 0 for spells that doesn´t deal damage

    amount = randint(*move["points"])  # The kind of "amount" depends on the move and type

    if move["physical"]:
        player_damage = amount
        print(Fore.GREEN + choice(move["text"]))  # Prints a random text of the move
        print("You deal", str(player_damage), "damage.")

    if move["spell"]:
        if player.mana < move["mana cost"]:
            print(Fore.RED + "You don't have enough mana!")
        elif player.sanity < move["sanity cost"]:
            gamefunctions.game_over(player, sanity_drain=True)  # Game losing condition: sanity going to zero
        else:

            player.mana = -move["mana cost"]  # spending mana to cast spell
            print(Fore.GREEN + choice(move["text"]))  # Prints a random text of the move

            if move["type"] == "offensive":
                player_damage = amount
                print(Fore.GREEN + "You deal", str(player_damage), "damage.")

            if move["type"] == "mana":
                player.mana = amount  # mana recovered
                sanity_fluctuation(player, -amount)  # losing sanity

            if move["type"] == "sanity":
                sanity_fluctuation(player, amount)  # sanity recovered

            if move["type"] == "health":
                player.health = amount  # health recovered
                player.change_score(points=amount, amount_healed=True)

    return player_damage


def deal_damage(damage, attacker, defender):
    defender.health = -damage
    # Updating score
    if type(attacker) is Player:
        attacker.change_score(damage, damage_done=True)
    if type(defender) is Player:
        defender.change_score(damage, damage_taken=True)


def check_health(player, enemy, show=True):
    if enemy.health > 0:
        if show:
            print(Fore.RED + "The enemy's health is " + str(enemy.health))
    else:
        if show:
            print(Fore.RED + "The enemy is dead.")
        return False

    if player.health <= 0:
        if show:
            print(Fore.RED + "Your health is 0.")
            sleep(1)
            gamefunctions.game_over(player, dead_in_battle=True)
    else:
        if show:
            print(Fore.GREEN + "Your health is " + str(player.health))

    return True


def sanity_fluctuation(player, amount):
    player.sanity = (amount, True)
    if player.sanity == 0:
        gamefunctions.game_over(player, sanity_drain=True)
