from game_controller import Controller
import textwrap
#These imports should go away after testing
from texticular.game_loader import load_game_map
from texticular.game_enums import Directions
from texticular.game_object import GameObject
import texticular.globals


gamemap = load_game_map("./../../data/GameConfigManifest.json")
player = gamemap["characters"]["player"]


controller = Controller(gamemap, player)



print(controller.go())
while controller.gamestate.name != "GAMEOVER":
    controller.get_input()
    controller.update()
    print(controller.render())





