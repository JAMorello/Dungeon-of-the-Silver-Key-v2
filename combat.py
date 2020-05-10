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
    while player_action not in player.attacks:
        print(Fore.WHITE + 'Select your action: ', ', '.join(player.attacks))
        player_action = input(">> ").lower()

        if player_action not in player.attacks:
            print("Please select an action available to you!")

    player_damage = 0
    if player_action == "thrust":
        player_damage = thrust(player)
    elif player_action == "slash":
        player_damage = slash(player)
    elif player_action == "heal":
        heal(player, spell="heal", mana=-10)
    elif player_action == "greater heal":
        heal(player, spell="greater heal", mana=-30)
    elif player_action == "pure of mind":
        pure_of_mind(player)
    elif player_action == "void flame":
        player_damage = void_flame(player, mana=-30)
    elif player_action == "call of madness":
        call_of_madness(player)
    return player_damage


def establish_damage(damage, attacker, defender):
    defender.health -= damage

    # Score
    if type(attacker) is Player:
        change_score(attacker, damage, damage_done=True)
    if type(defender) is Player:
        change_score(defender, damage, damage_taken=True)


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
    player_damage = randint(*player.attacks['thrust'])
    print(Fore.GREEN + "You deftly weave between the enemy's attacks, giving your sword a powerful forward thrust, "
                       "dealing", str(player_damage), "damage.")
    return player_damage


def slash(player):
    player_damage = randint(*player.attacks['slash'])
    print(Fore.GREEN + "With a prayer, you swing your sword in a recklessly wide arc, dealing", str(player_damage),
          "damage.")
    return player_damage


def void_flame(player, mana):
    player_damage = 0
    if player.mana < mana:
        print(Fore.RED + "You don't have enough mana!")
    else:
        player_damage = randint(*player.attacks["void flame"])
        mana_fluctuation(player, -30)
        print(Fore.GREEN + "You lift a hand and chant the spell. A torrent of invisible flame pours forth from the "
                           "Abyss, dealing ", str(player_damage), " damage.")
    return player_damage


def call_of_madness(player):
    if player.sanity < 35:
        gamefunctions.game_over(player, sanity_drain=True)
    energy = randint(*player.attacks['call of madness'])
    print(Fore.GREEN + """Cosmic winds cackle about you. You feel arcane power course through you. You feel... 
    unstable.""")
    mana_fluctuation(player, energy)
    sanity_fluctuation(player, -energy)


def pure_of_mind(player):
    if player.mana < 20:
        print(Fore.RED + "You don't have enough mana!")
    else:
        mana_fluctuation(player, -20)
        print(
            Fore.GREEN + """You close your eyes and chant the incantation, for a brief second you can 
                feel a ghostly hand upon your shoulder, offering its support. Your mind is clear and you 
                can feel your sanity returning.""")
        sanity_recovered = randint(*player.attacks['pure of mind'])
        sanity_fluctuation(player, sanity_recovered)


def heal(player, spell, mana):
    if player.mana < -mana:
        print(Fore.RED + "You have no mana remaining!")
    else:
        mana_fluctuation(player, mana)

        healing = 0
        if spell == "heal":
            healing = randint(*player.attacks["heal"])

            print(Fore.GREEN + "A warm light encompasses you and vigor flows back into your damaged limbs. You are "
                               "healed for ", str(healing), " health.")
        if spell == "greater heal":
            healing = randint(*player.attacks["greater heal"])
            print(Fore.GREEN + "A ray of divine light falls upon you, breathing life into your damaged form... you are "
                               "healed for """ + str(healing))

        player.health += healing
        if player.health > player.base_stats['max_health']:
            player.health = player.base_stats['max_health']
        print(Fore.GREEN + "Your health is now " + str(player.health))

        change_score(player, points=healing, amount_healed=True, )


def sanity_fluctuation(player, amount):
    player.sanity += amount
    if player.sanity > player.base_stats['max_sanity']:
        player.sanity = player.base_stats['max_sanity']
    if player.sanity < 0:
        gamefunctions.game_over(player, sanity_drain=True)
    print(Fore.GREEN + "Your sanity is " + str(player.sanity) + Fore.WHITE)
    change_score(player, points=-amount, sanity_lost=True)


def mana_fluctuation(player, amount):
    player.mana += amount
    if player.mana < 0:
        player.mana = 0
    if player.mana > player.base_stats['max_mana']:
        player.mana = player.base_stats['max_mana']
    print("You have " + str(player.mana) + " mana remaining.")


def change_score(player, points=0, damage_done=False, damage_taken=False, amount_healed=False, sanity_lost=False):
    if damage_done:
        player.damage_done += points
    if damage_taken:
        player.damage_taken += points
    if amount_healed:
        player.amount_healed += points
    if sanity_lost:
        player.sanity_lost += points
