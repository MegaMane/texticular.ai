#!/usr/bin/env python3
"""
Test TV channel functionality
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_loader import load_game_map
from texticular.game_controller import Controller

def test_tv_channels():
    print("📺 TESTING TV CHANNEL FUNCTIONALITY")
    print("=" * 50)
    
    # Load game 
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    # Test TV commands
    test_commands = [
        ("Turn on TV", "Should turn on TV and show first channel"),
        ("Change channel", "Should switch to next channel"),
        ("Change channel", "Should switch to next channel again"),
        ("Change channel", "Should switch to next channel again"),
        ("Change channel", "Should wrap back to first channel"),
        ("Watch TV", "Should show current channel content"),
        ("Turn off TV", "Should turn off TV"),
        ("Watch TV", "Should show TV is off"),
    ]
    
    for cmd, expected in test_commands:
        print(f"\n🧪 Testing: '{cmd}'")
        print(f"   Expected: {expected}")
        
        controller.user_input = cmd
        controller.response = []
        
        try:
            parse_success = controller.parse()
            
            if parse_success:
                # Object resolution
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                
                # Try to handle the command
                handled = controller.handle_input()
                
                # Show response
                if controller.response:
                    response_text = " ".join(controller.response)
                    print(f"   📝 Response: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
                else:
                    print(f"   ⚠️  No response generated")
                    
            else:
                print(f"   ❌ Parse failed: {controller.tokens.response}")
                
        except Exception as e:
            print(f"   💥 Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_tv_channels()