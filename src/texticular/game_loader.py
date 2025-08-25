"""responsible for loading and saving game objects to and from json"""

import json
import os
from pathlib import Path
import texticular.actions.story_item_actions as story_item_actions
import texticular.actions.room_actions as room_actions
from texticular.game_object import GameObject
from texticular.game_enums import Flags, Directions
from texticular.items.story_item import StoryItem, Inventory, Container
from texticular.items.vending_machine import VendingMachine
from texticular.rooms.room import Room
from texticular.rooms.exit import  RoomExit
from texticular.character import Player, NPC
import inspect


def get_data_path():
    """Get the absolute path to the data directory, regardless of where the script is run from."""
    # First try to find data directory relative to current working directory (development mode)
    cwd_data_path = Path.cwd() / "data"
    if cwd_data_path.exists():
        return str(cwd_data_path)
    
    # If not found, try relative to this file (for installed package)
    current_file = Path(__file__).resolve()
    # Navigate up to project root and into data folder
    project_root = current_file.parent.parent.parent  # from src/texticular/game_loader.py to project root
    data_path = project_root / "data"
    
    # If that doesn't exist either, try a few more common locations
    if not data_path.exists():
        # Try in the same directory as the package
        package_data_path = current_file.parent / "data"
        if package_data_path.exists():
            return str(package_data_path)
    
    return str(data_path)


def encode_to_json(game_objects: dict, save_file_name: str, root_element_name: str):
    """
    Serialize a dictionary of game objects to a Json File. Used for saving game state.

    Parameters
    ----------
    game_objects: dict
        A dictionary of game objects where keys are identifiers and values are GameObject instances.
    save_file_name: str
        The file name where the JSON data will be saved. Files will be saved in the data directory
        relative path = ./../../data/
    root_element_name: str
        The name of the root element in the JSON structure.

    Returns
    -------
    None
    """
    json_objects = []
    json_document = {}
    for obj in game_objects.keys():
        json_objects.append(game_objects[obj].encode_tojson(game_objects[obj]))
        json_document [root_element_name] = json_objects
    with open(f"./../../data/{save_file_name}", "w") as jsonfile:
        json.dump(json_document, jsonfile, indent=4)


def load_json(json_file_path):
    with open(json_file_path) as json_file:
        config = json.load(json_file)
    return config

def generate_game_object_flags(flag_list=None):
    if flag_list is None:
        return []
    else:
        return [Flags[flag] for flag in flag_list]

def decode_container_fromjson(dct):
    if dct["keyValue"] == "player-inventory":
        constructed_container = Inventory(
            key_value=dct["keyValue"],
            location_key=dct["locationKey"],
            name=dct["name"],
            synonyms=dct["synonyms"],
            adjectives=dct["adjectives"],
            descriptions=dct["descriptions"],
            slots=dct["slots"],
            flags=generate_game_object_flags(dct["flags"])
        )
    else:
        constructed_container = Container(
            key_value=dct["keyValue"],
            location_key=dct["locationKey"],
            name=dct["name"],
            synonyms=dct["synonyms"],
            adjectives=dct["adjectives"],
            descriptions=dct["descriptions"],
            slots=dct["slots"],
            key_object=dct["keyObject"],
            flags=generate_game_object_flags(dct["flags"])
        )


    constructed_container.current_description = dct["currentDescription"]
    constructed_container.examine_description = dct["examineDescription"]
    constructed_container.action_method_name = dct["actionMethod"]

    #Add the items to the container
    for keyval in dct["itemKeyValues"]:
        constructed_container.add_item(GameObject.objects_by_key.get(keyval))

    return constructed_container


def decode_story_item_fromjson(dct):
    constructed_item = StoryItem(
        key_value=dct["keyValue"],
        location_key=dct["locationKey"],
        name=dct["name"],
        synonyms=dct["synonyms"],
        adjectives=dct["adjectives"],
        descriptions=dct["descriptions"],
        size=dct["size"],
        flags=generate_game_object_flags(dct["flags"])
    )

    constructed_item.current_description = dct["currentDescription"]
    constructed_item.examine_description = dct["examineDescription"]
    constructed_item.action_method_name = dct["actionMethod"]

    return constructed_item


