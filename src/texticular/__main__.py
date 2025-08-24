from texticular.game_controller import Controller
import textwrap
import logging
#These imports should go away after testing
from texticular.game_loader import load_game_map
from texticular.game_enums import Directions
from texticular.game_object import GameObject
import texticular.globals

# Configure logging to keep debug output separate from game
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('texticular_debug.log'),
        # Remove console handler to keep debug out of game output
    ]
)


gamemap = load_game_map("GameConfigManifest.json")
player = gamemap["characters"]["player"]


controller = Controller(gamemap, player)



controller.go()  # Rich UI handles display
while controller.gamestate.name != "GAMEOVER":
    controller.get_input()
    should_continue = controller.update()
    if should_continue == False:  # Explicit check for quit command
        break
    controller.render()  # Rich UI handles display





