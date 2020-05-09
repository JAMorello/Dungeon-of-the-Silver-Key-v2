from random import choice
import json

# Load all the parser data
with open('data/parser.json', 'r') as file:
    parser_data = json.load(file)


def get_unknown_cmd():
    print(choice(parser_data['UNKNOWN_CMD_RESPONSE']))


def remove_prepositions_adjectives(list_words):
    result = list()
    for word in list_words:
        if word not in parser_data['PREPOSITIONS'] and word not in parser_data['ADJECTIVES']:
            result.append(word)
    return result


def check_synonyms(list_words):
    true_words = list()
    for word in list_words:
        for key in parser_data['SYNONYMS']:
            if word in parser_data['SYNONYMS'][key]:
                true_words.append(key)
    if len(true_words) < len(list_words):
        get_unknown_cmd()
        return None
    return true_words


def check_verb(list_words):
    if list_words[0] not in parser_data["VERBS"]:
        get_unknown_cmd()
        return None
    return list_words


def combine(verb, dir_object, ind_object):
    for word in parser_data['COMBINE']:
        print("lOl")
        if word == verb:
            for obj in parser_data['COMBINE'][verb]:
                if obj == dir_object:
                    for obj2 in parser_data['COMBINE'][verb][dir_object]:
                        if obj2 == ind_object:
                            return parser_data['COMBINE'][verb][dir_object][ind_object]
    get_unknown_cmd()
    return None


def handle_command(verb, dir_object=None, ind_object=None):
    # Handles a verb-only sentence
    if not dir_object and not ind_object:
        return [verb], None  # Is an ACTION

    if verb and dir_object and not ind_object:
        return [verb, dir_object], None  # Is an ACTION

    result = combine(verb, dir_object, ind_object)  # Has a RESULT
    return None, result


def parse_command():
    """Parses the sentence and returns a verb and the two objects (if applicable)"""
    command, true_command = "", ""
    while not command:
        command = input(">> ").lower().split()
        if command:
            clean_command = remove_prepositions_adjectives(command)
            cleaner_command = check_synonyms(clean_command)
            if cleaner_command:
                true_command = check_verb(cleaner_command)

        if not true_command:
            command = ""

        if command:
            verb = true_command[0]
            try:
                direct_object = true_command[1]
            except:
                direct_object = None
            try:
                indirect_object = true_command[2]
            except:
                indirect_object = None

    action, result = handle_command(verb, direct_object, indirect_object)
    return action, result


print(parse_command())
