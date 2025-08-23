import re
from texticular.game_loader import load_game_map
from texticular.game_enums import Directions
from texticular.game_object import GameObject
from texticular.items.story_item import  StoryItem
from texticular.globals import *



class Parser:
    """A class responsible for attempting to parse player input into a known verb and optionally direct object & indirect object

     The parser splits player input on spaces or certain punctuation into words it then attempts to search the grammar
     for a known verb, remove articles and prepositions and then search the list of game objects for a direct and indirect
     object in the form:

     VERB_PHRASE DIRECT_OBJECT_PHRASE? INDIRECT_OBJECT_PHRASE?

    Attributes
    ----------
    actions: list
        the list of known verbs passed in to the parser at initialization
    prepositions: list
        hard coded list of prepositions to be used in identifying indirect objects
        Example: Get the lamp on the table
        ('the' is an article, 'on' is a preposition. Once the articles are removed,
        the indirect object appears directly after the preposition)


    Methods
    ---------
    tokenize(self, user_input: str, game_objects: dict):
        attempt to parse the player input and return a ParseTree object that contains the resulting parsed tokens
        or at the very least a ParseTree object that contains a response explaining why the input could not be parsed

    get_verb(parse_tree): Search for the Verb in the parsed tokens.

    get_possible_matches(synonyms, adjectives): Generate all possible combinations of synonyms and adjectives.

    parse_input(user_input): Parse the player input and create a ParseTree object with relevant information.
    """

    def __init__(self, game_objects: dict, known_verbs: list = KNOWN_VERBS):
        self.actions = known_verbs
        self.prepositions = PREPOSITIONS

        self.game_objects = {}
        for k, v in game_objects.items():
            if isinstance(v, StoryItem):
                self.game_objects [k] = self.get_possible_matches(v.synonyms, v.adjectives)
            else:
                self.game_objects [k] = [v.name.lower()]

    def tokenize(self, user_input: str):
        """
        Tokenize the user input into a list of parsed tokens.

        Args:
            user_input (str): The player's input string.

        Returns:
            ParseTree: A ParseTree object containing the parsed tokens.
        """
        parse_tree = ParseTree()
        parse_tree.unparsed_input = user_input
        # To split a string with multiple delimiters in Python, use the re.split() method.
        # The re.split() function splits the string by each occurrence of the pattern
        delimiters = "[\s,!\.\?]"
        parse_tree.tokens = re.split(delimiters, parse_tree.unparsed_input.lower())
        # split on the delimiters and remove any empty entries
        parse_tree.tokens  = [token.strip() for token in parse_tree.tokens if token]
        return parse_tree


    def get_verb(self, parse_tree):
        """
        Search for a recognized verb in the parsed tokens and update the ParseTree with the verb.

        Args:
            parse_tree (ParseTree): The ParseTree object containing the parsed tokens.

        Returns:
            int: The offset indicating where the verb was found in the tokens. Returns -1 if no verb is found.
        """
        offset = -1

        for index, part in enumerate(parse_tree.tokens):
            command_name = " ".join(parse_tree.tokens[0:index + 1])
            if command_name in self.actions:
                parse_tree.action = command_name
                offset = index + 1
        return offset

    def expand_adjectives(self, adjective_list):
        """
        Generate all possible combinations of adjectives given a list of adjectives containig 0-3 elements.

        Args:
            adjective_list (list): A list of adjectives to be combined max len = 3.

        Returns:
            list: A list containing individual adjectives and all possible combinations
                  of adjectives from the input list.

        Example:
            >>> input_array = ["Tiny", "Sour", "Yellow"]
            >>> result = expand_adjectives(input_array)
            >>> print(result)
            ['Sour', 'Sour Tiny', 'Sour Tiny Yellow', 'Sour Yellow', 'Sour Yellow Tiny', 'Tiny', 'Tiny Sour',
            'Tiny Sour Yellow', 'Tiny Yellow', 'Tiny Yellow Sour', 'Yellow', 'Yellow Sour',
            'Yellow Sour Tiny', 'Yellow Tiny', 'Yellow Tiny Sour']
        """
        combinations = []

        for i in range(len(adjective_list)):
            # Add individual adjective
            combinations.append(adjective_list[i])

            for j in range(i + 1, len(adjective_list)):
                # Combine with the next adjective
                combinations.append(f"{adjective_list[i]} {adjective_list[j]}")
                combinations.append(f"{adjective_list[j]} {adjective_list[i]}")

                for k in range(j + 1, len(adjective_list)):
                    # Combine with the next adjective again
                    combinations.append(f"{adjective_list[i]} {adjective_list[j]} {adjective_list[k]}")
                    combinations.append(f"{adjective_list[i]} {adjective_list[k]} {adjective_list[j]}")
                    combinations.append(f"{adjective_list[j]} {adjective_list[i]} {adjective_list[k]}")
                    combinations.append(f"{adjective_list[j]} {adjective_list[k]} {adjective_list[i]}")
                    combinations.append(f"{adjective_list[k]} {adjective_list[i]} {adjective_list[j]}")
                    combinations.append(f"{adjective_list[k]} {adjective_list[j]} {adjective_list[i]}")

        return sorted(combinations)

    def get_possible_matches(self, synonyms, adjectives):
        """
        Generate all possible combinations of synonyms and adjectives.

        Args:
            synonyms (list): A list of synonyms.
            adjectives (list): A list of adjectives.

        Returns:
            list: A list containing all possible combinations of adjectives and synonyms.

        Example:s
            >>> synonyms = ["Ear Plugs"]
            >>> adjectives = ["Crusty", "Yellow"]
            >>> matches = self.get_possible_matches(synonyms, adjectives)
            >>> print(matches)
            ['Crusty Ear Plugs', 'Crusty Yellow Ear Plugs', 'Yellow Ear Plugs', 'Yellow Crusty Ear Plugs']
        """
        expanded_adjectives = self.expand_adjectives(adjectives)
        if expanded_adjectives:
            matches = []
            for adj in expanded_adjectives:
                for syn in synonyms:
                    # Add spaced version (existing behavior)
                    matches.append(f'{adj} {syn}')
                    # Add concatenated version (new functionality)
                    concatenated = f'{adj}{syn}'.replace(' ', '')
                    matches.append(concatenated)
            matches.extend(synonyms)
        else:
            matches = synonyms
        return [m.lower() for m in matches]


    def find_game_object(self, remaining_input):
        for index, part in enumerate(remaining_input):
            object_name = " ".join(remaining_input[0:index + 1])
            # print(object_name)
            for object_key, possible_matches in self.game_objects.items():
                # print(possible_matches)
                if object_name.lower() in possible_matches:
                    return object_key


    def parse_game_objects(self, remaining_input, parse_tree):
        direct_objects = []
        secondary_objects = []

        # Find a preposition if it exists
        preps = [word for word in remaining_input if word in self.prepositions]
        preposition_count = len(preps)

        # bail out, syntax only allows for one preposition at this time
        if len(preps) > 1:
            return preposition_count

        if len(preps) == 1:
            # prepostion found
            preposition_index = remaining_input.index(preps[0])
            secondary_objects = remaining_input[preposition_index + 1:]
            direct_objects = remaining_input[0:preposition_index]

            if not direct_objects:
                direct_objects = secondary_objects
                secondary_objects = []
            # print(secondary_objects)
            # print(direct_objects)

        else:
            direct_objects = remaining_input

        parse_tree.direct_object_key = self.find_game_object(direct_objects)
        parse_tree.indirect_object_key = self.find_game_object(secondary_objects)

        return preposition_count

    def valid_direction(self, remaining_input: list, parse_tree):
        direction_name = "".join(remaining_input).upper()
        try:
            parse_tree.direct_object_key = Directions[direction_name]
        except KeyError:
            parse_tree.response = (f"{direction_name} is not a valid direction.")
            return False
        return True

    def parse_input(self, user_input):
        parse_tree = self.tokenize(user_input)
        if len(parse_tree.tokens) == 0:
            parse_tree.response = "Command is Empty"
            return parse_tree

        verb_offset = self.get_verb(parse_tree)
        if verb_offset == -1:
            # exit early command did not start with a known verb
            parse_tree.response = f'''Command: "{parse_tree.unparsed_input}" does not start with a known verb.'''
            return parse_tree

        # The rest of the input after the verb has been extracted
        # Remove articles
        remaining_input = [token for token in parse_tree.tokens[verb_offset:] if token not in ["a", "an", "the"]]

        preposition_count = self.parse_game_objects(remaining_input, parse_tree)

        if preposition_count > 1:
            # exit early shouldn't have more than one preposition in a command
            parse_tree.response = "I'm not smart enough to understand more than one preposition per command."
            return parse_tree

        if parse_tree.action and parse_tree.direct_object_key is None:

            remaining_input = [token for token in remaining_input if token not in self.prepositions]

            # check to see if the user is trying to move the player
            if parse_tree.action in ["go", "move", "walk"]:
                if self.valid_direction(remaining_input, parse_tree):
                    parse_tree.response = f"Player movement: {parse_tree.action} {repr(parse_tree.direct_object_key)}"
                    parse_tree.input_parsed = True
                    return parse_tree

            elif parse_tree.action in SINGLE_VERB_COMMANDS and (
                    len(remaining_input) == 0 or
                    parse_tree.action == 'look' and remaining_input[0] == 'room'
            ):
                parse_tree.response = f"Single verb command: {parse_tree.action}"
                parse_tree.input_parsed = True
                return parse_tree

            elif len(remaining_input) == 0 and parse_tree.action not in SINGLE_VERB_COMMANDS:
                parse_tree.response = f"{parse_tree.action} what?"
                parse_tree.input_parsed = True
                return parse_tree

            else:
                #a direct object wasn't found but the user attempted to provide one
                obj = ' '.join(remaining_input)
                article = 'an' if obj[0] in ['a', 'e', 'i', 'o', 'u'] else 'a'
                parse_tree.response = f"I don't see {article} {obj} here!"
                parse_tree.input_parsed = False
                return parse_tree

        parse_tree.input_parsed = True
        if not parse_tree.response:
            parse_tree.response = f"Command: <{parse_tree.unparsed_input}> parsed."
        return parse_tree



