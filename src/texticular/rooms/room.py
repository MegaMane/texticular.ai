from texticular.game_object import GameObject
from texticular.game_enums import Flags, Directions
from texticular.rooms.exit import RoomExit


class Room(GameObject):
    """A Class representing a room, the main building black of the game

    Attributes
    ----------
    key_value: str
        The globally unique string identifier for an object, should contain no spaces
    name: str
        The friendly object for the room (does not have to be unique)
    descriptions: dict
        A dictionary of descriptions for the Room that can change based on events in the game
        At the very least should contain  {"Main": "Some Room Description"}
    exits: dict
        dictionary with "Directions" enum as the key and an Exit object as the value
    items: list
        A list of interactable items in the  room
    npcs: list
        A list of the npcs that are present in the room

    Methods
    ---------
    __init__()
        The constructor for the Room Class

    """
    room_count = 0

    def __init__(self, key_value: str, name: str, descriptions: dict, location_key="Map", flags=None):
        self.times_visited = 0
        self.items = []
        self.exits = {}
        self.npcs = []
        super().__init__(key_value, name, descriptions, location_key, flags)
        Room.room_count += 1

    def add_exit(self, direction:Directions, exit: RoomExit):
        if direction in [Directions.NORTH, Directions.NORTHEAST, Directions.EAST,
                         Directions.SOUTHEAST, Directions.SOUTH, Directions.SOUTHWEST,
                         Directions.WEST, Directions.NORTHWEST]:
            self.exits[direction] = exit
        else:
            raise KeyError("Please use one of the Cardinal directions found in the DIRECTIONS "
                           "ENUM as a key i.e NORTH, EAST, SOUTHWEST ETC.")

    def remove_exit(self, direction:Directions, exit: RoomExit):
        exit.location_key = "NOWHERE-LAND"
        self.exits[direction] = None

    def remove_item(self, item:GameObject):
        """Remove an item from any 'item' collections in the current room or from any containers inside the room

        """

        containers = [container for container in self.items if Flags.CONTAINERBIT in container.flags]
        for container in containers:
            if item in container.items:
                container.remove_item(item)
                return True

        if item in self.items:
            self.items.remove(item)  # pull the item out of the room "items" array
            item.remove()  # set its location to "nowhereLand"
        return True

    def describe(self) -> list:
        """Return a list containing the desciption of everything relevant in the current room

        This includes the room description itself and all items,exits, and npcs visible to the player.
        Takeable items will be appended to the end of the rooms fixed description before the exits

        Returns
        -------
        str
            The main description for the room

        """
        main_description = ''
        response = []
        main_description += f"You are in the {self.name}: {super().describe()}"
        main_description += self.get_takeable_item_descriptions()
        main_description += self.get_exit_descriptions()
        response.append(main_description)
        response.append("\n\n---Exits---\n\n")
        response.extend(self.list_exits())
        return response

    def get_exit_descriptions(self) -> str:
        """Loop through the exit keys and return each exits description

         Concat the descriptions and their cardinal direction positions to return to the describe method

        Returns
        -------
        str
            A string containing a listing of all the exits in the current room and where they are located

        """
        response = ''
        for exit_direction in self.exits.keys():
            exit_description = self.exits[exit_direction].describe()
            response += (f" To the {exit_direction.name} {exit_description}")
        return response


    def list_exits(self) -> str:
        response = []
        for exit_direction in self.exits.keys():
            exit_description = f"{self.exits[exit_direction].name} : {self.exits[exit_direction].describe()}"
            response.append(f"To the {exit_direction.name} is the {exit_description}\n")
        return response

    def get_takeable_item_descriptions(self):
        """Append the descriptions of all the takeable items to the room description"""
        response = ''
        for item in self.items:
            if Flags.TAKEBIT in item.flags:
                response += " " + item.describe()
        return response

    def get_npcs(self):
        pass

    def encode_tojson(self,o):
        """Serialize Room Object to Json

        """
        exit_dict = {}
        for exit_direction in self.exits.keys():
            exit_dict[exit_direction.name] = self.exits[exit_direction].encode_tojson(None)

        item_dict = {}


        return {
            "type": self.__class__.__name__,
            "keyValue": self.key_value,
            "locationKey": self.location_key,
            "name": self.name,
            "currentDescription": self._current_description,
            "examineDescription": self._examine_description,
            "descriptions": self.descriptions,
            "flags": [flag.name for flag in self.flags],
            "actionMethod": self.action_method_name,
            "timesVisited": self.times_visited,
            "exits": exit_dict,
            "itemKeyValues": [item.key_value for item in self.items],
            "npcs": self.npcs
        }


if __name__ == "__main__":
    import textwrap
    import json
    room_201 = Room(key_value="room201",
                    name="Room 201",
                    descriptions={"Main":("As you look around the hotel room you see an old TV with "
                                          "rabbit ears that looks like it came straight out of the 1950's. Against the "
                                          "wall there is a beat up night stand with a little drawer built into it and an"
                                          " old phone on top. Next to it is a lumpy old bed that looks like it's seen "
                                          "better days, with a dark brown stain on the sheets and a funny smell coming "
                                          "from it. There is an obnoxious orange couch in the corner next to a small "
                                          "window smudged with sticky purple hand prints. The stuffing is coming out of"
                                          " the cushions which are also spotted with purple, and the floor is covered "
                                          "with cans of Fast Eddie's Colon Cleanse.")
                                  },
                    flags=[Flags.CONTAINERBIT, Flags.ONBIT]
                    )
    room_201.add_exit(Directions.WEST,
                                        RoomExit(
                                                 key_value="exits-room201-bathroom",
                                                 name="Bathroom Door",
                                                 descriptions={
                                                     "Main": "is the DOOR to that sweet sweet porcelain throne.",
                                                     "GreatDane": "is the DOOR to a fucked up killer version of Scooby-Doo (and He's hungry)!"
                                                 },
                                                 location_key="room201",
                                                 connection="bathroom-room201",
                                                 flags=[Flags.DOORBIT, Flags.OPENBIT]
                                                 )
                      )
    room_201.add_exit(Directions.EAST,
                                        RoomExit(
                                                 key_value="exits-room201-hallway",
                                                 name="Hallway Door",
                                                 descriptions={
                                                     "Main": "the DOOR leads outside to the hallway...where hopefully there are toilets."
                                                 },
                                                 location_key="room201",
                                                 connection="westHallway-2f",
                                                 flags=[Flags.DOORBIT, Flags.OPENBIT]
                                                 )
                      )


    print("\n".join(textwrap.wrap(room_201.describe(), width=150, replace_whitespace=False)))

    print(json.dumps(room_201, indent=4, default=room_201.encode_tojson))



