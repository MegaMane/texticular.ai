from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *
import texticular.globals as g

if TYPE_CHECKING:
    from texticular.game_controller import Controller
    from texticular.game_object import GameObject


def action_room201(context: str = "M-ENTER") -> bool:
    room = g.CONTROLLER.player.location

    if g.GREAT_DANE_ENCOUNTERED:
        g.CONTROLLER.response.extend(["Room action for Bathroom Room 201 called!"])
        g.CONTROLLER.response.extend([f"visited Room 201 {g.CONTROLLER.player.location.times_visited} times"])
        room.exits[Directions.WEST].current_description = "GreatDane"
    return True

def action_bathroom_room201(context: str = "M-ENTER") -> bool:
    g.GREAT_DANE_ENCOUNTERED = True
    g.CONTROLLER.response.extend(["Room action for Bathroom Room 201 called!"])
    g.CONTROLLER.response.extend([f"visited the bathroom {g.CONTROLLER.player.location.times_visited} times"])
    return True

