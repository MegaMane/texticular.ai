#!/usr/bin/env python3
"""
Debug and test the money/couch issues
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map
from texticular.game_object import GameObject

def debug_couch_and_money():
    """Debug the couch and money issues."""
    print("🔍 DEBUGGING COUCH AND MONEY ISSUES")
    print("=" * 50)
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    print("🛋️ COUCH INVESTIGATION:")
    couch = GameObject.objects_by_key.get("room201-couch")
    if couch:
        print(f"  - Couch found: {couch.name}")
        print(f"  - Type: {type(couch)}")
        print(f"  - Items inside: {[item.name for item in couch.items] if hasattr(couch, 'items') else 'No items attr'}")
        if hasattr(couch, 'items'):
            for item in couch.items:
                print(f"    * {item.name} ({item.key_value})")
        
        # Test opening couch
        controller.user_input = "open couch"
        controller.response = []
        try:
            parse_success = controller.parse()
            if parse_success:
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                controller.handle_input()
            else:
                controller.response = [controller.tokens.response]
            print(f"  - Open couch response: {controller.response}")
        except Exception as e:
            print(f"  - Open couch ERROR: {e}")
    else:
        print("  - ❌ Couch not found!")
    
    print("\n💰 MONEY INVESTIGATION:")
    
    # Look for any money-related items
    money_items = []
    for key, obj in GameObject.objects_by_key.items():
        if any(word in key.lower() or word in obj.name.lower() for word in ['coin', 'money', 'cent', 'cash', 'change']):
            money_items.append((key, obj))
    
    if money_items:
        print("  - Money items found:")
        for key, obj in money_items:
            print(f"    * {obj.name} ({key}) at {obj.location_key}")
    else:
        print("  - ❌ No money items found in game!")
    
    print("\n🗄️ NIGHTSTAND INVESTIGATION:")
    nightstand = GameObject.objects_by_key.get("room201-nightStand")
    drawer = GameObject.objects_by_key.get("room201-nightStand-drawer")
    
    if nightstand:
        print(f"  - Nightstand found: {nightstand.name}")
        print(f"  - Description: {nightstand.describe()}")
    else:
        print("  - ❌ Nightstand not found!")
    
    if drawer:
        print(f"  - Drawer found: {drawer.name}")
        print(f"  - Items in drawer: {[item.name for item in drawer.items] if hasattr(drawer, 'items') else 'No items'}")
        if hasattr(drawer, 'items'):
            for item in drawer.items:
                print(f"    * {item.name} ({item.key_value})")
    else:
        print("  - ❌ Drawer not found!")
    
    print("\n🧪 INTERACTION TESTS:")
    test_commands = [
        "examine couch",
        "look in couch",
        "open nightstand", 
        "look in drawer",
        "take coins",
        "search couch",
        "look under cushions"
    ]
    
    for cmd in test_commands:
        controller.user_input = cmd
        controller.response = []
        try:
            parse_success = controller.parse()
            if parse_success:
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                controller.handle_input()
            else:
                controller.response = [controller.tokens.response]
            print(f"  '{cmd}': {controller.response}")
        except Exception as e:
            print(f"  '{cmd}': ERROR - {e}")

if __name__ == "__main__":
    debug_couch_and_money()