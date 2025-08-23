"""
VendingMachine - Special interactive object for Texticular
Handles shop mechanics and item purchasing
"""

from texticular.items.story_item import StoryItem
from texticular.game_enums import Flags, GameStates
from typing import Dict, Any


class VendingMachine(StoryItem):
    """
    A talking vending machine that sells Fast Eddie's and Dog Treats.
    
    Features:
    - Menu-driven interface (similar to dialogue system)
    - Item inventory with prices
    - Money validation and transaction handling
    - Humorous responses and personality
    - Integration with main game loop
    """
    
    def __init__(self, key_value: str, name: str, descriptions: dict, location_key: str = None, flags: list = None, synonyms: list = None, adjectives: list = None):
        # Define synonyms if not provided
        if synonyms is None:
            synonyms = [
                "vending machine",
                "machine", 
                "fast eddie's machine",
                "vendor",
                "vending"
            ]
        
        if adjectives is None:
            adjectives = ["shiny", "talking"]
            
        super().__init__(
            key_value=key_value,
            name=name, 
            descriptions=descriptions,
            synonyms=synonyms,
            adjectives=adjectives,
            location_key=location_key,
            flags=flags,
            size=1000
        )
        
        # Vending machine inventory: item_key -> {name, price, description, stock}
        self.inventory = {
            "fast_eddies": {
                "name": "Fast Eddie's Colon Cleanse",
                "price": 0.50,
                "description": "When in doubt, flush it out! (Warning: May cause explosive results)",
                "stock": 99,
                "synonyms": ["fast eddies", "colon cleanse", "eddie's", "cleanse"]
            },
            "dog_treats": {
                "name": "Sleepy Time Dog Treats",
                "price": 2.50, 
                "description": "Guaranteed to knock out even the angriest Great Dane!",
                "stock": 5,
                "synonyms": ["dog treats", "sleepy time", "treats", "scooby snacks"]
            }
        }
        
        # Current interface state
        self.interface_state = "main_menu"  # main_menu, item_selection, payment
        self.selected_item = None
        self.is_active = False
        
        # Talking machine personality responses
        self.responses = {
            "greeting": [
                "*** WELCOME TO FAST EDDIE'S AUTOMATED DISPENSARY! ***",
                "Insert coins to continue, or just admire my shiny chrome exterior.",
                "I've been waiting here all day for someone with loose change!"
            ],
            "insufficient_funds": [
                "INSUFFICIENT FUNDS! What do I look like, a charity case?",
                "Your poverty is showing, friend. Come back with real money.",
                "Error 404: Money not found. Try checking your couch cushions."
            ],
            "successful_purchase": [
                "TRANSACTION COMPLETE! Pleasure doing business with you!",
                "Ka-ching! Your item is dispensed below. Don't forget to tip your machine!",
                "Sold! Another satisfied customer. Leave a 5-star review!"
            ],
            "out_of_stock": [
                "ITEM OUT OF STOCK! Popular item, that one. Too bad for you.",
                "Sold out faster than tickets to a bathroom emergency convention.",
                "Nothing left but disappointment and the smell of opportunity lost."
            ],
            "goodbye": [
                "Come back soon! My loneliness is financially devastating.",
                "Thanks for visiting! I'll be here, dispensing and judging silently.",
                "Farewell! May your purchases serve you better than they served the last guy."
            ]
        }
    
    def interact(self, controller):
        """
        Main interaction method called when player uses the vending machine.
        Switches game to vending machine interface.
        """
        if not self.is_active:
            controller.response.extend(self.responses["greeting"])
            controller.response.append(self.display_main_menu())
            self.is_active = True
            controller.gamestate = GameStates.VENDING_MACHINE
            return True
        else:
            # Machine is already active, handle the current input
            return self.handle_vending_input(controller)
    
    def display_main_menu(self) -> str:
        """Display the main vending machine menu with items and prices."""
        menu = ["", "=" * 60]
        menu.append("*** FAST EDDIE'S VENDING MACHINE MENU ***")
        menu.append("=" * 60)
        menu.append("")
        
        for i, (item_key, item_data) in enumerate(self.inventory.items(), 1):
            stock_text = f"({item_data['stock']} left)" if item_data['stock'] > 0 else "(SOLD OUT)"
            price_text = f"${item_data['price']:.2f}"
            menu.append(f"{i}. {item_data['name']} - {price_text} {stock_text}")
            menu.append(f"   {item_data['description']}")
            menu.append("")
        
        menu.append("Commands: '1' or '2' to buy, 'insert money', 'leave'")
        menu.append("=" * 60)
        
        return "\n".join(menu)
    
    def handle_vending_input(self, controller):
        """
        Process vending machine menu commands directly (bypasses parser).
        Simple finite state machine for menu-driven interface.
        """
        user_input = controller.user_input.lower().strip()
        
        # Menu command mapping
        menu_commands = {
            # Purchase commands
            "1": lambda: self.buy_item(controller, 1),
            "2": lambda: self.buy_item(controller, 2),
            
            # Money commands  
            "money": lambda: self.insert_money(controller),
            "coin": lambda: self.insert_money(controller),
            "coins": lambda: self.insert_money(controller),
            "insert money": lambda: self.insert_money(controller),
            
            # Menu/help commands
            "menu": lambda: self.show_menu(controller),
            "help": lambda: self.show_menu(controller),
            "look": lambda: self.show_menu(controller),
            "?": lambda: self.show_menu(controller),
            
            # Exit commands
            "leave": lambda: self.exit_vending_machine(controller),
            "exit": lambda: self.exit_vending_machine(controller),
            "quit": lambda: self.exit_vending_machine(controller),
            "done": lambda: self.exit_vending_machine(controller),
        }
        
        # Execute command if found
        if user_input in menu_commands:
            return menu_commands[user_input]()
        
        # Default response for unknown commands
        controller.response.append("Invalid command! Valid options:")
        controller.response.append("  1 or 2 - Buy item")
        controller.response.append("  'money' - Insert coins")
        controller.response.append("  'menu' - Show menu")
        controller.response.append("  'leave' - Exit")
        return True
    
    def buy_item(self, controller, item_number: int):
        """Buy an item by menu number (1 or 2)."""
        return self.attempt_purchase(controller, item_number)
    
    def insert_money(self, controller):
        """Insert money into the vending machine."""
        controller.response.append("*CLINK* Found some loose change in your pocket!")
        controller.player.add_money(0.50)
        controller.response.append(f"You now have ${controller.player.money:.2f}")
        controller.response.append("(Tip: Check the nightstand drawer upstairs for more coins!)")
        return True
    
    def show_menu(self, controller):
        """Display the vending machine menu."""
        controller.response.append(self.display_main_menu())
        return True
    
    def exit_vending_machine(self, controller):
        """Exit the vending machine interface."""
        controller.response.extend(self.responses["goodbye"])
        self.is_active = False
        controller.gamestate = GameStates.EXPLORATION
        controller.ui.exit_vending_machine()  # Clear the persistent menu
        return True
    
    def attempt_purchase(self, controller, item_number: int):
        """Attempt to purchase an item by menu number."""
        try:
            item_keys = list(self.inventory.keys())
            item_key = item_keys[item_number - 1]
            item_data = self.inventory[item_key]
        except IndexError:
            controller.response.append(f"Invalid item number. Choose 1-{len(self.inventory)}.")
            return True
        
        # Check stock
        if item_data["stock"] <= 0:
            controller.response.extend(self.responses["out_of_stock"])
            return True
        
        # Check player money (we'll need to implement this)
        player_money = getattr(controller.player, 'money', 0.00)
        if player_money < item_data["price"]:
            controller.response.extend(self.responses["insufficient_funds"])
            controller.response.append(f"You need ${item_data['price']:.2f} but only have ${player_money:.2f}")
            return True
        
        # Successful purchase
        self.complete_purchase(controller, item_key, item_data)
        return True
    
    def complete_purchase(self, controller, item_key: str, item_data: dict):
        """Complete a successful purchase transaction."""
        # Deduct money (we'll implement this in Player class)
        controller.player.spend_money(item_data["price"])
        
        # Reduce stock
        item_data["stock"] -= 1
        
        # Create the purchased item and add to player inventory
        purchased_item = self.create_purchased_item(item_key, item_data)
        controller.player.inventory.add_item(purchased_item)
        
        # Success message
        controller.response.extend(self.responses["successful_purchase"])
        controller.response.append(f"You bought {item_data['name']} for ${item_data['price']:.2f}")
        controller.response.append(f"Remaining money: ${controller.player.money:.2f}")
        
        # Check for story progression (dog treats purchase)
        if item_key == "dog_treats":
            controller.response.append("")
            controller.response.append("The treats smell like bacon and valium...")
            controller.response.append("Perfect for calming angry guard dogs!")
        
    def create_purchased_item(self, item_key: str, item_data: dict):
        """Create a StoryItem object for the purchased item."""
        from texticular.items.story_item import StoryItem
        
        # Create appropriate StoryItem based on what was bought
        if item_key == "fast_eddies":
            return StoryItem(
                key_value="purchased_fast_eddies",
                name="Fast Eddie's Colon Cleanse", 
                descriptions={
                    "Main": "A can of Fast Eddie's Colon Cleanse. The warning label takes up most of the can.",
                    "Dropped": "An unopened can of Fast Eddie's lies on the ground, oozing slightly."
                },
                synonyms=["fast eddies", "colon cleanse", "can", "eddie's"],
                adjectives=["purchased"],
                location_key="player_inventory",
                flags=["TAKEBIT"]
            )
        elif item_key == "dog_treats":
            return StoryItem(
                key_value="sleepy_time_dog_treats",
                name="Sleepy Time Dog Treats",
                descriptions={
                    "Main": "A bag of Sleepy Time Dog Treats. They smell like bacon and something... medicinal.",
                    "Dropped": "The dog treats lie scattered on the ground. They still smell effective."
                },
                synonyms=["dog treats", "sleepy time", "treats", "scooby snacks"],
                adjectives=["sleepy", "time"],
                location_key="player_inventory", 
                flags=["TAKEBIT"]
            )
        
        return None
    
    def get_money_hint(self) -> str:
        """Return a hint about where to find money."""
        return ("Psst... I heard someone dropped some change in the nightstand drawer upstairs. "
               "Also, that janitor looks like he might have deep pockets...")
    
    def serialize(self) -> dict:
        """Serialize vending machine state to JSON for saving."""
        data = super().serialize()
        data.update({
            "inventory": self.inventory,
            "interface_state": self.interface_state,
            "is_active": self.is_active
        })
        return data
    
    @classmethod
    def deserialize(cls, data: dict):
        """Create VendingMachine from saved JSON data."""
        machine = cls(
            key_value=data["keyValue"],
            name=data["name"], 
            descriptions=data["descriptions"],
            location_key=data.get("locationKey"),
            flags=data.get("flags", [])
        )
        
        if "inventory" in data:
            machine.inventory = data["inventory"]
        if "interface_state" in data:
            machine.interface_state = data["interface_state"]
        if "is_active" in data:
            machine.is_active = data["is_active"]
            
        return machine