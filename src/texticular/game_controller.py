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
from texticular.ui.terminal_ui import TerminalUI
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
        self.ui = TerminalUI()



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
        
        # Get initial room description  
        self.response = []
        self.commands["look"](self)
        self.ui.display_room(self.response)
        
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
        
        # Normal parsing for exploration mode
        if self.parse():
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



    def render(self):
        '''Display the response using Rich UI'''
        if self.gamestate == GameStates.VENDING_MACHINE:
            # Handle vending machine display
            self.ui.display_vending_response(self.response)
        else:
            # Handle regular room/exploration display
            self.ui.display_response(self.response)
        
        return ""  # UI handles display, no need to return text

    def clocker(self):
        pass
    def main_loop(self):
        pass

    def set_commands(self):
        self.commands["look"] = va.look
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
        self.commands["inventory"] = va.inventory
        self.commands["wipe"] = va.clean
        self.commands["wipe off"] = va.clean




