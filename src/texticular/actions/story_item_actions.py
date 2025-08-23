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
    if tokens.action == "sit":
        couch.current_description = "Sitting"
        controller.response.append("You sit on the couch.")
        controller.response.append(couch.describe())  # Show the sitting description
        return True
    elif tokens.action in ["stand", "get off", "get up"]:
        couch.current_description = "Main"
        controller.response.append("You get off the couch.")
        return True
    return False


def action_vending_machine_2f(controller: Controller, target: GameObject) -> bool:
    """Handle interactions with the Fast Eddie's Vending Machine."""
    from texticular.items.vending_machine import VendingMachine
    
    # Ensure we're working with a VendingMachine object
    if not isinstance(target, VendingMachine):
        controller.response.append("This doesn't seem to be a proper vending machine.")
        return False
    
    action = controller.tokens.action
    
    # Handle "use vending machine" command (both first time and while active)
    if action in ["use", "operate", "activate"]:
        if target.is_active:
            # Already active, treat as requesting menu
            controller.response.append("You're already using the vending machine.")
            controller.ui.set_menu(target.display_main_menu(), "Vending Machine")
            return True
        else:
            # Not active, start interaction
            result = target.interact(controller)
            # Set up persistent menu for Rich UI
            if target.is_active:
                controller.ui.display_vending_machine_menu(
                    target.responses["greeting"],
                    target.display_main_menu()
                )
            return result
    
    # Handle "look at vending machine" - show detailed description
    elif action == "look":
        controller.response.append(target.describe())
        if not target.is_active:
            controller.response.append("Type 'use vending machine' to start shopping!")
        else:
            controller.response.append(target.display_main_menu())
        return True
    
    # Default responses for inactive machine
    else:
        responses = [
            "The vending machine sits silently. Maybe try using it?",
            "The machine's display shows 'INSERT COIN TO CONTINUE'",
            "You can't do that with the vending machine. Try 'use vending machine'."
        ]
        controller.response.append(responses[0])
        return True