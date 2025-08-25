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
            # Check if the item has a custom TakeResponse
            if "TakeResponse" in item.descriptions:
                controller.response.append(item.descriptions["TakeResponse"])
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
    from texticular.actions.action_dispatcher import dispatch_object_action
    if dispatch_object_action(controller, target):
        return True
    
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
    from texticular.actions.action_dispatcher import dispatch_object_action
    if dispatch_object_action(controller, target):
        return True
    
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
    
    # Special case for genie - check if it's a genie object with dialogue
    if "genie" in target.name.lower():
        # Try to start genie dialogue directly
        if hasattr(controller, 'start_dialogue'):
            return controller.start_dialogue()
        else:
            controller.response.append("The Genie Bobblehead's googley eyes focus on you with an eerie intensity...")
            return True
    
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


def move_object(controller: Controller):
    """Handle move/adjust commands for objects"""
    item = controller.tokens.direct_object
    
    if "MoveResponse" in item.descriptions:
        controller.response.append(item.descriptions["MoveResponse"])
    else:
        controller.response.append(f"You can't move the {item.name}.")
    return True


def adjust(controller: Controller):
    """Handle adjust commands - same as move"""
    return move_object(controller)



def jump_on(controller: Controller):
    """Handle jumping on objects"""
    item = controller.tokens.direct_object
    
    if "JumpResponse" in item.descriptions:
        controller.response.append(item.descriptions["JumpResponse"])
    elif Flags.SETPIECEBIT in item.flags and any(word in item.name.lower() for word in ["bed", "couch", "mattress"]):
        controller.response.append(f"You jump on the {item.name}. It creaks and groans under your weight.")
    else:
        controller.response.append(f"Jumping on the {item.name} doesn't seem like a good idea.")
    return True


def lay_on(controller: Controller):
    """Handle laying on objects"""
    item = controller.tokens.direct_object
    
    if "LayResponse" in item.descriptions:
        controller.response.append(item.descriptions["LayResponse"])
    elif Flags.SETPIECEBIT in item.flags and any(word in item.name.lower() for word in ["bed", "couch", "mattress"]):
        controller.response.append(f"You lay down on the {item.name}. It's not very comfortable.")
    else:
        controller.response.append(f"You can't lay on the {item.name}.")
    return True


def touch(controller: Controller):
    """Handle touching objects"""
    item = controller.tokens.direct_object
    
    if "TouchResponse" in item.descriptions:
        controller.response.append(item.descriptions["TouchResponse"])
    else:
        controller.response.append(f"You touch the {item.name}. It feels about like you'd expect.")
    return True


def smell(controller: Controller):
    """Handle smelling objects"""
    item = controller.tokens.direct_object
    
    if "SmellResponse" in item.descriptions:
        controller.response.append(item.descriptions["SmellResponse"])
    elif "smell" in item.name.lower():
        controller.response.append(f"You take a whiff of the {item.name}. You immediately regret this decision.")
    else:
        controller.response.append(f"The {item.name} doesn't have much of a smell.")
    return True


def eat(controller: Controller):
    """Handle eating objects"""
    item = controller.tokens.direct_object
    
    if "EatResponse" in item.descriptions:
        controller.response.append(item.descriptions["EatResponse"])
    elif item.name.lower() in ["lemon", "food", "fruit"]:
        controller.response.append(f"You eat the {item.name}. It's... edible.")
    else:
        controller.response.append(f"You can't eat the {item.name}. That would be disgusting and possibly dangerous.")
    return True


def squeeze(controller: Controller):
    """Handle squeezing objects"""
    item = controller.tokens.direct_object
    
    if "SqueezeResponse" in item.descriptions:
        controller.response.append(item.descriptions["SqueezeResponse"])
    elif "lemon" in item.name.lower():
        controller.response.append(f"You squeeze the {item.name}. A little citrus juice drips out. Very refreshing!")
    else:
        controller.response.append(f"You squeeze the {item.name}. Nothing interesting happens.")
    return True


def break_object(controller: Controller):
    """Handle breaking objects"""
    item = controller.tokens.direct_object
    
    if "BreakResponse" in item.descriptions:
        controller.response.append(item.descriptions["BreakResponse"])
    elif Flags.SETPIECEBIT in item.flags:
        controller.response.append(f"You can't break the {item.name}. It's too sturdy, too important, or you just don't have the right tools.")
    else:
        controller.response.append(f"Breaking the {item.name} doesn't seem like a good idea right now.")
    return True


