#!/usr/bin/env python3
"""
Comprehensive test for Room 201 tutorial experience.
Tests all interactions from GameInteractions.txt specification.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map
from texticular.actions.action_dispatcher import dispatch_object_action


class MockTokens:
    def __init__(self, action, direct_object_key, direct_object=None, indirect_object=None):
        self.action = action
        self.direct_object_key = direct_object_key
        self.direct_object = direct_object
        self.indirect_object = indirect_object


def test_object_interaction(controller, obj_key, action, expected_keywords=None):
    """Helper to test a specific object interaction."""
    obj = controller.get_game_object(obj_key)
    if not obj:
        return f"❌ Object {obj_key} not found"
    
    controller.tokens = MockTokens(action, obj_key, obj)
    controller.response = []
    
    result = dispatch_object_action(controller, obj)
    
    if result and controller.response:
        response_text = " ".join(controller.response)
        if expected_keywords:
            for keyword in expected_keywords:
                if keyword.lower() not in response_text.lower():
                    return f"⚠️  {obj_key} {action}: Missing '{keyword}' in response: {response_text[:50]}..."
        return f"✅ {obj_key} {action}: {response_text[:50]}{'...' if len(response_text) > 50 else ''}"
    else:
        return f"❌ {obj_key} {action}: No response or action not handled"


def test_room201_tutorial():
    print("🎮 TESTING COMPLETE ROOM 201 TUTORIAL EXPERIENCE")
    print("=" * 60)
    
    # Load game
    print("Loading game...")
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    current_room = controller.get_game_object(player.location_key)
    print(f"Player location: {current_room.name} ({current_room.key_value})")
    
    print("\n📋 TESTING CORE ROOM 201 OBJECTS")
    print("-" * 40)
    
    # Test all objects from GameInteractions.txt
    tests = [
        # Purple handprints
        ("room201-purpleHandPrints", "wipe", ["hand prints", "stay"]),
        ("room201-purpleHandPrints", "clean", ["hand prints", "stay"]),
        
        # Couch interactions
        ("room201-couch", "sit", ["sit", "couch"]),
        ("room201-couch", "stand", ["get off", "couch"]),
        ("room201-couch", "get up", ["get off"]),
        
        # Nightstand (should redirect to drawer)
        ("room201-nightStand", "open", None),  # Should work via redirect
        
        # Genie interactions
        ("room201-genie", "rub", None),  # Should start dialogue
        ("room201-genie", "talk", None), # Should start dialogue
    ]
    
    for obj_key, action, expected in tests:
        result = test_object_interaction(controller, obj_key, action, expected)
        print(result)
    
    print("\n🗂️  TESTING CONTAINER SYSTEM")
    print("-" * 40)
    
    # Test container interactions
    cushions = controller.get_game_object("room201-couch-cushions")
    if cushions:
        print(f"✅ Found couch cushions container: {cushions.name}")
        
        # Test if cushions contain money
        if cushions.items:
            print(f"✅ Cushions contain {len(cushions.items)} item(s):")
            for item in cushions.items:
                print(f"    - {item.name}")
        else:
            print("⚠️  Cushions are empty")
    else:
        print("❌ Couch cushions container not found")
    
    print("\n🎪 TESTING SPECIAL OBJECTS")
    print("-" * 40)
    
    # Test other Room 201 objects exist
    special_objects = [
        "room201-tv",
        "room201-bed", 
        "room201-window",
        "room201-phone",
        "room201-floor",
        "room201-cans"
    ]
    
    for obj_key in special_objects:
        obj = controller.get_game_object(obj_key)
        if obj:
            print(f"✅ Found {obj_key}: {obj.name}")
        else:
            print(f"❌ Missing {obj_key}")
    
    print("\n🎯 TESTING DIALOGUE SYSTEM")
    print("-" * 40)
    
    # Test genie dialogue loading
    genie = controller.get_game_object("room201-genie")
    if genie:
        controller.tokens = MockTokens("rub", "room201-genie", genie)
        controller.response = []
        
        try:
            result = dispatch_object_action(controller, genie)
            if hasattr(controller, 'dialogue_graph') and controller.dialogue_graph:
                print("✅ Genie dialogue system loaded successfully")
                print(f"    Root node ID: {controller.dialogue_graph.root_node_id}")
                print(f"    Total nodes: {len(controller.dialogue_graph.nodes)}")
            else:
                print("⚠️  Genie action executed but dialogue not properly set")
        except Exception as e:
            print(f"❌ Genie dialogue error: {e}")
    
    print("\n💰 TESTING MONEY MECHANICS")
    print("-" * 40)
    
    # Check if money is properly placed
    money = controller.get_game_object("room201-coins")
    if money:
        print(f"✅ Found money: {money.name}")
        print(f"    Location: {money.location_key}")
        print(f"    Description: {money.describe()}")
    else:
        print("❌ Money not found")
    
    print("\n🎮 TUTORIAL SYSTEM TEST COMPLETE")
    print("=" * 60)
    
    # Summary
    total_objects = len([obj for obj in gamemap["items"].values() if obj.location_key == "room201"])
    print(f"📊 Room 201 contains {total_objects} interactive objects")
    print("🎯 Ready for player tutorial experience!")


if __name__ == "__main__":
    test_room201_tutorial()