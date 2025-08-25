#!/usr/bin/env python3
"""Test script to show ASCII UI output without input requirements"""

import sys
sys.path.insert(0, 'src')

from texticular.ui.ascii_ui import ASCIIGameUI, GameState

# Create test game state matching Room 201 specification
game_state = GameState(
    room_name="Room 201",
    room_description="As you look around the hotel room you see an old TV with rabbit ears that looks like it came straight out of the 1950's. Against the wall there is a beat up night stand with a little drawer built into it and black rotary phone on top. Next to it is a lumpy old bed that looks like it's seen better days, with a dark brown stain on the sheets and a funny smell coming from it. There is an obnoxious orange couch in the corner next to a small window smudged with sticky purple hand prints. The stuffing is coming out of the couch cushions which are also spotted with purple, and the floor is covered with empty cans of Fast Eddie's Colon Cleanse.",
    visible_items=[
        "On the floor you see a small folded piece of paper, looks like a note.",
        "A little lemon with a big attitude sits on the night stand."
    ],
    npcs=[
        "There is a strange little Genie Bobblehead with a speaker built into it on the nightstand that has googley eyes and an eery smile that almost seems like it's alive. It is holding a little sign that says \"Ask Me Anything...but you might WISH you hadn't hahaha!\". It's head is bouncing back and forth slightly and it seems to be silently judging you."
    ],
    exits=[
        {
            "direction": "west",
            "description": "is the DOOR to that sweet sweet porcelain throne",
            "name": "Bathroom Door"
        },
        {
            "direction": "east", 
            "description": "the DOOR leads outside to the hallway...where hopefully there are toilets",
            "name": "Hallway Door"
        }
    ],
    inventory=["pocket lint", "wallet"],
    turn=0,
    score=0,
    poop_level=45,
    location="Room 201",
    last_response="",
    dialogue_active=False,
    dialogue_content=None
)

# Create UI and render
ui = ASCIIGameUI()
print("=" * 80)
print("TEXTICULAR ASCII UI TEST - Room 201")
print("=" * 80)
print()

ui.render_game_screen(game_state)

print("\n" + "=" * 80)
print("END OF ASCII UI TEST")
print("=" * 80)