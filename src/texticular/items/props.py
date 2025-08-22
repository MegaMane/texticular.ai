from texticular.items.story_item import StoryItem

class Television(StoryItem):
    def __init__(self, key_value: str, name: str, descriptions: dict, location_key: str,
                 synonyms: list = ["Television", "Tube", "Boob Tube"], slots_occupied: int = 99, adjectives: list = [],
                 flags: list = [Flag.SETPIECEBIT], commands: dict = {}, channel_list:list = [],
                 turn_on_response = "You turn on the TV...", turn_off_response= "The TV flickers then goes black."):

        self.channels = channel_list
        self.current_channel = 0
        self.turn_on_response = turn_on_response
        self.turn_off_response = turn_off_response


        if len(self.channels) == 0:
            self.channels.append("Static...")

        super().__init__(key_value, name, descriptions, location_key=location_key, synonyms=synonyms,
                         slots_occupied=slots_occupied, adjectives=adjectives, flags=flags, commands=commands)

        self.commands["change channel"] = self.change_channel
        self.commands["turn on"] = self.turn_on
        self.commands["power on"] = self.turn_on
        self.commands["turn off"] = self.turn_off
        self.commands["power off"] = self.turn_off


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
    pass
