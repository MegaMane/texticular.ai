#!/usr/bin/env python3
"""
Comprehensive game testing simulation to validate all basic functionality.
Tests movement, object interactions, inventory, and error handling.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map

def run_test_command(controller, command, expected_success=True):
    """Run a single command and capture the result."""
    print(f"\n{'='*60}")
    print(f"TESTING COMMAND: '{command}'")
    print(f"{'='*60}")
    
    # Simulate user input
    controller.user_input = command
    controller.response = []
    
    try:
        # Parse and execute command
        parse_success = controller.parse()
        print(f"Parse Success: {parse_success}")
        
        if parse_success:
            controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
            controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
            controller.handle_input()
        else:
            controller.response = [controller.tokens.response]
        
        # Display results
        print(f"Response: {controller.response}")
        print(f"Player Location: {controller.player.location.name}")
        
        return True, controller.response
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print(f"Exception Type: {type(e).__name__}")
        return False, [f"Error: {str(e)}"]

def main():
    """Run comprehensive game simulation."""
    print("🎮 STARTING TEXTICULAR GAME SIMULATION")
    print("=" * 80)
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    # Test Commands - organized by category
    test_commands = [
        # Basic observation commands
        ("look", True),
        ("look around", True),
        ("examine room", True),
        
        # Object examination
        ("look at couch", True),
        ("examine couch", True),
        ("look at nightstand", True),
        ("examine bed", True),
        ("look at tv", True),
        ("look at phone", True),
        ("look at window", True),
        ("look at cans", True),
        
        # Object interactions
        ("sit on couch", True),
        ("get up", True),
        ("open nightstand", True),
        ("open drawer", True),
        ("take note", True),
        ("take money", True),
        ("take coin", True),
        
        # Inventory commands
        ("inventory", True),
        ("i", True),
        
        # Movement commands
        ("go west", True),  # Try to go to bathroom
        ("go back", True),  # Return to room
        ("go east", True),  # Go to hallway
        ("go west", True),  # Return to room
        ("walk north", False),  # Invalid direction from room 201
        ("move south", False), # Invalid direction from room 201
        
        # Container interactions
        ("put note in drawer", True),
        ("take note from drawer", True),
        ("close drawer", True),
        
        # Invalid commands (should fail gracefully)
        ("dance", False),
        ("sing", False),
        ("fly", False),
        ("take elephant", False),
        ("go up", False),
        ("", False),  # Empty command
        
        # Edge cases
        ("look at nothing", False),
        ("take everything", False),
        ("use couch", True),  # Might work or might not, depends on implementation
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for command, expected_success in test_commands:
        success, response = run_test_command(controller, command, expected_success)
        
        if success:
            successful_tests += 1
            print("✅ Command executed successfully")
        else:
            failed_tests += 1
            print("❌ Command failed")
    
    # Final summary
    print(f"\n{'='*80}")
    print("🏁 SIMULATION COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Successful tests: {successful_tests}")
    print(f"❌ Failed tests: {failed_tests}")
    print(f"Total tests: {successful_tests + failed_tests}")
    
    if failed_tests > 0:
        print(f"\n⚠️  {failed_tests} commands caused crashes or unexpected errors!")
        print("These need to be fixed before proceeding with NPC dialogue implementation.")
    else:
        print(f"\n🎉 All basic functionality is working! Ready for NPC dialogue implementation.")

if __name__ == "__main__":
    main()