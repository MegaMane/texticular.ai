from texticular.game_object import GameObject
from texticular.game_enums import Flags
class StoryItem(GameObject):
    def __init__(self, key_value: str, name: str, descriptions: dict, synonyms: list,
                 adjectives: list = None, size: int = 1, location_key: str = None, flags: list = None):
        self.synonyms = synonyms
        self.adjectives = adjectives
        self.size = size

        if adjectives is None:
            self.adjectives = []

        self.descriptive_name = (" ".join(self.adjectives) + " " + name).strip()

        super().__init__(key_value, name, descriptions, location_key, flags)

    def encode_tojson(self, o):
        """Serialize Story Item to Json

        """

        return {
            "type": self.__class__.__name__,
            "keyValue": self.key_value,
            "locationKey": self.location_key,
            "name": self.name,
            "synonyms": self.synonyms,
            "adjectives": self.adjectives,
            "currentDescription": self._current_description,
            "examineDescription": self._examine_description,
            "descriptions": self.descriptions,
            "size": self.size,
            "flags": [flag.name for flag in self.flags],
            "actionMethod": self.action_method_name
        }

    def is_present(self, room) -> bool:
        """Check if the item is present in the provided location or
         any open containers in the provided location and visible

        Parameters
        ----------
        room: Room
            The room to search for the item
        """
        open_containers = [container for container in room.items if
                           Flags.CONTAINERBIT in container.flags and Flags.OPENBIT in container.flags]

        item_in_open_container = False
        for container in open_containers:
            if self in container.items:
                item_in_open_container = True
                break

        return (self.location_key == room.key_value and Flags.INVISIBLE not in self.flags or
                item_in_open_container )

class Container(StoryItem):
    def __init__(self, key_value: str, name: str, descriptions: dict, synonyms: list, adjectives: list = None,
                 slots: int = 10, location_key: str = None, key_object=None, flags: list = [Flags.CONTAINERBIT]):
        super().__init__(key_value, name, descriptions, synonyms, adjectives, size=99,
                         location_key=location_key, flags=flags)
        self.slots = slots
        self.slots_occupied = 0
        self.key_object = key_object
        self.items = []

    def check_item_fits_inside(self, item: StoryItem):
        return item.size + self.slots_occupied <= self.slots

    def add_item(self, item: StoryItem) -> bool:
        self.slots_occupied += item.size
        self.items.append(item)
        item.move(self.key_value)
        return True


    def remove_item(self, item: StoryItem) -> bool:
        if item in self.items:
            self.slots_occupied -= item.size
            self.items.remove(item)
            item.remove()
            return True
        return False

    def open(self, key_object=None):
        if Flags.LOCKEDBIT in self.flags:
            if key_object is None:
                return False
            if key_object.key_value != self.key_object:
                return False
            else:
                key_object.location_key = self.key_value
        self.add_flag(Flags.OPENBIT)
        return True

    def close(self):
        if Flags.OPENBIT not in self.flags:
            return False
        self.remove_flag(Flags.OPENBIT)
        return True

    def look_inside(self) -> str:
        response = []
        response.append(f"You look inside the {self.descriptive_name} and see...\n")
        response.append(("-" * len(response[0])) + "\n\n")

        if self.items:
            for item in self.items:
                response.append(f"{item.descriptive_name}: {item.describe()}")
        else:
            response.append(f"Nothing. It's empty.")

        return response

    def encode_tojson(self, o):
        """Serialize Container Item to Json

        """

        return {
            "type": self.__class__.__name__,
            "keyValue": self.key_value,
            "locationKey": self.location_key,
            "name": self.name,
            "synonyms": self.synonyms,
            "adjectives": self.adjectives,
            "currentDescription": self._current_description,
            "examineDescription": self._examine_description,
            "descriptions": self.descriptions,
            "slots": self.slots,
            "size": self.size,
            "keyObject": self.key_object,
            "itemKeyValues": [item.key_value for item in self.items],
            "flags": [flag.name for flag in self.flags],
            "actionMethod": self.action_method_name
        }

class Inventory(Container):
    def __init__(self, key_value: str, name: str, descriptions: dict, synonyms: list, adjectives: list = None,
                 slots: int = 10, location_key: str = None, flags: list = [Flags.CONTAINERBIT, Flags.OPENBIT]):
        super().__init__(key_value, name, descriptions, synonyms, adjectives,
                         slots, location_key, key_object=None, flags=flags)

    def look_inside(self) -> str:
        response = []
        response.append(f"{self.name}: {super().describe()}\n")
        response.append(("-" * (len(self.name) + len(super().describe()) + 2)) + "\n\n")
        if self.items:
            for item in self.items:
                response.append(f"{item.descriptive_name}: {item.describe()}")
        else:
            response.append(f"Nothing. It's empty.")

        return response

if __name__ == "__main__":
    import json

    nightStand = Container(
        key_value="room201-nightStand",
        name="Stand",
        descriptions={"Main": "A beat up night stand with a little drawer built into it and black rotary phone on top"},
        synonyms=["Table"],
        adjectives=["Beat Up", "Night"],
        location_key="room201",
        flags=[Flags.CONTAINERBIT, Flags.SETPIECEBIT]
    )

    earplugs = StoryItem(
        key_value="room201-earPlugs",
        name="Ear Plugs",
        location_key="room201-nightStand",
        descriptions={"Main": "Some well loved yellow ear plugs, they smell kinda funky but they still work."},
        synonyms=["Plugs"],
        adjectives=["Crusty", "Yellow"],
        flags=[Flags.TAKEBIT]

    )

    nightStand.add_item(earplugs)

    print(json.dumps(nightStand, indent=4, default=nightStand.encode_tojson))