class ParseTree:
    """
    A class representing the parsed result of a player's input.

    Attributes:
        unparsed_input (str): The original unparsed player input.
        tokens (list): The parsed tokens of the player input.
        action (str): The recognized action (verb) from the input.
        direct_object_key: (str) The key of the direct object.
        indirect_object_key: (str) The key of the indirect object.
        input_parsed (bool): A flag indicating if the input was successfully parsed.
        response (str): A response explaining the parsing result.
    """
    def __init__(self):
        self.unparsed_input = None
        self.tokens = []
        self.action = None
        self.direct_object_key = None
        self.direct_object = None
        self.indirect_object_key = None
        self.indirect_object = None
        self.input_parsed = False
        self.response = None

    def __repr__(self):
        return f"""
        Parse Tree
        -----------
        unparsed_input: {self.unparsed_input}
        tokens: {str(self.tokens)}
        action: {self.action}
        direct_object_key: {self.direct_object_key}
        indirect_object_key:  {self.indirect_object_key}
        input_parsed: {str(self.input_parsed)}
        response = {self.response}
        """


if __name__ == "__main__":
    gamemap = load_game_map("./../../data/GameConfigManifest.json")
    parser = Parser(game_objects=GameObject.objects_by_key)


    parser_test_sentences = [
        "Look at the Night Stand",
        "Take the Ear Plugs",
        "Open Night Stand",
        "Look at the Little Wooden Drawer",
        "drink the chicken soup on the table.",
        "put the ear plugs in the Little Wooden Drawer",
        "Take The sour yellow Lemon",
        "Hey, Drop that candlestick!",
        "Go West",
        "Walk East",
        "Take note",
        "Inventory",
        "Open Inventory",
        "Open Backpack",
        "Drop Note",
        "look"
    ]

    for s in parser_test_sentences:
        parse_tree = parser.parse_input(s)
        print(parse_tree)



