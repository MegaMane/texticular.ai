from texticular.game_object import GameObject
from texticular.game_enums import Flags

class RoomExit(GameObject):
    """A Class representing an exit. Connects one Room to another but only one way

    Meaning if you want a two-way exit (as they exist in the real world) that connects
    room A to B and B to A, you would need two instances of an RoomExit object by convention with key_values
    "exits-a-b" and "exits-b-a"

    """
    def __init__(self, key_value: str, name: str, descriptions: dict, location_key: str, connection: str,
                 key_object = None, flags=None):
        """The constructor for the Exit Class

        Parameters
        ----------
        key_value: str
            The globally unique string identifier for an object, should contain no spaces
        name: str
            The friendly object name (does not have to be unique)
        descriptions: dict
            A dictionary of descriptions for the object that can change based on events in the game
            At the very least should contain  {"Main": "Some Object Description"}
        location_key: str
            The object key_value where the exit is located
        connection: str
            The object key_value the exit leads to
        key_object: str
            The object key_value of the key for this exit (if any)
        flags: list
            a list of "Flags" enum members to define attributes of an object to be used by game logic
        """
        self.connection = connection
        self.key_object = key_object
        super().__init__(key_value, name, descriptions, location_key, flags)
        if self.key_object and Flags.LOCKEDBIT not in self.flags:
            self.add_flag(Flags.LOCKEDBIT)

    def encode_tojson(self,o):
        """Serialize Exit Object to Json

        """
        return {
            "type": self.__class__.__name__,
            "keyValue": self.key_value,
            "locationKey": self.location_key,
            "name": self.name,
            "connection": self.connection,
            "keyObject": self.key_object,
            "currentDescription": self._current_description,
            "examineDescription": self._examine_description,
            "descriptions": self.descriptions,
            "flags": [flag.name for flag in self.flags],
            "actionMethod": self.action_method_name,

        }
