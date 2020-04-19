from random import randint


class Enemy:
    def __init__(self, enemy_dict):
        self.name = enemy_dict['name']
        self.adjective = enemy_dict['adjective']
        self.description = enemy_dict['description']
        self.signature_move = enemy_dict['signature move']
        self.sanity_move = enemy_dict['sanity move']
        self.special_move = enemy_dict['special move']
        self.speed = enemy_dict['speed']
        self.health = enemy_dict['health']
        self.drop_chance = enemy_dict['drop chance']
        self.attacks = enemy_dict['attacks']

    def monster_appears(self, player):  # This method is used to announce the start of a non-boss fight
        print(self.adjective + self.name + " appears before you.\n" + self.description)
        print("It's speed is " + str(self.speed) + " and your speed is " + str(player.speed) + ".")


lesser_spawn = {
    'name': "Lesser Spawn",
    'adjective': "A malformed and hideous ",
    'description': "It's form is twisted and frail, it appears quite weak.",
    "signature move": "The Lesser Spawn gives a furious shriek and uses ",
    'sanity move': None,
    'special move': None,
    'speed': randint(1, 20),
    'health': 50,
    'drop chance': 5,
    'attacks': {"Slash": (5, 10),
                "Punch": (10, 15)}
}

clay_golem = {
    'name': "Clay Golem",
    'adjective': "A human sized ",
    'description': "It is a long abandoned construct of rogue cultists.",
    'signature move': "The Golem rears back and uses ",
    'sanity move': None,
    'special move': None,
    'speed': randint(1, 50),
    'health': 50,
    'drop chance': 5,
    'attacks': {"Smash": (10, 20),
                "Stomp": (10, 15)}
}

# Miniboss
dimensional_shambler = {
    'name': "Dimensional Shambler",
    'adjective': "A twisted ",
    'description': "It's body is twisted and ape-like, with wrinkled skin and sharp teeth. It's eyes see more than you "
                   "are to think of.",
    'signature move': "The Dimensional Shambler howls and uses ",
    'sanity move': "The Shambler affixes you with a hypnotic Gaze...",
    'special move': None,
    'speed': randint(30, 60),
    'health': 75,
    'drop chance': 5,
    'attacks': {"Claw": (20, 30),
                "Tear": (30, 35),
                "Unsettling Gaze": (30, 35),
                "[S] Hypnotic Gaze": 10}
}

# Miniboss
hunting_horror = {
    'name': "Hunting Horror",
    'adjective': "A snakelike ",
    'description': "It's body is snakelike and it's head is malformed. It's strange form is ever-changing.",
    'signature move': "The Hunting Horror hisses insidiously and uses ",
    'sanity move': "The Hunting Horror gives off a terrible aura...",
    'special move': None,
    'speed': randint(50, 75),
    'health': 75,
    'drop chance': 5,
    'attacks': {"Bite": (20, 30),
                "Snap": (30, 35),
                "Mutilate": (30, 35),
                "[S] Dread Aura": 10}
}

# Miniboss
flying_polyp = {
    'name': "Flying Polyp",
    'adjective': "A colossal, terrifying ",
    'description': "It is an ancient alien entity, momentarily disappearing from sight every now and again as it "
                   "angrily approaches you.",
    'signature move': "The Flying Polyp writhes hideously and uses ",
    'sanity move': "The Flying Polyp gives an unspeakable aura...",
    'special move': None,
    'speed': randint(30, 60),
    'health': 80,
    'drop chance': 5,
    'attacks': {"Cosmic Wind": (20, 30),
                "Tentacle Swipe": (30, 35),
                "Foul Affliction": (30, 35),
                "[S] Unnerving Aura": 15}
}

# Miniboss
shoggoth = {
    'name': "Shoggoth",
    'adjective': "A wandering ",
    'description': "It is a terrifying protoplasmic mass, an ancient servant of masters long forgotten",
    'signature move': "The Shoggoth roils angrily and uses ",
    'sanity move': "The Shoggoth fixes its multitude of eyes upon you...",
    'special move': None,
    'speed': randint(1, 50),
    'health': 100,
    'drop chance': 5,
    'attacks': {"Strangle": (20, 30),
                "Pummel": (30, 35),
                "Engulf": (30, 35),
                "[S] Unsettling Gaze": 10}
}

# Miniboss
moon_beast = {
    'name': "Moon-Beast",
    'adjective': "A pale, toad-like ",
    'description': "A foul stench emanates from this being",
    'signature move': "The Moon-Beast groans unsettlingly and uses ",
    'sanity move': "The Moon-Beast gives a horrific wail...",
    'special move': None,
    'speed': randint(1, 100),
    'health': 80,
    'drop chance': 5,
    'attacks': {"Claw": (20, 30),
                "Slash": (30, 40),
                "Eviscerate": (30, 35),
                "[S] Horrific Wail": 20}
}

# Boss
nyarlathotep = {
    'name': "Servant of The Nameless Mist",
    'adjective': "You are stricken with hopelessness. The unspeakable ",
    'description': "It is a being of immense and terrifying power",
    'signature move': "The Servant of the Nameless Mist uses ",
    'sanity move': "Your eyes are drawn to the endless abyss. You feel it gazing back...",
    'special move': "The servant casts a dreadful curse... you feel your life force being consumed...",
    'speed': int(200),
    'health': 125,
    'drop chance': 5,
    'attacks': {"[N] Curse of the Stars": (20, 25),
                "Eldritch Fire": (25, 30),
                "Cursed Blow": (35, 40),
                "Cosmic Vampirism": (20, 30),
                "[S] Gaze of the Abyss": 30}
}
