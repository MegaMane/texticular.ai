"""
Action methods for Room 201 interactable objects.
These handle specialized interactions beyond basic verb responses.
"""

import random
from texticular.game_enums import GameStates


def action_room201_tv(controller, target=None):
    """Handle TV interactions: turn on, turn off, change channel, watch"""
    user_input = controller.user_input.lower()
    
    # TV channels for entertainment
    channels = [
        "Whenever I feel like a sweaty slob, there is one assurance that gives me peace of mind. Deodorant. Just one wipe under each arm pit and I am good to go for days. Heck, I don't even need to shower for one whole week. That's how good this shit is.",
        "Ever sit on a toilet and have the never ending wipe? Well, those days are over. I've invented one wipes. A new form of toilet paper that contains a solution where with just one wipe, you are fresh and clean. Done deal.",
        "Well, I'm your Vita-vega-vittival girl. Are you tired? Run-down? Listless? Do you poop out at parties? Are you unpoopular? Well, are you? The answer to all your problems is in this little ol' bottle…Vitameatavegemin. That's it. Vitameatavegemin contains vitamins, meat, meg-e-tables, and vinerals. So why don't you join the thousands of happy, peppy people and get a great big bottle of Vita-veaty-vega-meany-minie-moe-amin. I'll tell you what you have to do. You have to take a whole tablespoon after every meal. It's so tasty, too: it's just like candy. So everybody get a bottle of…this stuff.",
        "Static..."
    ]
    
    if any(phrase in user_input for phrase in ["turn on", "switch on", "power on"]):
        controller.response.append("You turn on the old TV. After some static and crackling, a fuzzy image appears...")
        controller.response.append(f"Channel: {random.choice(channels)}")
        return True
        
    elif any(phrase in user_input for phrase in ["turn off", "switch off", "power off"]):
        controller.response.append("You turn off the TV. The screen goes dark with a satisfying 'pop' sound.")
        return True
        
    elif any(phrase in user_input for phrase in ["change channel", "channel", "switch channel"]):
        controller.response.append("You fiddle with the knobs and the channel changes...")
        controller.response.append(f"Channel: {random.choice(channels)}")
        return True
        
    elif "watch" in user_input:
        controller.response.append("You watch the fuzzy TV screen...")
        controller.response.append(f"Currently showing: {random.choice(channels)}")
        return True
        
    # Default TV response
    controller.response.append("The TV sits there, ancient and dusty. Try turning it on, changing the channel, or watching it.")
    return True


def action_room201_bed(controller, target=None):
    """Handle bed interactions: sit, lay, jump, etc."""
    user_input = controller.user_input.lower()
    
    if any(phrase in user_input for phrase in ["sit", "sit on"]):
        controller.response.append("You sit on the edge of the lumpy bed. The springs creak ominously and you sink deeper than expected. This mattress has definitely seen better days.")
        return True
        
    elif any(phrase in user_input for phrase in ["lay", "lie", "lay on", "lie on", "sleep"]):
        controller.response.append("You lay down on the bed and immediately regret it. The mattress is lumpy, the springs poke into your back, and that stain is way too close to your face. You get up quickly.")
        return True
        
    elif any(phrase in user_input for phrase in ["jump", "jump on", "bounce"]):
        controller.response.append("You bounce on the lumpy old bed. The springs creak ominously and you notice the dark brown stain is even more prominent now. Maybe jumping on it wasn't the best idea.")
        return True
        
    elif any(phrase in user_input for phrase in ["look in", "look inside", "search"]):
        controller.response.append("You carefully check under the bed and around the mattress. Nothing interesting here except dust bunnies and a smell you'd rather not investigate further.")
        return True
        
    # Default bed response
    controller.response.append("The bed looks like it's seen too much action already. You can sit on it, lay down, or jump on it if you're feeling adventurous.")
    return True


def action_room201_couch(controller, target=None):
    """Handle couch interactions: sit, search cushions, etc."""
    user_input = controller.user_input.lower()
    
    if any(phrase in user_input for phrase in ["sit", "sit on"]):
        controller.response.append("You plop down on the obnoxious orange couch. The stuffing crunches under you and you sink in way too deep. This thing has definitely seen better days.")
        return True
        
    elif any(phrase in user_input for phrase in ["lay", "lie", "lay on", "lie on"]):
        controller.response.append("You stretch out on the orange couch. It's surprisingly comfortable despite the torn fabric and purple stains. You could probably take a nap here if you weren't so desperate to find a bathroom.")
        return True
        
    elif any(phrase in user_input for phrase in ["jump", "jump on", "bounce"]):
        controller.response.append("You jump on the couch cushions. More stuffing puffs out of the tears and the springs groan in protest. The whole couch shifts slightly.")
        return True
        
    elif any(phrase in user_input for phrase in ["look in", "look inside", "search"]):
        controller.response.append("You should try looking in the couch cushions specifically. There might be something hidden there.")
        return True
        
    # Default couch response
    controller.response.append("The orange couch dominates the corner of the room. You can sit on it, lay down, or search the cushions for hidden items.")
    return True


