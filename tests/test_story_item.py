from texticular.items.story_item import StoryItem
from texticular.game_enums import Flags
from texticular.game_object import GameObject


def test_story_item():
    assert StoryItem(
        key_value="Twinkie",
        name="Master Twinkie",
        location_key="nowhereLand",
        descriptions={"Main": "The Twinkie that opens every door"},
        synonyms=["Bad Mother Fuckin' TwinKey"],
        flags=[Flags.KLUDGEBIT]
    )
