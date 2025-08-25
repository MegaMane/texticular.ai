#!/usr/bin/env python3
"""
Test the key fixes we just made
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_loader import load_game_map
from texticular.game_controller import Controller

def test_key_fixes():
    print("🧪 TESTING KEY FIXES")
    print("=" * 40)
    
    # Load game 
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    # Test the critical commands that were failing
    test_commands = [
        "Look at the floor",
        "Look at the rabbit ears", 
        "Turn on the TV",
        "Pickup the phone",
        "Get up",
    ]
    
    for cmd in test_commands:
        print(f"\n🔧 Testing: '{cmd}'")
        controller.user_input = cmd
        controller.response = []
        
        try:
            parse_success = controller.parse()
            
            if parse_success:
                # Object resolution
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                
                print(f"   ✅ Parsed: {controller.tokens.action} {controller.tokens.direct_object.name if controller.tokens.direct_object else 'None'}")
                
                # Try to handle the command
                handled = controller.handle_input()
                
                # Show response
                if controller.response:
                    response_text = " ".join(controller.response)
                    print(f"   📝 Response: {response_text[:80]}{'...' if len(response_text) > 80 else ''}")
                else:
                    print(f"   ⚠️  No response generated")
                    
            else:
                print(f"   ❌ Parse failed: {controller.tokens.response}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")
    
    print(f"\n🎯 Quick parser test:")
    floor_found = controller.parser.find_game_object(["floor"])
    rabbit_found = controller.parser.find_game_object(["rabbit", "ears"])
    print(f"   Floor found: {'✅' if floor_found else '❌'}")
    print(f"   Rabbit ears found: {'✅' if rabbit_found else '❌'}")

if __name__ == "__main__":
    test_key_fixes()