def action_room201_window(controller, target=None):
    """Handle window interactions"""
    user_input = controller.user_input.lower()
    
    if any(phrase in user_input for phrase in ["open"]):
        controller.response.append("You try to open the window but it's stuck shut. Years of grime and those sticky purple handprints have sealed it tight.")
        return True
        
    elif any(phrase in user_input for phrase in ["break", "smash"]):
        controller.response.append("You consider breaking the window to escape, but you're on the second floor and there's probably a better way out. Plus, the purple handprints are so gross you don't want to touch them.")
        return True
        
    elif any(phrase in user_input for phrase in ["look", "look through", "peer"]):
        controller.response.append("You peer through a clean spot on the dirty window. You can make out the hotel's courtyard below and some of the city beyond, but the grime obscures most of the view.")
        return True
        
    elif any(phrase in user_input for phrase in ["touch", "feel"]):
        controller.response.append("You touch the window glass and immediately regret it. The purple handprints are sticky and smell weird. Your hand comes away slightly purple.")
        return True
        
    # Default window response
    controller.response.append("The small window is smudged with sticky purple handprints. You could try opening it, looking through it, or... touching those gross handprints if you really want to.")
    return True


def action_room201_phone(controller, target=None):
    """Handle rotary phone interactions"""
    user_input = controller.user_input.lower()
    
    # Phone numbers the player could discover and dial
    phone_responses = {
        "911": "You dial 911. 'Emergency services, what's your emergency?' You explain about being trapped in a hotel room with a desperate need for a bathroom. 'Sir, that's not really an emergency.' Click. They hung up.",
        "411": "You dial 411 for information. 'What city and state?' You're not even sure where you are. After some confusion, they hang up on you.",
        "0": "You dial 0 for the operator. An elderly woman's voice answers: 'Hotel front desk, how can I help you?' Finally! Maybe she can help you find a working bathroom.",
        "front desk": "You dial the front desk. 'Hello, hotel front desk. How can we help you today?'",
        "default": "You pick up the heavy receiver and dial randomly. The line rings a few times before someone answers: 'Joe's Pizza, we deliver!' Wrong number."
    }
    
    if any(phrase in user_input for phrase in ["dial", "call", "phone"]):
        # For now, give a random response since we don't have number parsing
        controller.response.append("You pick up the heavy rotary phone receiver. The dial tone buzzes in your ear.")
        controller.response.append("Try dialing a specific number like 0 for the operator, 911 for emergency, or 411 for information.")
        return True
        
    elif "0" in user_input and "dial" in user_input:
        controller.response.append(phone_responses["0"])
        return True
        
    elif "911" in user_input:
        controller.response.append(phone_responses["911"])
        return True
        
    elif "411" in user_input:
        controller.response.append(phone_responses["411"])
        return True
        
    # Default phone response
    controller.response.append("The old rotary phone sits heavily on the nightstand. You could try dialing a number - maybe 0 for the front desk, 911 for emergency, or 411 for information.")
    return True


def action_room201_genie(controller, target=None):
    """Handle genie bobblehead interactions - start dialogue"""
    user_input = controller.user_input.lower()
    
    if any(phrase in user_input for phrase in ["talk", "speak", "ask", "talk to", "speak to"]):
        # Load and start the genie dialogue using the existing dialogue system
        try:
            import json
            from texticular.dialogue.dialogue_graph import DialogueGraph, DialogueNode, DialogueChoice
            
            # Load the genie dialogue from JSON
            with open('data/genie_dialogue.json', 'r') as f:
                dialogue_data = json.load(f)
            
            # Create dialogue nodes
            nodes = []
            for node_data in dialogue_data['nodes']:
                choices = []
                for choice_data in node_data['choices']:
                    choice = DialogueChoice(choice_data['choice'], choice_data['leadsToId'])
                    choices.append(choice)
                
                node = DialogueNode(node_data['nodeId'], node_data['text'], choices)
                nodes.append(node)
            
            # Create dialogue graph
            dialogue_graph = DialogueGraph(dialogue_data['rootNodeID'], nodes, dialogue_data.get('title'))
            
            # Start dialogue mode
            controller.gamestate = GameStates.DIALOGUESCENE
            controller.active_npc = target
            
            # Set up dialogue content for ASCII UI
            current_node = dialogue_graph.current_node()
            dialogue_content = {
                "npc_name": "Genie Bobblehead",
                "current_text": current_node.text,
                "choices": [{"text": choice.text, "next_node": choice.leads_to_id} for choice in current_node.choices]
            }
            
            # Store dialogue graph and content in controller
            controller.dialogue_graph = dialogue_graph
            controller.dialogue_content = dialogue_content
            
            controller.response.append("The Genie Bobblehead's head stops bouncing and the googly eyes focus on you with an eerie intensity...")
            return True
            
        except Exception as e:
            controller.response.append(f"The genie tries to speak but seems to be malfunctioning... (Error: {e})")
            return True
        
    elif any(phrase in user_input for phrase in ["take", "pick up", "grab"]):
        controller.response.append("You try to pick up the genie bobblehead, but it seems to be stuck to the nightstand. As you touch it, the googly eyes swivel to look at you and it speaks: 'Ah ah ah! No touchy without asking nicely first!'")
        return True
        
    elif any(phrase in user_input for phrase in ["break", "smash", "destroy"]):
        controller.response.append("You raise your hand to smash the creepy bobblehead, but it speaks up: 'I wouldn't do that if I were you, mortal. Break me and you'll never find what you're looking for!' The threat in its tiny voice is surprisingly convincing.")
        return True
        
    # Default genie response
    controller.response.append("The strange genie bobblehead stares at you with its googly eyes. Its head bounces slightly and you swear you can see it smiling. Try talking to it, asking it something, or speaking to it.")
    return True


# Dictionary mapping action method names to functions
ROOM201_ACTIONS = {
    "action_room201_tv": action_room201_tv,
    "action_room201_bed": action_room201_bed,
    "action_room201_couch": action_room201_couch,
    "action_room201_window": action_room201_window,
    "action_room201_phone": action_room201_phone,
    "action_room201_genie": action_room201_genie,
}