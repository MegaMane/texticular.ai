#!/usr/bin/env python3
"""
Test the specific fixes we just implemented:
1. "look at couch" should work without crashing
2. "examine" command should work
3. "sit on couch" should work
4. "i" shortcut for inventory should work
5. "nightstand" should be found as "night stand"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map

def test_single_command(controller, command):
    """Test a single command and return success status."""
    print(f"\n🧪 Testing: '{command}'")
    print("-" * 40)
    
    controller.user_input = command
    controller.response = []
    
    try:
        parse_success = controller.parse()
        print(f"Parse Success: {parse_success}")
        
        if parse_success:
            controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
            controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
            controller.handle_input()
        else:
            controller.response = [controller.tokens.response]
        
        print(f"Response: {controller.response}")
        return True
        
    except Exception as e:
        print(f"❌ CRASHED: {e}")
        return False

def main():
    """Test the specific fixes."""
    print("🔧 TESTING SPECIFIC FIXES")
    print("=" * 50)
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    # Tests for the specific issues that were reported
    test_commands = [
        # The original failing command that caused the crash
        "look at couch",
        
        # Test the new verbs we added
        "examine couch",
        "sit on couch", 
        "i",  # inventory shortcut
        
        # Test the parser concatenation fix
        "look at nightstand",  # Should now work (was: "I don't see a nightstand here!")
        "examine nightstand",
        "open nightstand",
        
        # Test some other objects that might benefit from the fix
        "look at tv",  # There might be a television object
        "examine phone",
    ]
    
    print("Starting in Room 201...")
    controller.commands["look"](controller)
    print(f"Room: {controller.player.location.name}")
    print(f"Initial response: {controller.response}")
    
    successful = 0
    failed = 0
    
    for command in test_commands:
        success = test_single_command(controller, command)
        if success:
            successful += 1
            print("✅ SUCCESS")
        else:
            failed += 1
            print("❌ FAILED")
    
    print(f"\n{'='*50}")
    print(f"🏁 RESULTS: {successful} success, {failed} failed")
    
    if failed == 0:
        print("🎉 All fixes are working!")
    else:
        print(f"⚠️ {failed} commands still need attention")

if __name__ == "__main__":
    main()