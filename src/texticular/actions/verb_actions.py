# https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/
# https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *
from texticular.game_object import GameObject

if TYPE_CHECKING:
    from texticular.game_controller import Controller


def look(controller: Controller):
    if controller.tokens.direct_object:
        controller.response.append(controller.tokens.direct_object.describe())
    else:
        controller.response.extend(controller.player.location.describe())
    return True


def walk(controller: Controller):
    walk_direction = controller.tokens.direct_object_key
    controller.response.extend(controller.player.do_walk(walk_direction))
    return True


def take(controller: Controller):
    item = controller.tokens.direct_object
    inventory = controller.player.inventory

    if item in inventory.items:
        controller.response.append(f"You've already taken the {item.name}! Check your {inventory.name}")

    if item.is_present(controller.player.location):
        if Flags.TAKEBIT in item.flags:

            item_taken = inventory.add_item(item)
            if item_taken:
                controller.player.location.remove_item(item)
                item.move(inventory.location_key)
                item.current_description = "Main"
                controller.response.append("Taken.")
                return True
            else:
                controller.response.append((f"The  {item.name} won't fit in your {inventory.name}! "
                                            f"Try dropping something if you really want it."))
        else:
            controller.response.append(f"The {item.name} won't budge.")

        return False
    else:
        controller.response.append(f"You don't see a {item.name} here!")
        return False


def drop(controller: Controller):
    item = controller.tokens.direct_object
    inventory = controller.player.inventory
    if inventory.remove_item(item):
        item.move(controller.player.location_key)
        controller.player.location.items.append(item)
        item.current_description = "Dropped" if item.descriptions.get("Dropped") else "Main"
        controller.response.append("Dropped it like it's hot.")
        return True
    else:
        controller.response.append(f"You don't have a {item.name} to drop.")
        return False

def open(controller: Controller):
    target = controller.tokens.direct_object
    target_key = controller.get_game_object(target.key_object)
    player_inventory = controller.player.inventory.items

    if target_key in player_inventory:
        player_inventory.remove_item(target_key)
    else:
        target_key = None

    try:
        target_opened = target.open(target_key)
    except AttributeError:
        controller.response.append(f"You can't open the {target.name} try a different command.")
        return True

    if target_opened:
        controller.response.extend(target.look_inside())
    else:
        controller.response.append(f"The {target.name} is locked and you don't have the key.")
    return True

def close(controller: Controller):
    target = controller.tokens.direct_object
    try:
        target_closed = target.close()
    except AttributeError:
        controller.response.append(f"You can't close the {target.name} try a different command.")
        return True
    if target_closed:
        controller.response.append(f"{target.name} closed.")
    else:
        controller.response.append(f"No need. The {target.name} is already closed.")

def put(controller: Controller):
    item = controller.tokens.direct_object
    container = controller.tokens.indirect_object
    player_inventory = controller.player.inventory
    player_location = controller.player.location
    if container == player_inventory:
        # put {some item} in {inventory} is equivalent to take
        return take(controller)
    else:
        if not container.has_flag(Flags.CONTAINERBIT):
            controller.response.append(f"You can't. The {container.name} doesn't have anywhere to put it in (it's not a container).")
            return False
        if not container.has_flag(Flags.OPENBIT):
            controller.response.append(f"Why don't you try opening the {container.name} first!")
            return False
        if not item.has_flag(Flags.TAKEBIT):
            controller.response.append(f"You can't take the {item.name} in the first place. So....no.")
            return False
        if not (item.is_present(player_location) or item in player_inventory.items):
            controller.response.append(f"You can't put the {item.name} anywhere because it's not here.")
            return False

        # The 50 conditions for putting some shit into a container have been met, let's do this
        if (
                container.has_flag(Flags.CONTAINERBIT)
                and container.has_flag(Flags.OPENBIT)
                and item.has_flag(Flags.TAKEBIT)
                # the player either has the item or it is reachable in the current room
                and (item.is_present(player_location) or item in player_inventory.items)
        ):
            if container.check_item_fits_inside(item):
                player_inventory.remove_item(item)
                player_location.remove_item(item)
                container.add_item(item)
                controller.response.append(f"You put the {item.name} in the {container.name}.")
                return True
            else:
                controller.response.append(f"The {item.name} won't fit in the {container.name}!")
                return False

def clean(controller: Controller):
    item = controller.tokens.direct_object
    controller.response.append(f"You really put a spit shine on the {item.name}...but it looks much the same.")

def unlock(controller: Controller):
    pass

def inventory(controller: Controller):
    controller.response.extend(controller.player.inventory.look_inside())
    return True


def use(controller):
    """Handle 'use' command - primarily for special objects like vending machines."""
    target = controller.tokens.direct_object
    
    if not target:
        controller.response.append("Use what?")
        return False
        
    # Check if object has a custom action method
    if hasattr(target, 'action') and target.action_method_name:
        return target.action(controller=controller, target=target)
    
    # Default use behavior - most things can't be "used"
    controller.response.append(f"You can't use the {target.name}.")
    return False


def sit(controller):
    """Handle 'sit' command - sit on objects like chairs, couches, beds."""
    target = controller.tokens.direct_object
    
    if not target:
        controller.response.append("Sit on what?")
        return False
    
    # Check if object has a custom action method for sitting
    if hasattr(target, 'action') and target.action_method_name:
        return target.action(controller=controller, target=target)
    
    # Default sit behavior for most objects
    if "chair" in target.name.lower() or "couch" in target.name.lower() or "bed" in target.name.lower():
        controller.response.append(f"You sit on the {target.name}.")
        return True
    else:
        controller.response.append(f"You can't sit on the {target.name}.")
        return False


def talk(controller):
    """Handle 'talk' command - talk to NPCs."""
    from texticular.npc_manager import get_npc_manager
    
    target = controller.tokens.direct_object
    
    if not target:
        controller.response.append("Talk to whom?")
        return False
    
    # Check if the target is an NPC
    npc_manager = get_npc_manager()
    npc = npc_manager.get_npc(target.key_value)
    
    if not npc:
        controller.response.append(f"You can't talk to the {target.name}.")
        return False
    
    # Check if NPC is in the same room as player
    if npc.location_key != controller.player.location_key:
        controller.response.append(f"The {target.name} isn't here.")
        return False
    
    # Start conversation
    player_id = controller.player.key_value
    conversation = npc_manager.start_conversation(player_id, npc.key_value)
    
    if conversation:
        # Set game state to dialogue mode
        from texticular.game_enums import GameStates
        controller.gamestate = GameStates.DIALOGUESCENE
        controller.active_npc = npc
        controller.response.append(f"You approach the {npc.name}.")
        
        # Display conversation UI
        current_node = conversation.current_node()
        controller.ui.display_dialogue_interface(
            npc_name=npc.name,
            dialogue_text=current_node.text,
            choices=[choice.text for choice in current_node.choices]
        )
        return True
    else:
        controller.response.append(f"The {npc.name} doesn't seem interested in talking right now.")
        return False
