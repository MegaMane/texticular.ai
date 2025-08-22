from itertools import count
from texticular.game_enums import Flags
import functools
import json


class GameObject:
    """A Base Class representing a generic game object

    Provides some basic functionality for commands that can be used on all objects (i.e. Look and Examine).
    As well as a class level dictionary that keeps track of all game objects that are instantiated.

    Attributes
    ----------
    objects_by_key: dict
        A class level dictionary that keeps track of all the game objects created
        key_value >> GameObject
    id: int
        A globally unique integer ID assigned to each item that is created
    name: str
        The friendly object name (does not have to be unique)
   descriptions: dict
        A dictionary of descriptions for the object that can change based on events in the game
        At the very least should contain  {"Main": "Some Object Description"}
    current_description: str
        The description of the game object
    key_value: str
        The globally unique string identifier for an object, should contain no spaces

    Methods
    ---------
    __init__()
        The constructor for the GameObject Class

    """

    _objectid = count(1)
    objects_by_key = {}

    @classmethod
    def lookup_by_key(cls, key_value:str):
        return cls.objects_by_key .get(key_value)


    def __init__(self, key_value: str, name: str, descriptions: dict, location_key: str = None, flags: list = None):
        """The constructor for the GameObject Class

        Parameters
        ----------
        key_value: str
            The Unique Game-wide Identifier for an object
        name: str
            The friendly object name (does not have to be unique)
        descriptions: dict
            A dictionary of descriptions for the object that can change based on events in the game
            At the very least should contain  {"Main": "Some Object Description"}
        location_key: str
            The object key_value where the exit is located
        flags: list
            a list of "Flags" enum members to define attributes of an object to be used by game logic
        """
        self.id = next(GameObject._objectid)
        self.name = name

        if "Main" not in descriptions:
            raise KeyError("In addition to other descriptions, the  descriptions dict must contain at "
                           "least the 'Main' key with a description")

        self.descriptions = descriptions
        self.location_key = location_key
        self.flags = set()
        self.action_method_name = None

        if flags is None:
            flags = []
        for flag in flags:
            self.add_flag(flag)

        self._current_description = "Main"

        if descriptions.get("Examine"):
            self._examine_description = "Examine"
        else:
            self._examine_description = "Main"

        duplicate_object = GameObject.lookup_by_key(key_value)
        if duplicate_object:
            raise ValueError(f"Each game object must have a unique key value. {key_value} already exists on "
                             f"Object: {duplicate_object.name}:"
                             f" {duplicate_object.key_value}")
        else:
            self.key_value = key_value
            GameObject.objects_by_key[key_value] = self

    def __str__(self):
        return str(vars(self))

    @property
    def current_description(self):
        return self._current_description
    @current_description.setter
    def current_description(self, descript_key):
        if self.descriptions.get(descript_key):
            self._current_description = descript_key
        else:
            raise KeyError(f"Key {descript_key} not found in descriptions.")

    @property
    def examine_description(self):
        return self._examine_description
    @examine_description.setter
    def examine_description(self, descript_key):
        if self.descriptions.get(descript_key):
            self._examine_description = descript_key
        else:
            raise KeyError(f"Key {descript_key} not found in descriptions.")

    def describe(self) -> str:
        """Return the current description of the game object

        Returns
        -------
        str
            the current description of the game object
        """
        return self.descriptions[self.current_description]

    def examine(self) -> str:
        """Return the more detailed description of the game object

        Returns
        -------
        str
            A more detailed description of the game object if one is available
        """
        return self.descriptions[self.examine_description]

    def move(self, location_key:str):
        """Puts object1 into object2.
         Example:
             bread.move("toaster")
         """
        if GameObject.lookup_by_key(location_key):
            self.location_key = location_key
        else:
            raise ValueError(f"Invalid location Key provided {location_key}")

    def remove(self):
        """Remove the object from the game setting its location to "nowhereLand"

        A special room that contains all consumed or unreachable story objects

         Examples
         ----------
         >>> skeleton_key.remove()
         >>> print(skeleton_key.location_key)
         nowhereLand

         """
        self.location_key = "nowhereLand"
    def has_flag(self, flag: Flags):
        return flag in self.flags
    def add_flag(self, flag: Flags):
        self.flags.add(flag)


    def add_flag_by_name(self, flag:str):
        """Attempt to add a flag attribute to a game object if it is a valid member of the Flags Enum.

        Parameters
        ----------
        flag:str
            The flag to be added to the game object
        """
        flags = [member.name for member in Flags]
        if flag in flags:
            self.flags.add(Flags[flag])
        else:
            raise ValueError(f"Flag {flag} does not exist in game_enums.Flags.")

    def remove_flag(self, flag: Flags):
        try:
            self.flags.remove(flag)
            return True
        except KeyError:
            return False
    def remove_flag_by_name(self, flag:str) -> bool:
        """Remove a flag enum attribute from the game object if it is found in the flags set else return false

        Parameters
        ----------
        flag:Flags
            The flag to be removed from the game object

        """
        try:
            self.flags.remove(Flags[flag])
            return True
        except KeyError:
            return False


    def action(self, func):
        @functools.wraps(func)
        def wrapper_action(*args, **kwargs):
            results = func(*args, **kwargs)
            return results
        return wrapper_action

    def encode_tojson(self,o):
        """Serialize Game Object to Json

        """
        return {
            "type": self.__class__.__name__,
            "keyValue": self.key_value,
            "locationKey": self.location_key,
            "name": self.name,
            "currentDescription": self._current_description,
            "examineDescription": self._examine_description,
            "descriptions": self.descriptions,
            "flags": [flag.name for flag in self.flags],
            "actionMethod": self.action_method_name
        }

if __name__ == "__main__":
    game_object = GameObject(key_value="office_lock",
                             name="lock",
                             descriptions={
                                 "Main": "A little grey padlock",
                                 "Examine": "It's full of tiny little ridges, dings, and dents.",
                                 "Description-GummedUp": "The lock has a piece of gum jammed in it, no key will open it now.",
                                 "Examine-Discover": "Etched at the bottom of the lock is a faint 4 digit code. It reads 8745."
                             }
                             )
    print(game_object)

    game_object.add_flag_by_name("LOCKEDBIT")
    assert Flags.LOCKEDBIT in game_object.flags

    def custom_action(controller, target: GameObject = game_object, additional_arg="Extra"):
        target.action_method_name = "custom_action"
        if controller.lower() == "open":
            target.remove_flag_by_name("LOCKEDBIT")
            print(additional_arg)
            return True
        return False

    def encode_game_object(o):
        if isinstance(o, GameObject):
            return {"name": o.name}

    game_object.action = game_object.action(custom_action)

    game_object.action(controller="Open")

    assert Flags.LOCKEDBIT not in game_object.flags
    game_object.add_flag_by_name("TAKEBIT")

    print(json.dumps(game_object, indent=4, default=game_object.encode_tojson))