def decode_vending_machine_fromjson(dct):
    """Decode VendingMachine from JSON configuration."""
    constructed_machine = VendingMachine(
        key_value=dct["keyValue"],
        name=dct["name"],
        descriptions=dct["descriptions"],
        location_key=dct["locationKey"],
        flags=generate_game_object_flags(dct["flags"]),
        synonyms=dct.get("synonyms", None),
        adjectives=dct.get("adjectives", None)
    )
    
    constructed_machine.current_description = dct["currentDescription"]
    constructed_machine.examine_description = dct["examineDescription"]
    constructed_machine.action_method_name = dct["actionMethod"]
    
    return constructed_machine


def decode_room_fromjson(dct):
    constructed_room = Room(
        key_value=dct["keyValue"],
        name=dct["name"],
        descriptions=dct["descriptions"],
        location_key="Map",
        flags=generate_game_object_flags(dct["flags"]),
    )

    constructed_room.current_description = dct["currentDescription"]
    constructed_room.examine_description = dct["examineDescription"]
    constructed_room.action_method_name = dct["actionMethod"]
    constructed_room.times_visited = dct["timesVisited"]
    constructed_room.exits = decode_room_exits_fromjson(dct["exits"])

    # Add the items to the room
    for keyval in dct["itemKeyValues"]:
        constructed_room.items.append(GameObject.objects_by_key.get(keyval))


    return constructed_room

def decode_room_exits_fromjson(dct):
    exits = {}
    for direction in dct.keys():
        constructed_exit = RoomExit(
            key_value=dct[direction]["keyValue"],
            name=dct[direction]["name"],
            descriptions=dct[direction]["descriptions"],
            location_key=dct[direction]["locationKey"],
            connection=dct[direction]["connection"],
            key_object=dct[direction]["keyObject"],
            flags=generate_game_object_flags(dct[direction]["flags"]),
        )

        constructed_exit.current_description = dct[direction]["currentDescription"]
        constructed_exit.examine_description = dct[direction]["examineDescription"]
        constructed_exit.action_method_name = dct[direction]["actionMethod"]

        exits[Directions[direction]] = constructed_exit

    return exits

def decode_character_from_json(dct):
    if dct["type"] == "Player":
        player_inventory = decode_container_fromjson(dct["inventory"])

        constructed_player = Player(
            key_value=dct["keyValue"],
            name=dct["name"],
            descriptions=dct["descriptions"],
            sex = dct["sex"],
            location_key=dct["locationKey"],
            flags=generate_game_object_flags(dct["flags"]),
            inventory=player_inventory
        )

        return constructed_player
    elif dct["type"] == "NPC":
        constructed_npc = NPC(
            key_value=dct["keyValue"],
            name=dct["name"],
            descriptions=dct["descriptions"],
            location_key=dct["locationKey"],
            flags=generate_game_object_flags(dct["flags"]),
            synonyms=dct.get("synonyms", []),
            adjectives=dct.get("adjectives", []),
            dialogue_file=dct.get("dialogueFile")
        )
        return constructed_npc
    else:
        raise NotImplementedError



def load_story_items(config_file_path):
    config = load_json(config_file_path)
    items = [item for item in config["items"] if item["type"] == "StoryItem"]
    vending_machines = [item for item in config["items"] if item["type"] == "VendingMachine"]
    
    storyitems = {}
    
    # Load regular story items
    for item in items:
        #print(json.dumps(item, indent=4))
        decoded_item = decode_story_item_fromjson(item)
        storyitems[decoded_item.key_value] = decoded_item
    
    # Load vending machines
    for machine in vending_machines:
        decoded_machine = decode_vending_machine_fromjson(machine)
        storyitems[decoded_machine.key_value] = decoded_machine
        
    return storyitems

def load_containers(config_file_path):
    config = load_json(config_file_path)
    storage_containers = [item for item in config["items"] if item["type"] == "Container"]
    containers = {}
    for container in storage_containers:
        #print(json.dumps(item, indent=4))
        decoded_container = decode_container_fromjson(container)
        #add_item_reference_to_room(gamemap, decoded_item)
        containers[decoded_container.key_value] = decoded_container
    return containers

def load_characters(config_file_path):
    config = load_json(config_file_path)
    game_characters = config["characters"]
    characters = {}
    for character in game_characters:
        decoded_character  = decode_character_from_json(character)
        characters[decoded_character.key_value] = decoded_character
    return characters


def load_game_rooms(config_file_path):
    config = load_json(config_file_path)
    rooms = {}
    for room in config["rooms"]:
        decoded_room = decode_room_fromjson(room)
        rooms[decoded_room.key_value] = decoded_room
    return rooms


