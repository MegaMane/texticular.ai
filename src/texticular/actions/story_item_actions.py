from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *

if TYPE_CHECKING:
    from texticular.game_controller import Controller
    from texticular.game_object import GameObject


def action_room201_nightStand(controller: Controller, target: GameObject) -> bool:
    if controller.tokens.action == "open":
        # Redirect from the prop to the actual container then call the stock open method
        drawer = controller.get_game_object("room201-nightStand-drawer")
        controller.tokens.direct_object = drawer
        controller.tokens.direct_object_key = drawer.key_value
        return controller.commands["open"](controller)
    return False

def action_room201_purpleHandPrints(controller: Controller, target: GameObject) -> bool:
    if controller.tokens.action == "wipe" or controller.tokens.action == "wipe off":
        controller.response.append("Try as you might the hand prints are here to stay.")
        return True
    return False



def action_room201_couch(controller: Controller, target: GameObject) -> bool:
    tokens = controller.tokens
    couch = target
    if tokens.verb == "sit":
        couch.current_description = couch.descriptions["Sitting"]
        controller.response.append("You sit on the couch.")
        controller.response.extend(controller.player.go_to(couch.key_value))
        return True
    elif tokens.verb in ["stand", "get off", "get up"]:
        couch.current_description = couch.descriptions["Main"]
        controller.response.append("You get off the couch.")
        controller.response.extend(controller.player.go_to(couch.location_key))
        return True
    return False