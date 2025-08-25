KNOWN_VERBS = [
    "look",
    "examine",  # Add examine verb
    "search",   # Add search verb
    "walk",
    "go", 
    "move",
    "get",
    "take",
    "pickup",   # Add pickup verb
    "drop",
    "open",
    "close",
    "put",
    "use",
    "turn on",  # Add turn on verb
    "turn off", # Add turn off verb
    "sit",  # Add sit verb
    "stand",    # Add stand verb
    "get up",   # Add get up verb
    "talk",  # Add talk verb for NPCs
    "speak", # Add speak as alias for talk
    "inventory",
    "i",  # Add inventory shortcut
    "wipe",
    "wipe off",
    "rub"  # Add rub verb for genie
]

SINGLE_VERB_COMMANDS = [
    "get up",
    "help",
    "inventory",
    "look",
    "quit",
    "save"
]


PREPOSITIONS = [
    "in",
    "on",
    "at",
    "from"
    # "inside"
    # through, up, under, over, beside, below, down ...{the apple}
]




# Player State
GREAT_DANE_ENCOUNTERED = False
HAS_POOPED = False
PLAYERSITTING = False