#!/usr/bin/env python3
"""
Quick test script to verify Room 201 objects and actions work.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.actions.action_dispatcher import dispatch_object_action

def test_room201():
    print("Testing Room 201 objects and actions...")
    
    # Load game map
    from texticular.game_loader import load_game_map
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    
    # Initialize game controller
    controller = Controller(gamemap, player)
    
    # Get player starting room (should be Room 201)
    player = controller.get_game_object("player")
    if not player:
        print("❌ Player not found!")
        return
    
    current_room = controller.get_game_object(player.location_key)
    print(f"✅ Player is in: {current_room.name} ({current_room.key_value})")
    
    # Test key Room 201 objects
    test_objects = [
        "room201-couch",
        "room201-purpleHandPrints", 
        "room201-genie",
        "room201-nightStand"
    ]
    
    print("\nTesting object existence:")
    for obj_key in test_objects:
        obj = controller.get_game_object(obj_key)
        if obj:
            print(f"✅ Found {obj_key}: {obj.name}")
        else:
            print(f"❌ Missing {obj_key}")
    
    # Test action dispatcher
    print("\nTesting action dispatcher:")
    
    # Test purple handprints
    handprints = controller.get_game_object("room201-purpleHandPrints")
    if handprints:
        # Mock the controller tokens for testing
        class MockTokens:
            action = "wipe"
            direct_object = handprints
            direct_object_key = "room201-purpleHandPrints"
            indirect_object = None
        
        controller.tokens = MockTokens()
        controller.response = []
        
        result = dispatch_object_action(controller, handprints)
        if result and controller.response:
            print(f"✅ Purple handprints action worked: {controller.response[0]}")
        else:
            print("❌ Purple handprints action failed")
    
    # Test couch sitting
    couch = controller.get_game_object("room201-couch")
    if couch:
        class MockTokens:
            action = "sit"
            direct_object = couch
            direct_object_key = "room201-couch"
            indirect_object = None
        
        controller.tokens = MockTokens()
        controller.response = []
        
        result = dispatch_object_action(controller, couch)
        if result and controller.response:
            print(f"✅ Couch action worked: {controller.response[0]}")
        else:
            print("❌ Couch action failed")
    
    print("\nRoom 201 test complete!")

if __name__ == "__main__":
    test_room201()