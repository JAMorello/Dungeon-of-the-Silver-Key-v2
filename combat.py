from colorama import Fore
from random import randint, choice
import gamefunctions
from player import Player
from time import sleep


def start_combat(player, enemy):
    print(Fore.MAGENTA + "Combat started!")
    sleep(1)
    combat_ongoing = True
    turn_order = check_speed(player, enemy)

    while combat_ongoing:
        for participant in turn_order:
            if participant is player:
                damage = player_attack(participant)
                establish_damage(damage, attacker=player, defender=enemy)
                if not check_health(player, enemy, show=False):
                    combat_ongoing = check_health(player, enemy)
                    break
            if participant is enemy:
                damage = enemy_attack(player, participant)
                establish_damage(damage, attacker=enemy, defender=player)
            if not damage == 0:
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
        print(Fore.RED + enemy.sanity_move + " you feel your sanity slipping.")  # ALSO "your sanity is under assault."
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
    player_action = ''

    # List of available player physical attacks and spells
    move_list = list()
    for move in player.attacks:
        print(player.attacks[move]['learned'])
        if player.attacks[move]['learned']:
            move_list.append(move)

    while player_action not in player.attacks:
        print('Select your action: ', ', '.join(move_list))
        player_action = input(">> ").lower()

        if player_action not in player.attacks:
            print("Please select an action available to you!")

    player_damage = 0
    if player_action == "thrust":
        player_damage = thrust(player)
    elif player_action == "slash":
        player_damage = slash(player)
    elif player_action == "heal":
        heal(player, spell="heal")
    elif player_action == "greater heal":
        heal(player, spell="greater heal")
    elif player_action == "pure of mind":
        pure_of_mind(player)
    elif player_action == "void flame":
        player_damage = void_flame(player)
    elif player_action == "call of madness":
        call_of_madness(player)
    return player_damage


def establish_damage(damage, attacker, defender):
    defender.health -= damage

    # Score
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


def thrust(player):
    move = player.attacks["thrust"]
    player_damage = randint(*move['thrust'])
    print(Fore.GREEN + choice(move["text"]) + ", dealing", str(player_damage), "damage.")
    return player_damage


def slash(player):
    move = player.attacks["slash"]
    player_damage = randint(*move['points'])
    print(Fore.GREEN + choice(move["text"]) + ", dealing", str(player_damage), "damage.")
    return player_damage


def void_flame(player):
    move = player.attack["void flame"]
    player_damage = 0
    if player.mana < move["mana cost"]:
        print(Fore.RED + "You don't have enough mana!")
    else:
        player_damage = randint(*move["points"])
        player.mana = -move["mana cost"]
        print(Fore.GREEN + choice(move["text"]), str(player_damage), " damage.")
    return player_damage


def call_of_madness(player):
    move = player.attacks["call of madness"]
    if player.sanity < move["sanity cost"]:
        gamefunctions.game_over(player, sanity_drain=True)
    amount = randint(*move['points'])
    print(Fore.GREEN + choice(move["text"]))
    player.mana = amount
    sanity_fluctuation(player, -amount)


def pure_of_mind(player):
    move = player.attacks["pure of mind"]
    if player.mana < move["mana cost"]:
        print(Fore.RED + "You don't have enough mana!")
    else:
        player.mana = -move["mana cost"]
        print(Fore.GREEN + choice(move["text"]))
        sanity_recovered = randint(*move["points"])
        sanity_fluctuation(player, sanity_recovered)


def heal(player, spell):
    move = player.attacks[spell]
    if player.mana < -move["mana cost"]:
        print(Fore.RED + "You have no mana remaining!")
    else:
        player.mana = move["mana cost"]

        healing = randint(*move["points"])
        print(Fore.GREEN + choice(move["text"]))

        player.health += healing

        player.change_score(points=healing, amount_healed=True)


def sanity_fluctuation(player, amount):
    player.sanity = (amount, True)
    if player.sanity == 0:
        gamefunctions.game_over(player, sanity_drain=True)
    player.change_score(points=-amount, sanity_lost=True)
