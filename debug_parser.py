#!/usr/bin/env python3
"""
Debug parser object matching for Room 201 issues
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_loader import load_game_map
from texticular.game_controller import Controller

def debug_parser_objects():
    print("🔍 DEBUGGING PARSER OBJECT MATCHING")
    print("=" * 50)
    
    # Load game 
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    print(f"Player location: {player.location_key}")
    
    # Check what objects the parser knows about
    parser_objects = controller.parser.game_objects
    
    print(f"\n📋 Parser knows about {len(parser_objects)} objects:")
    
    # Look specifically for floor-related objects
    floor_objects = {k: v for k, v in parser_objects.items() if 'floor' in k.lower()}
    print(f"\n🔍 Floor-related objects found: {len(floor_objects)}")
    for key, matches in floor_objects.items():
        print(f"  {key}: {matches}")
    
    # Test specific searches that are failing
    test_searches = ["floor", "rabbit ears", "genie", "tv"]
    
    print(f"\n🧪 Testing object searches:")
    for search_term in test_searches:
        found_key = controller.parser.find_game_object([search_term])
        if found_key:
            obj = controller.get_game_object(found_key)
            print(f"✅ '{search_term}' → {found_key} ({obj.name if obj else 'None'})")
        else:
            print(f"❌ '{search_term}' → Not found")
    
    # Check if floor object actually exists in GameObject registry
    print(f"\n🗂️  Checking GameObject registry:")
    from texticular.game_object import GameObject
    floor_key = "room201-floor"
    floor_obj = GameObject.objects_by_key.get(floor_key)
    if floor_obj:
        print(f"✅ {floor_key} exists in GameObject registry")
        print(f"   Name: {floor_obj.name}")
        print(f"   Synonyms: {getattr(floor_obj, 'synonyms', 'N/A')}")
        print(f"   Adjectives: {getattr(floor_obj, 'adjectives', 'N/A')}")
    else:
        print(f"❌ {floor_key} NOT in GameObject registry")
    
    # Test the parser matching logic directly
    print(f"\n⚙️  Direct parser test:")
    test_input = "look at the floor"
    tokens = controller.parser.parse_input(test_input)
    print(f"Input: '{test_input}'")
    print(f"Parsed action: {tokens.action}")
    print(f"Direct object key: {tokens.direct_object_key}")
    print(f"Parse successful: {tokens.input_parsed}")
    print(f"Response: {tokens.response}")

if __name__ == "__main__":
    debug_parser_objects()