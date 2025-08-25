#!/usr/bin/env python3
"""
Comprehensive test simulating the failing commands from results.txt
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_loader import load_game_map
from texticular.game_controller import Controller

def test_failing_commands():
    print("🔥 COMPREHENSIVE TEST OF FAILING COMMANDS")
    print("=" * 60)
    
    # Load game 
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    # Commands that are failing according to results.txt
    failing_commands = [
        "Look at the floor",
        "Look at the rabbit ears", 
        "Turn on the TV",
        "Pickup the phone",
        "Talk to the genie",
        "Use the phone",
        "Sit on the bed",
        "Get up",
        "Move the rabbit ears"
    ]
    
    print("Testing each failing command:")
    print("-" * 40)
    
    for cmd in failing_commands:
        print(f"\n🧪 Command: '{cmd}'")
        controller.user_input = cmd
        controller.response = []
        
        # Simulate the full game loop
        try:
            parse_success = controller.parse()
            print(f"   Parse success: {parse_success}")
            
            if parse_success:
                # Object resolution
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                
                print(f"   Action: {controller.tokens.action}")
                print(f"   Direct object: {controller.tokens.direct_object.name if controller.tokens.direct_object else 'None'}")
                
                # Try to handle the command
                handled = controller.handle_input()
                print(f"   Command handled: {handled}")
                
            else:
                print(f"   Parse failed: {controller.tokens.response}")
            
            # Show response
            if controller.response:
                response_text = " ".join(controller.response)
                print(f"   Response: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
            else:
                print("   Response: (no response)")
                
        except Exception as e:
            print(f"   💥 CRASHED: {e}")
    
    print(f"\n📊 SUMMARY OF MAJOR ISSUES FOUND:")
    print("=" * 60)
    
    print("🔍 PARSER ISSUES:")
    print("   • Objects not found: floor, rabbit ears (name vs synonyms bug)")
    print("   • Missing verbs: 'turn on', 'pickup'")  
    print("   • Duplicate items in rooms (loading bug)")
    
    print("\n⚙️  VERB ACTION ISSUES:")
    print("   • Duplicate sit() functions")
    print("   • No 'get up' command mapping")
    print("   • Missing verb-to-action mappings")
    
    print("\n🏗️  ARCHITECTURE ISSUES:")
    print("   • StoryItem objects only use synonyms, ignore actual name")
    print("   • Room items duplicated during loading")
    print("   • Inconsistent action method system")
    
    print("\n🎯 IMMEDIATE FIXES NEEDED:")
    print("   1. Fix parser to include object names in matching")
    print("   2. Add missing verbs to KNOWN_VERBS and command mapping")
    print("   3. Remove duplicate sit() function") 
    print("   4. Fix room item duplication bug")
    print("   5. Add 'get up' command implementation")

if __name__ == "__main__":
    test_failing_commands()