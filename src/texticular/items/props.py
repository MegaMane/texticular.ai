from texticular.items.story_item import StoryItem
from texticular.game_enums import Flags as Flag

class Television(StoryItem):
    def __init__(self, key_value: str, name: str, descriptions: dict, location_key: str,
                 synonyms: list = ["Television", "Tube", "Boob Tube"], adjectives: list = [],
                 flags: list = [Flag.SETPIECEBIT], channel_list: list = [],
                 turn_on_response = "You turn on the TV...", turn_off_response= "The TV flickers then goes black."):

        self.channels = channel_list
        self.current_channel = 0
        self.turn_on_response = turn_on_response
        self.turn_off_response = turn_off_response


        if len(self.channels) == 0:
            self.channels.append("Static...")

        super().__init__(key_value, name, descriptions, synonyms=synonyms,
                         adjectives=adjectives, location_key=location_key, flags=flags)


    def change_channel(self) ->str:
        response = ""
        if Flag.ONBIT in self.flags:
            if self.current_channel < len(self.channels) - 1:
                self.current_channel += 1
                response += "\n\nClick..." + self.channels[self.current_channel]
                return response
            else:
                self.current_channel = 0
                response += "\n\nClick..." + self.channels[self.current_channel]
                return response
        else:
            return "You have to turn the TV on first!\n"

    def turn_on(self) ->str:
        self.add_flag(Flag.ONBIT)
        response = ""
        response += "Click..." + self.turn_on_response + "\n\n" + "-------------------------\n\n" + self.channels[self.current_channel]
        return response

    def turn_off(self) ->str:
        self.remove_flag(Flag.ONBIT)
        return "\n\n" + self.turn_off_response


class Phone(StoryItem):
    def __init__(self, key_value: str, name: str, descriptions: dict, location_key: str,
                 synonyms: list = ["Phone"], adjectives: list = [],
                 flags: list = [Flag.SETPIECEBIT], numbers_dict: dict = None):
        
        super().__init__(key_value, name, descriptions, synonyms=synonyms,
                         adjectives=adjectives, location_key=location_key, flags=flags)
        
        self.numbers = numbers_dict or {
            "0": "Operator: All circuits are busy. Please try again later.",
            "911": "Emergency Services: What's your emergency? ...Wait, is this about a bathroom situation? We don't handle that.",
            "411": "Information: The number you have dialed has been changed to a non-published number.",
            "555-1234": "You hear a recording: 'Thank you for calling Fast Eddie's customer service. All representatives are currently helping other customers with their bowel movements.'"
        }
    
    def dial_number(self, number=None):
        if not number:
            return "What number would you like to dial? Try 'dial [number]' on the phone."
        
        if str(number) in self.numbers:
            return self.numbers[str(number)]
        else:
            return f"You dial {number}... The line rings a few times before disconnecting. Must be out of service."
