import logging
import textwrap
import texticular.actions.verb_actions as va
from texticular.game_object import GameObject
from texticular.rooms.room import Room
from texticular.game_enums import Directions
from texticular.character import Player,NPC
from dataclasses import dataclass
from texticular.game_enums import GameStates
from texticular.command_parser import Parser, ParseTree
from texticular.ui.fixed_layout_ui import FixedLayoutUI
from texticular.gameplay_logger import get_logger
from texticular.npc_manager import get_npc_manager
import texticular.globals as g



# Logging is now configured in __main__.py

class Controller:
    # def __new__(cls, gamemap: dict, player: Player):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Controller, cls).__new__(cls, gamemap, player)
    #     return cls.instance

    def __init__(self, gamemap: dict[str, Room], player: Player):
        self.gamemap = gamemap
        self.commands = {}
        self.player_input_history = []
        self.globals = {}
        self.response = []
        self.set_commands()
        self.gamestate = GameStates.EXPLORATION
        self.player = player
        self.parser = Parser(game_objects=GameObject.objects_by_key)
        self.tokens = ParseTree()
        self.ui = FixedLayoutUI()
        self.turn_count = 0
        self.score = 0
        self.poop_level = 45  # Starting urgency
        self.logger = get_logger()  # Get gameplay logger
        self.active_npc = None  # Currently talking to NPC
        
        # Initialize NPC system
        self.npc_manager = get_npc_manager()
        self._setup_npcs()



    def go(self):
        #https://patorjk.com/software/taag/#p=display&v=1&f=Standard&t=Texticular%3A%20Chapter%201%0AYou%20Gotta%20Go!
        #'Standard' Font
        intro_text = (
            """
  _____         _   _            _                 ____ _                 _              _ 
 |_   _|____  _| |_(_) ___ _   _| | __ _ _ __ _   / ___| |__   __ _ _ __ | |_ ___ _ __  / |
   | |/ _ \ \/ / __| |/ __| | | | |/ _` | '__(_) | |   | '_ \ / _` | '_ \| __/ _ \ '__| | |
   | |  __/>  <| |_| | (__| |_| | | (_| | |   _  | |___| | | | (_| | |_) | ||  __/ |    | |
   |_|\___/_/\_\\__|_|\___|\__,_|_| \__,_|_|  (_)  \____|_| |_|\__,_| .__/ \__\___|_|    |_|
 __   __             ____       _   _           ____       _       |_|                     
 \ \ / /__  _   _   / ___| ___ | |_| |_ __ _   / ___| ___ | |                              
  \ V / _ \| | | | | |  _ / _ \| __| __/ _` | | |  _ / _ \| |                              
   | | (_) | |_| | | |_| | (_) | |_| || (_| | | |_| | (_) |_|                              
   |_|\___/ \__,_|  \____|\___/ \__|\__\__,_|  \____|\___/(_)                              
                                                                                           
            """

        )

        #self.player.name = input("Hello, What is your first name >>")

        intro_scene_part1 = (
            "You wake up disoriented with a pounding headache in a shabby looking hotel room " 
            "surrounded by a bunch of empty cans. You've got a taste in your mouth like a dirty old rat crawled in "
            "and died in there. Disoriented, you roll out of the bed you woke up in, barely avoiding some questionable" 
            " stains on the sheets, as you stumble to your feet sending cans flying like bowling pins in your wake. "
            "You bend over to take a closer look at the pile of crushed aluminum. You read one of the labels: "
            '"Fast Eddie''s Colon Cleanse: When in doubt flush it out!"'
        )

        intro_scene_part2 = (
            "Side effects may include:\nDizzines, vomiting, diarrhea, cold sweats, hallucinations, intense panic," 
            "paranoia, permanent tongue discoloration, mild brain damage, amnesia, bowel implosion, and occasionally hiccups."
        )

        intro_scene_part3 = (
            "The can has a purple iridescent sludge oozing out of it that's really similar to the shade of purple that your"
            " hands are. Come to think of it, you vaguely remember signing up for a test group that was supposed to try"
            "out a new health drink. Looks like your part time job as a barrista just wasn't paying the bills, nothing "
            "like easy money! The thing is, you don't remember anything about going to a hotel last night, and you "
            "definitely don't remember anything about drinking a 24 pack of Fast Eddie's Colon Cleanse. Your stomach"
            "starts to feel a little uneasy, but never mind that, it's time to spend some of that hard earned cash! "
            "You reach into your wallet and realize in that moment that you don't even remember your name. You look at"
            f"your license and focus your still hazy eyes and barely make out that it says...{self.player.name}."
        )

        # Use Rich UI for intro
        intro_content = [
            intro_text,
            intro_scene_part1,
            intro_scene_part2, 
            intro_scene_part3
        ]
        
        self.ui.display_intro(intro_content)
        
        # Get initial room description and render first screen
        self.response = []
        self.commands["look"](self)
        self.render_game_screen()
        
        return ""  # No need to return content, UI handles display
    def handle_input(self) ->bool:
        g.CONTROLLER = self
        tokens = self.tokens
        verb = tokens.action
        direct_object= tokens.direct_object_key
        indirect_object = tokens.indirect_object
        
        # Handle special game states (vending machine, dialogue, etc.)
        if self.gamestate == GameStates.VENDING_MACHINE:
            return self.handle_vending_machine_input()
        
        # Normal exploration game state continues below...


        if isinstance(tokens.direct_object_key, Directions):
            # print("is instance of direction")
            return self.commands[verb](controller=self)


        logger = logging.getLogger(__name__)
        
        #Try letting the indirect object handle the input first
        if indirect_object:
            target_object = self.tokens.indirect_object
            if hasattr(target_object, 'action') and target_object.action_method_name:
                logger.debug(f"Indirect object handler: {target_object.name}")
                if target_object.action(controller=self, target=target_object):
                    return True

        #If that doesn't work try giving the direct object a change to handle the input
        if direct_object:
            target_object = self.tokens.direct_object
            if hasattr(target_object, 'action') and target_object.action_method_name:
                logger.debug(f"Direct object handler: {target_object.name}")
                if target_object.action(controller=self, target=target_object):
                    return True

        # fall through to the most generic verb response
        logger.debug(f"Generic verb handler: {verb}")
        if verb in self.commands:
            return self.commands[verb](controller=self)
        else:
            self.response.append(f"I don't know how to '{verb}' yet.")
            return False
    
    def handle_vending_machine_input(self) -> bool:
        """Handle input when the player is interacting with the vending machine."""
        # Find the active vending machine
        vending_machine = None
        for obj in GameObject.objects_by_key.values():
            if hasattr(obj, 'is_active') and obj.is_active:
                vending_machine = obj
                break
        
        if not vending_machine:
            # No active vending machine, return to exploration
            self.gamestate = GameStates.EXPLORATION
            self.response.append("The vending machine has mysteriously disappeared.")
            return False
        
        # Let the vending machine handle the input directly (bypasses parser)
        return vending_machine.handle_vending_input(self)

    def get_game_object(self, key_value: str) -> GameObject:
        game_object = GameObject.objects_by_key.get(key_value)
        return game_object

    def get_input(self):
        self.user_input = self.ui.get_input()
        self.player_input_history.append(self.user_input)
        self.user_input = self.user_input.strip()
        self.response = []

    def parse(self) ->bool:
        self.tokens = self.parser.parse_input(self.user_input)
        return self.tokens.input_parsed

    def update(self):
        # Handle special game states first (bypass parser)
        if self.gamestate == GameStates.VENDING_MACHINE:
            self.handle_vending_machine_input()
            self.clocker()
            return
        elif self.gamestate == GameStates.DIALOGUESCENE:
            self.handle_dialogue_input()
            self.clocker()
            return
        
        # Normal parsing for exploration mode
        parse_success = self.parse()
        
        if parse_success:
            logger = logging.getLogger(__name__)
            logger.debug(f"Parse successful: {self.tokens}")
            
            self.tokens.direct_object = self.get_game_object(self.tokens.direct_object_key)
            self.tokens.indirect_object = self.get_game_object(self.tokens.indirect_object_key)
            
            # Safe debug logging that handles directions
            direct_obj_method = "N/A (Direction)" if isinstance(self.tokens.direct_object_key, Directions) else (
                GameObject.objects_by_key.get(self.tokens.direct_object_key).action_method_name 
                if GameObject.objects_by_key.get(self.tokens.direct_object_key) else "None"
            )
            
            logger.debug(f"Player: {self.player.location.name}, Room method: {self.player.location.action_method_name}, Object method: {direct_obj_method}")
            self.handle_input()
            self.clocker()

        else:
            logger = logging.getLogger(__name__)
            self.response = [self.tokens.response]
            logger.debug(f"Parse failed: {self.tokens}")
            logger.debug(f"Player location: {self.player.location.name}")
        
        # Log the command and response
        response_text = ""
        if self.response:
            if isinstance(self.response, list):
                response_text = " ".join([str(r) for r in self.response])
            else:
                response_text = str(self.response)
        
        # Create game state snapshot for logging
        game_state = {
            "room_name": self.player.location.name if self.player.location else "Unknown",
            "turn": self.turn_count,
            "score": self.score,
            "poop_level": self.poop_level,
            "inventory": [item.name for item in self.player.inventory.items] if hasattr(self.player, 'inventory') and hasattr(self.player.inventory, 'items') else []
        }
        
        # Log the command
        self.logger.log_command(
            command=self.user_input,
            parse_success=parse_success,
            response=response_text,
            game_state=game_state
        )



    def render(self):
        '''Display the response using the new fixed layout UI'''
        self.render_game_screen()
        return ""  # UI handles display, no need to return text

    def render_game_screen(self):
        '''Render the complete game screen with current state'''
        # Prepare exits list
        exits = []
        if hasattr(self.player.location, 'exits') and self.player.location.exits:
            for direction, room_exit in self.player.location.exits.items():
                # Handle both string and Directions enum
                dir_name = direction.name if hasattr(direction, 'name') else str(direction).upper()
                exit_desc = f"{dir_name} - {room_exit.name}"
                if hasattr(room_exit, 'is_locked') and room_exit.is_locked:
                    exit_desc += " (locked)"
                exits.append(exit_desc)
        
        # Prepare inventory list
        inventory = []
        if hasattr(self.player, 'inventory') and self.player.inventory:
            if hasattr(self.player.inventory, 'items') and self.player.inventory.items:
                for item in self.player.inventory.items:
                    inventory.append(item.name)
        
        # Prepare response text
        response_text = ""
        if self.response:
            if isinstance(self.response, list):
                response_text = " ".join([str(r) for r in self.response])
            else:
                response_text = str(self.response)
        
        # Get room description and handle if it's a list
        room_description = ""
        if self.player.location:
            desc = self.player.location.describe()
            if isinstance(desc, list):
                room_description = " ".join([str(d) for d in desc])
            else:
                room_description = str(desc)
        else:
            room_description = "You are nowhere."
        
        # Create game state for UI
        game_state = {
            "room_name": self.player.location.name if self.player.location else "Unknown",
            "description": room_description,
            "exits": exits,
            "turn": self.turn_count,
            "score": self.score,
            "poop_level": self.poop_level,
            "inventory": inventory,
            "last_command": self.user_input if hasattr(self, 'user_input') else "",
            "response": response_text
        }
        
        # Render the screen
        self.ui.render_screen(game_state)

    def handle_dialogue_input(self):
        """Handle input during dialogue scenes."""
        npc_manager = get_npc_manager()
        player_id = self.player.key_value
        conversation = npc_manager.get_active_conversation(player_id)
        
        if not conversation:
            # No active conversation, return to exploration
            self.gamestate = GameStates.EXPLORATION
            self.active_npc = None
            self.response = ["The conversation has ended."]
            return
        
        current_node = conversation.current_node()
        
        # Handle end of conversation
        if not current_node.choices or current_node.node_id == "EXIT":
            # Conversation has ended
            npc_manager.end_conversation(player_id)
            self.gamestate = GameStates.EXPLORATION
            
            # Check for special dialogue outcomes
            if current_node.node_id == "SMALL_REQUEST" or current_node.node_id == "GRATEFUL_EXIT":
                # Janitor gives player money
                self.player.add_money(0.50)
                self.response = [current_node.text, "The janitor tosses you 50 cents!"]
                self.ui.display_dialogue_response(" ".join(self.response))
            else:
                self.response = [current_node.text]
                self.ui.display_dialogue_response(current_node.text)
            
            self.active_npc = None
            return
        
        # Parse user choice
        try:
            choice_num = int(self.user_input.strip()) - 1  # Convert to 0-based index
            
            if 0 <= choice_num < len(current_node.choices):
                # Valid choice
                success = npc_manager.make_dialogue_choice(player_id, choice_num)
                
                if success:
                    # Move to next node
                    updated_conversation = npc_manager.get_active_conversation(player_id)
                    if updated_conversation:
                        next_node = updated_conversation.current_node()
                        
                        # Display next dialogue
                        self.ui.display_dialogue_interface(
                            npc_name=self.active_npc.name,
                            dialogue_text=next_node.text,
                            choices=[choice.text for choice in next_node.choices]
                        )
                    else:
                        # Conversation ended
                        self.gamestate = GameStates.EXPLORATION
                        self.active_npc = None
                else:
                    self.response = ["Invalid choice. Please try again."]
            else:
                self.response = [f"Please choose a number between 1 and {len(current_node.choices)}."]
                
        except ValueError:
            # Handle special commands during dialogue
            if self.user_input.strip().lower() in ['quit', 'exit', 'leave']:
                npc_manager.end_conversation(player_id)
                self.gamestate = GameStates.EXPLORATION
                self.active_npc = None
                self.response = ["You end the conversation."]
            else:
                self.response = [f"Please enter a number (1-{len(current_node.choices)}) or 'quit' to leave."]
    
    def _setup_npcs(self):
        """Initialize NPCs from character data."""
        from texticular.character import NPC
        
        # Find all NPCs in the global object registry (loaded from JSON)
        npcs = {key: obj for key, obj in GameObject.objects_by_key.items() 
                if isinstance(obj, NPC)}
        
        # Register each NPC with the NPC manager
        for npc_key, npc in npcs.items():
            self.npc_manager.register_npc(npc)
            self.logger.log_event("npc_registered", {"name": npc.name, "location": npc.location_key})
    
    def clocker(self):
        # Increment turn and increase poop urgency
        self.turn_count += 1
        self.poop_level = min(100, self.poop_level + 2)  # Increase urgency each turn
    def main_loop(self):
        pass

    def set_commands(self):
        self.commands["look"] = va.look
        self.commands["examine"] = va.look  # Add examine as alias for look
        self.commands["search"] = va.look   # Add search as alias for look
        self.commands["walk"] = va.walk
        self.commands["go"] = va.walk
        self.commands["move"] = va.walk
        self.commands["get"] = va.take
        self.commands["take"] = va.take
        self.commands["drop"] = va.drop
        self.commands["open"] = va.open
        self.commands["close"] = va.close
        self.commands["put"] = va.put
        self.commands["use"] = va.use
        self.commands["sit"] = va.sit  # Add sit command
        self.commands["inventory"] = va.inventory
        self.commands["i"] = va.inventory  # Add shortcut for inventory
        self.commands["talk"] = va.talk  # Add talk command for NPCs
        self.commands["speak"] = va.talk  # Add speak as alias for talk
        self.commands["wipe"] = va.clean
        self.commands["wipe off"] = va.clean