def turn_on(controller: Controller):
    """Handle turning on objects like TVs, lights, etc."""
    item = controller.tokens.direct_object
    
    if not item:
        controller.response.append("Turn on what?")
        return False
    
    # Check if it's a Television object with proper methods
    if hasattr(item, 'turn_on') and callable(item.turn_on):
        response = item.turn_on()
        controller.response.append(response)
        return True
    elif "TurnOnResponse" in item.descriptions:
        controller.response.append(item.descriptions["TurnOnResponse"])
    elif "tv" in item.name.lower():
        controller.response.append(f"You try to turn on the {item.name}, but it just displays static and fuzzy images. The reception here is terrible.")
    elif "light" in item.name.lower() or "lamp" in item.name.lower():
        controller.response.append(f"You turn on the {item.name}. The room brightens up a bit.")
    else:
        controller.response.append(f"You can't turn on the {item.name}.")
    return True


def turn_off(controller: Controller):
    """Handle turning off objects like TVs, lights, etc."""
    item = controller.tokens.direct_object
    
    if not item:
        controller.response.append("Turn off what?")
        return False
    
    # Check if it's a Television object with proper methods
    if hasattr(item, 'turn_off') and callable(item.turn_off):
        response = item.turn_off()
        controller.response.append(response)
        return True
    elif "TurnOffResponse" in item.descriptions:
        controller.response.append(item.descriptions["TurnOffResponse"])
    elif "tv" in item.name.lower():
        controller.response.append(f"You turn off the {item.name}. The room becomes a bit quieter.")
    elif "light" in item.name.lower() or "lamp" in item.name.lower():
        controller.response.append(f"You turn off the {item.name}. The room gets dimmer.")
    else:
        controller.response.append(f"You can't turn off the {item.name}.")
    return True


def stand_up(controller: Controller):
    """Handle getting up from sitting positions."""
    # Check if player is sitting on something
    # For now, just provide a generic response
    controller.response.append("You stand up and stretch your legs.")
    return True


def change_channel(controller: Controller):
    """Handle changing TV channels."""
    item = controller.tokens.direct_object
    
    if not item:
        # Look for a TV in the current room
        for room_item in controller.player.location.items:
            if "tv" in room_item.name.lower() and hasattr(room_item, 'change_channel'):
                response = room_item.change_channel()
                controller.response.append(response)
                return True
        controller.response.append("Change channel on what?")
        return False
    
    # Check if it's a Television object with channel changing capability
    if hasattr(item, 'change_channel') and callable(item.change_channel):
        response = item.change_channel()
        controller.response.append(response)
        return True
    elif "tv" in item.name.lower():
        controller.response.append(f"You fiddle with the knobs on the {item.name}, but nothing happens. Maybe it needs to be turned on first?")
    else:
        controller.response.append(f"You can't change channels on the {item.name}.")
    return True


def watch(controller: Controller):
    """Handle watching TV or other objects."""
    item = controller.tokens.direct_object
    
    if not item:
        controller.response.append("Watch what?")
        return False
    
    if "tv" in item.name.lower():
        # Check if it's a Television object that's on
        if hasattr(item, 'channels') and hasattr(item, 'flags'):
            from texticular.game_enums import Flags as Flag
            if Flag.ONBIT in item.flags:
                controller.response.append(f"You watch the {item.name}. Currently showing: {item.channels[item.current_channel]}")
            else:
                controller.response.append(f"The {item.name} is turned off. You see only your own reflection in the dark screen.")
        else:
            controller.response.append(f"You stare at the {item.name}, but it's not very interesting when it's off.")
    else:
        controller.response.append(f"You watch the {item.name} intently. Not much happens.")
    return True


def dial(controller: Controller):
    """Handle dialing phone numbers."""
    # This is more complex - need to extract the number from the input
    # For now, just direct to the phone if they have one
    phone = None
    
    # Look for phone in current room
    for item in controller.player.location.items:
        if "phone" in item.name.lower():
            phone = item
            break
    
    if phone and hasattr(phone, 'dial_number'):
        # Extract number from user input - this is a simplified approach
        import re
        numbers = re.findall(r'\b\d+(?:-\d+)*\b', controller.user_input)
        if numbers:
            response = phone.dial_number(numbers[0])
            controller.response.append(response)
        else:
            controller.response.append("What number would you like to dial?")
    else:
        controller.response.append("You don't see a phone here.")
    return True


def call(controller: Controller):
    """Handle calling - same as dial."""
    return dial(controller)
