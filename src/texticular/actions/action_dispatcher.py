"""
Centralized action dispatcher for game objects.

Simple, direct dispatch system that's easy to debug and maintain.
Each object's custom actions are handled by checking the key_value directly.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from texticular.game_controller import Controller
    from texticular.game_object import GameObject


def dispatch_object_action(controller: Controller, target: GameObject) -> bool:
    """
    Main dispatcher for object-specific actions.
    
    Args:
        controller: The game controller
        target: The target GameObject
        
    Returns:
        bool: True if action was handled, False if not
    """
    key_value = target.key_value
    action = controller.tokens.action
    
    # Room 201 Objects
    if key_value == "room201-nightStand":
        return handle_nightstand_action(controller, target)
    elif key_value == "room201-purpleHandPrints":
        return handle_purple_handprints_action(controller, target)
    elif key_value == "room201-couch":
        return handle_couch_action(controller, target)
    elif key_value == "room201-genie":
        return handle_genie_action(controller, target)
    elif key_value == "vending-machine-2f":
        return handle_vending_machine_action(controller, target)
    elif key_value == "bathroom-room201":
        return handle_bathroom_great_dane_action(controller, target)
    
    # No custom action found
    return False


# Room 201 Action Handlers

def handle_nightstand_action(controller: Controller, target: GameObject) -> bool:
    """Handle nightstand interactions - redirect to drawer."""
    if controller.tokens.action == "open":
        # Redirect from the prop to the actual container then call the stock open method
        drawer = controller.get_game_object("room201-nightStand-drawer")
        if drawer:
            controller.tokens.direct_object = drawer
            controller.tokens.direct_object_key = drawer.key_value
            return controller.commands["open"](controller)
    return False


def handle_purple_handprints_action(controller: Controller, target: GameObject) -> bool:
    """Handle purple handprints interactions."""
    if controller.tokens.action in ["wipe", "wipe off", "clean"]:
        controller.response.append("Try as you might the hand prints are here to stay.")
        return True
    return False


def handle_couch_action(controller: Controller, target: GameObject) -> bool:
    """Handle couch interactions - sitting and standing."""
    action = controller.tokens.action
    
    if action == "sit":
        target.current_description = "Sitting"
        controller.response.append("You sit on the couch.")
        controller.response.append(target.describe())
        return True
    elif action in ["stand", "get off", "get up"]:
        target.current_description = "Main"
        controller.response.append("You get off the couch.")
        return True
    return False


def handle_genie_action(controller: Controller, target: GameObject) -> bool:
    """Handle genie bobblehead interactions."""
    from texticular.dialogue.dialogue_graph import DialogueGraph, DialogueNode, DialogueChoice
    from texticular.game_loader import get_data_path
    import json
    import os
    
    action = controller.tokens.action
    
    if action in ["talk", "speak", "ask", "rub", "touch"]:
        # Load dialogue from JSON file
        data_path = get_data_path()
        dialogue_file = os.path.join(data_path, "genie_dialogue.json")
        
        try:
            with open(dialogue_file, 'r') as f:
                dialogue_data = json.load(f)
            
            # Convert JSON to DialogueGraph
            nodes = []
            for node_data in dialogue_data['nodes']:
                choices = []
                for choice_data in node_data.get('choices', []):
                    choice = DialogueChoice(
                        text=choice_data['choice'],
                        leads_to_id=choice_data['leadsToId']
                    )
                    choices.append(choice)
                
                node = DialogueNode(
                    node_id=node_data['nodeId'],
                    text=node_data['text'],
                    choices=choices
                )
                nodes.append(node)
            
            dialogue_graph = DialogueGraph(dialogue_data['rootNodeID'], nodes)
            controller.dialogue_graph = dialogue_graph
            controller.start_dialogue()
            return True
            
        except FileNotFoundError:
            controller.response.append("The genie bobblehead sits silently. Something seems wrong with its magic.")
            return True
        except Exception as e:
            controller.response.append("The genie flickers mysteriously but says nothing.")
            return True
    
    return False


def handle_vending_machine_action(controller: Controller, target: GameObject) -> bool:
    """Handle vending machine interactions."""
    from texticular.items.vending_machine import VendingMachine
    
    # Ensure we're working with a VendingMachine object
    if not isinstance(target, VendingMachine):
        controller.response.append("This doesn't seem to be a proper vending machine.")
        return False
    
    action = controller.tokens.action
    
    # Handle "use vending machine" command
    if action in ["use", "operate", "activate"]:
        if target.is_active:
            controller.response.append("You're already using the vending machine.")
            controller.ui.set_menu(target.display_main_menu(), "Vending Machine")
            return True
        else:
            result = target.interact(controller)
            if target.is_active:
                controller.ui.display_vending_machine_menu(
                    target.responses["greeting"],
                    target.display_main_menu()
                )
            return result
    
    # Handle "look at vending machine"
    elif action == "look":
        controller.response.append(target.describe())
        if not target.is_active:
            controller.response.append("Type 'use vending machine' to start shopping!")
        else:
            controller.response.append(target.display_main_menu())
        return True
    
    # Default responses
    else:
        controller.response.append("The vending machine sits silently. Maybe try using it?")
        return True


def handle_bathroom_great_dane_action(controller: Controller, target: GameObject) -> bool:
    """Handle Great Dane bathroom encounter - game over logic."""
    player = controller.get_game_object("player")
    if not player:
        return False
    
    # Check if player has visited bathroom before
    bathroom_visited = target.times_visited > 0
    
    # Check if player has dog treats in inventory
    has_dog_treats = False
    dog_treats = None
    for item in player.inventory.items:
        if "dog treats" in item.name.lower() or "treats" in item.name.lower():
            has_dog_treats = True
            dog_treats = item
            break
    
    if bathroom_visited and not has_dog_treats:
        # GAME OVER - Player returns without dog treats
        controller.response.append("═" * 60)
        controller.response.append("🐕 GAME OVER 🐕")
        controller.response.append("═" * 60)
        controller.response.append("")
        controller.response.append("As you open the bathroom door, the massive Great Dane immediately")
        controller.response.append("recognizes you as the intruder who dared disturb its sacred duty.")
        controller.response.append("Without hesitation, the beast lunges forward with terrifying speed.")
        controller.response.append("")
        controller.response.append("Your last coherent thought is wondering why hotel security")
        controller.response.append("involves carnivorous canines...")
        controller.response.append("")
        controller.response.append("💀 You have been devoured by the Great Dane! 💀")
        controller.response.append("")
        controller.response.append("HINT: Try getting dog treats from the vending machine first!")
        controller.response.append("(Use coins from the couch cushions)")
        controller.response.append("═" * 60)
        
        # End game
        controller.game_over = True
        return True
        
    elif has_dog_treats:
        # Player has dog treats - feed the dane and make it sleepy
        controller.response.append("As you enter the bathroom, the Great Dane growls menacingly...")
        controller.response.append("But wait! You have dog treats!")
        controller.response.append("")
        controller.response.append("You toss the treats to the massive beast. Its eyes light up with")
        controller.response.append("pure joy as it devours the snacks. Within moments, the dog")
        controller.response.append("becomes drowsy and curls up peacefully in the corner.")
        controller.response.append("")
        controller.response.append("The bathroom is now safe! You can finally relieve yourself.")
        controller.response.append("🎉 VICTORY! You have successfully completed your quest! 🎉")
        
        # Remove dog treats from inventory
        if dog_treats:
            player.inventory.remove_item(dog_treats)
            
        # Change room descriptions to sleepy mode
        bathroom_exit = target.exits.get("EAST")  # Exit back to room 201
        if bathroom_exit:
            bathroom_exit.current_description = "SleepyTime"
            
        # Change room 201's west exit description too
        room201 = controller.get_game_object("room201")
        if room201 and "WEST" in room201.exits:
            room201.exits["WEST"].current_description = "Main"  # Back to normal
            
        # Mark game as won
        controller.game_won = True
        return True
        
    else:
        # First visit - player gets scared and leaves automatically
        controller.response.append("You crack open the door and peer inside...")
        controller.response.append("")
        controller.response.append("OH NO! There's an enormous Great Dane guarding the toilet!")
        controller.response.append("The beast fixes you with a hungry stare. Your survival")
        controller.response.append("instincts kick in and you quickly slam the door shut.")
        controller.response.append("")
        controller.response.append("You'll need to find something to appease that dog")
        controller.response.append("before you can safely use this bathroom!")
        controller.response.append("")
        controller.response.append("(Try talking to the genie for advice)")
        
        # Mark as visited and change door description
        target.times_visited = 1
        room201 = controller.get_game_object("room201")
        if room201 and "WEST" in room201.exits:
            room201.exits["WEST"].current_description = "GreatDane"
            
        # Don't actually enter the room on first visit
        return True
    
    return False