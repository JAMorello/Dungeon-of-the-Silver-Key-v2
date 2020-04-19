class Item:
    def __init__(self, item_properties):
        self.name = item_properties['name']
        self.description = item_properties['description']
        self.found_object = item_properties['found_object']
        self.grab_object = item_properties['grab_object']

    def inspect_item(self):
        print("This item is a " + self.name + ". " + "It is " + self.description)


class Book(Item):
    def __init__(self, item_properties):
        super().__init__(item_properties)
        self.spell = item_properties['spell']
        self.damage = item_properties['damage']


class Potion(Item):
    def __init__(self, item_properties):
        super().__init__(item_properties)
        self.healing = item_properties['healing']
        self.mana_recover = item_properties['mana_recover']

    def inspect_item(self):
        print("This item is a " + self.name + ". " + "It is " + self.description)
        if self.healing > 0:
            print("This item restores " + str(self.healing) + " health.")
        if self.mana_recover > 0:
            print("This item restores " + str(self.mana_recover) + " health.")


class Talisman(Item):
    def __init__(self, item_properties):
        super().__init__(item_properties)
        self.stat_boost = item_properties['stat_boost']

    def inspect_item(self):
        print("This item is a " + self.name + ". " + "It is " + self.description)
        if self.stat_boost > 0:
            print("This item boosts your stats by " + str(self.stat_boost))


# Books
book = {
    # Room 5
    'ornate_tome': {
        'name': "Ornate Tome",
        'description': "a large, white book bound with gold thread. It must have been a holy book at some point.",
        'found_object': "You see a skeleton grasping an ornated tome, previously obscured by the mist.",
        'grab_object': "The tome contains a powerful healing spell, capable of curing even the most gruesome wounds.",
        'spell': "greater heal",
        'damage': (50, 60)
    },
    # Room 21
    'cursed_tome': {
        'name': "Cursed Tome",
        'description': "a book bound in a most unsettling familiar substance.",
        'found_object': "You approach the pedestal and inspect the book.",
        'grab_object': "The tome contains a dark spell that can regenerate the caster's mana... at the cost of his sanity.",
        'spell': "call of madness",
        'damage': (30, 35)
    },
    # Room 7
    'ancient_scroll': {
        'name': "Ancient Scroll",
        'description': "an eon old scroll of bloodied and torn parchment.\n"
                       "It appears to have a spell inscribed upon it.",
        'found_object': "You approach the pedestal that holds the scroll.",
        'grab_object': "Madness has claimed many in this dark place, yet before it took it's toll, a long dead sorcerer\n"
                       "had penned his final spell- a hopeful chant to push back the darkness of the dungeon.",
        'spell': "pure of mind",
        'damage': (20, 30)
    },
    # Room 23
    'ancient_spellbook': {
        'name': "Ancient Spellbook",
        'description': "a leather-bound spellbook containing arcane symbols and instructions",
        'found_object': "You found that the skeleton is grasping a spellbook.",
        'grab_object': "You pick up the spellbook and read it's contents.\n"
                       "It is a spellbook that teaches the user to summon forth a powerful torrent of invisible flames\n"
                       "from the abyss, searing the target's soul. ",
        'spell': "void flame",
        'damage': (35, 50)
    }
}

# Potions
potion = {
    # Rooms 4, 12, 18, 25
    'health_potion': {
        'name': "Health Potion",
        'description': "a red-hued restorative brew mixed by a skilled alchemist.",
        'found_object': "You see a little bottle with some liquid inside.",
        'grab_object': "You grab the potion.",
        'healing': 35,
        'mana_recover': 0
    },
    # Rooms 1, 10
    'mana_potion': {
        'name': "Mana Potion",
        'description': "a deep blue potion in an ornate bottle. This must've belonged to a mage at some point.",
        'found_object': "You see a little bottle with some liquid inside.",
        'grab_object': "You grab the potion.",
        'healing': 0,
        'mana_recover': 45
    }

}

# Talismans
talisman = {
    # Room 15
    'silver_key': {
        'name': "Silver Key",
        'description': "a large, ornate silver key decorated with strange sigils. On the bit, the an inscription reads\n"
                       "\"Randolph C.\"...A previous owner, perhaps?",
        'found_object': "You approach the pedestal, small flecks of cosmic energy seem to radiate off of the key.",
        'grab_object': "You pick up the key.",
        'stat_boost': 40
    },
    # Room 3
    'sun_talisman': {
        'name': "Sun Talisman",
        'description': "a small talisman depicting the sun.\n"
                       "It's craftsmanship is crude, but it fills you with a sense of vigor.",
        'found_object': "You see a curious talisman within the jaws of the Horror.",
        'grab_object': "You reach into the creature's mouth and withdraw the talisman.",
        'stat_boost': 15
    }
}
