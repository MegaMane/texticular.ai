from texticular.game_loader import load_game_rooms, load_story_items
from texticular.character import Player, Inventory
from texticular.game_object import GameObject
from texticular.game_enums import Directions, Flags
import pytest
import textwrap
from pytest import raises

def text_wrap(string_to_format):
    print("\n\n" + ("\n".join(textwrap.wrap(string_to_format, width=150, replace_whitespace=False))))

@pytest.fixture(scope="module")
def game_map():
    gamemap = load_game_rooms("../data/testMovementGameMap.json")
    load_story_items("../data/testItems.json")
    return gamemap

@pytest.fixture(scope="module")
def player():
    inventory = Inventory(
        key_value="player-inventory",
        name="Backpack",
        descriptions={"Main": "Your trusty black backpack."},
        location_key="Player"

    )
    player = Player(
        key_value="Player",
        name="Eagleberto",
        descriptions= {"Main": "An Angry nerd with dillusions of grandeur."},
        sex = "Male",
        location_key=("room201"),
        flags=[Flags.PLAYERBIT],
        inventory=inventory
    )

    return player




def test_can_move_player(player, game_map):
    text_wrap(GameObject.objects_by_key.get(player.location_key).describe())
    text_wrap(player.do_walk(Directions.WEST))
    assert player.location_key == "bathroom-room201"

def test_cant_move_player_past_locked_door(player, game_map):
    player.go_to("room201")
    # Start Room 201 Walk East >> West Hallway Walk North <> Room 203 (Locked)
    player.do_walk(Directions.EAST)
    text_wrap(player.do_walk(Directions.NORTH))
    assert player.location_key == 'westHallway-2f'