def load_game_map(game_manifest, manifest_key="newGame"):
    # Handle both absolute and relative paths for game_manifest
    if not os.path.isabs(game_manifest):
        data_path = get_data_path()
        game_manifest = os.path.join(data_path, game_manifest)
    
    manifest = load_json(game_manifest)
    room_config = manifest[manifest_key]["roomConfig"]
    item_config = manifest[manifest_key]["itemConfig"]
    character_config = manifest["newGame"]["characterConfig"]

    data_path = get_data_path()
    gamemap = {}

    gamemap["items"] = load_story_items(os.path.join(data_path, item_config))
    gamemap["containers"] = load_containers(os.path.join(data_path, item_config))
    gamemap["rooms"] = load_game_rooms(os.path.join(data_path, room_config))
    gamemap["characters"] = load_characters(os.path.join(data_path, character_config))

    # Place items in their designated rooms
    place_items_in_rooms(gamemap)

    # No longer using dynamic binding - actions handled by direct dispatch
    return gamemap


def place_items_in_rooms(gamemap):
    """Place all loaded items into their designated rooms."""
    # Combine all item types
    all_items = {}
    all_items.update(gamemap["items"])
    all_items.update(gamemap["containers"])
    
    # Place each item in its designated room
    for item_key, item in all_items.items():
        if item.location_key and item.location_key in gamemap["rooms"]:
            target_room = gamemap["rooms"][item.location_key]
            target_room.items.append(item)

def wire_story_item_action_funcs():
    """Use the inspect module to return all of the functions in the item_actions module

    function names are identical to the key value of the object they belong to with two exceptions

    1. an 'action_' prefix is added on to the beginning of the function
    2. dashes from the key value are replaced with underscores because they are not allowed in function names

    example: The function action_room201_nightStand maps to the item with a key value of room201-nightStand

    Once the key_value: function mapping is built we loop through the dictionary keys and try to get any
    corresponding game items that match and then use eval to assign that function to the objects action method
    as well as write a reference to its name that will be saved when the object is serialized

    This seems like it might be some bad hacky shit, but it seems to work and it's pretty cool


    """
    func_names = [item[0] for item in inspect.getmembers(story_item_actions,predicate=inspect.isfunction)]
    key_values = [func_name.strip("action_").replace("_","-") for func_name in func_names]
    action_functions = dict(zip(key_values, func_names))

    for item in action_functions:
        item_to_wire = GameObject.objects_by_key.get(item)
        if item_to_wire:
            func_name = action_functions[item]
            custom_action = eval(f"story_item_actions.{func_name }")
            item_to_wire.action = item_to_wire.action(custom_action)
            item_to_wire.action_method_name = func_name


def wire_room_action_funcs():
    """Use the inspect module to return all of the functions in the item_actions module

    function names are identical to the key value of the object they belong to with two exceptions

    1. an 'action_' prefix is added on to the beginning of the function
    2. dashes from the key value are replaced with underscores because they are not allowed in function names

    example: The function action_room201_nightStand maps to the item with a key value of room201-nightStand

    Once the key_value: function mapping is built we loop through the dictionary keys and try to get any
    corresponding game items that match and then use eval to assign that function to the objects action method
    as well as write a reference to its name that will be saved when the object is serialized

    This seems like it might be some bad hacky shit, but it seems to work and it's pretty cool


    """
    func_names = [room[0] for room in inspect.getmembers(room_actions, predicate=inspect.isfunction)]
    key_values = [func_name.strip("action_").replace("_","-") for func_name in func_names]
    action_functions = dict(zip(key_values, func_names))

    for room in action_functions:
        room_to_wire = GameObject.objects_by_key.get(room)
        if room_to_wire:
            func_name = action_functions[room]
            custom_action = eval(f"room_actions.{func_name }")
            room_to_wire.action = room_to_wire.action(custom_action)
            room_to_wire.action_method_name = func_name







if __name__ ==  "__main__":
    print("YEllow")
    player = gamemap["characters"]["player"]
    #player.inventory.add_item(gamemap["items"]["room201-nightStand-lemon"])
    #print(json.dumps(player, indent=4, default=player.encode_tojson))



    #print(gamemap["containers"])

    save_state = True

    if save_state:
        characters = {}
        characters["player"] = GameObject.objects_by_key.get("player")
        encode_to_json(characters, "newGameCharacters.json", "characters")
        encode_to_json(game_objects=gamemap["rooms"], save_file_name="newGameMap.json", root_element_name="rooms")
        encode_to_json(game_objects={**gamemap["items"], **gamemap["containers"]}, save_file_name="newGameItems.json", root_element_name="items")
