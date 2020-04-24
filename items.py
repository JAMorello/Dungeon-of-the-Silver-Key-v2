import json

# Load all the items data
with open('data/book.json', 'r') as file:
    book = json.load(file)
with open('data/potion.json', 'r') as file:
    potion = json.load(file)
with open('data/talisman.json', 'r') as file:
    talisman = json.load(file)


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
