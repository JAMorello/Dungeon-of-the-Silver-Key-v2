from random import choice
import json

# Load all the parser data
with open('data/parser.json', 'r') as file:
    parser_data = json.load(file)


def get_unknown_cmd():
    return choice(parser_data['UNKNOWN_CMD_RESPONSE'])


def remove_prepositions(sentence):
    words = sentence.split()
    result = list()
    for word in words:
        if word not in parser_data['PREPOSITIONS']:
            result.append(word)
    return result


def parse_sentence(sentence):
    """Parses the sentence and returns a verb and the two objects (if applicable)"""
    elements = remove_prepositions(sentence)
    verb = elements[0]
    direct_object = None
    indirect_object = None
    elements = elements[1:]

    if len(elements) >= 1:
        direct_object = elements[0]

    if len(elements) >= 2:
        indirect_object = elements[1]

    return verb, direct_object, indirect_object


def is_direction(word):
    return True if word in parser_data['DIRECTIONS'] else False


def parse_action(data_base, action):
    if not action:
        return
    actions = action.split(';')
    for each in actions:
        components = each.split()

        # if each.startswith('unblock'):
        #     data_base.unblock(components[1])
        #
        # elif each.startswith('increment'):
        #     data_base.increment(components[1])
        #
        # elif each.startswith('remove'):
        #     data_base.remove(components[1])
        #
        # elif each.startswith('create'):
        #     data_base.to_inv(components[1])
        #
        # elif each.startswith('state'):
        #     try:
        #         data_base.setState(components[1], int(components[2]))
        #     except ValueError:
        #         continue


def handle(data_base, verb, dir_object=None, ind_object=None):
    # Handles a verb-only sentence
    if not dir_object and not ind_object:
        return None

    # Check verbs, results, and actions on parser.json
    # verb = data_base.check_verb(verb)
    # result = data_base.getResult(dir_object, ind_object, verb)
    # action = data_base.getAction(dir_object, ind_object, verb)

    # parse_action(data_base, action)
    # return result

# Functions relative to parser:
    # PROMPT = '>> '
    # check_verb(): return none if "". If not, check verbonyms
    # clear_synonyms(): takes user input and check in each value of each key on parser.json "SYNONYMS" and takes key if True
    #                   Synonyms of objects and verbs
    # combine() --> check dumped .json; also return something if cant do
    # default() --> for unrecognized commands: parse sentence and handle; if not, unknow cmd

# parser.json
    # combine: verb/obj1/ob2 dict as
    #                               "verb": {
    #                                       "obj1": {
    #                                               "obj2": x,
    #                                               "result": y}}

# Functions relative to game in general:
    # do_move()
    # do_look(): in general ("look"); to object, to room, to direction (cleaner())
    # do_examine(): ("examine") "Examine what?"; with obj, do_look(). ¿What if more info?
    # inventory: do not show if there isnt any item

# Functions relative to rooms:
    # get_room_name()
    # get_room_description()
    # get_near_room_description() --> In current room (more complex dict) or from dumped .json (only one line, but how?)
    # move_to_room()
    # get_room_contents()

# Functions relative to objects:
    # get_inventory()
    # look_at()
    # pick_up() --> a "movable or not" is missing; also, if person or not; if there isnt any, "There isnt any %"; sucess message
    # drop() --> implement; nothing to drop, "You dont have any %"; sucess message
