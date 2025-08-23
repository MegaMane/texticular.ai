#!/usr/bin/env python3
"""
Test the complete vending machine flow:
1. Find money in couch
2. Take money
3. Go to vending machine
4. Use vending machine
5. Buy something
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map

def test_command(controller, command, expected_success=True):
    """Test a single command and show results."""
    print(f"\n🧪 Testing: '{command}'")
    print("-" * 40)
    
    controller.user_input = command
    controller.response = []
    
    try:
        # Track old location for movement detection
        old_room = controller.player.location.name
        
        # Parse and execute
        parse_success = controller.parse()
        if parse_success:
            controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
            controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
            controller.handle_input()
        else:
            controller.response = [controller.tokens.response]
        
        # Show results
        print(f"Parse Success: {parse_success}")
        print(f"Response: {controller.response}")
        print(f"Room: {controller.player.location.name}")
        
        # Check for room change
        if old_room != controller.player.location.name:
            print(f"🚪 Moved: {old_room} → {controller.player.location.name}")
        
        # Show inventory if it changed
        inventory = []
        if hasattr(controller.player, 'inventory') and hasattr(controller.player.inventory, 'items'):
            inventory = [item.name for item in controller.player.inventory.items]
        if inventory:
            print(f"🎒 Inventory: {inventory}")
        
        print("✅ SUCCESS" if parse_success else "⚠️  PARSE FAILED")
        return True
        
    except Exception as e:
        print(f"❌ CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test the complete vending machine workflow."""
    print("🎮 TESTING COMPLETE VENDING MACHINE FLOW")
    print("=" * 60)
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    # Start in Room 201
    controller.response = []
    controller.commands["look"](controller)
    print(f"Starting Room: {controller.player.location.name}")
    print(f"Initial Description: {controller.response}")
    
    # Test sequence
    test_sequence = [
        # Step 1: Discover the couch hint
        "look",
        "examine couch",
        
        # Step 2: Try different ways to get money
        "search couch",
        "open couch", 
        "look in couch",
        
        # Step 3: Take the money
        "take coins",
        "take money", 
        "inventory",
        
        # Step 4: Navigate to vending machine
        "go east",  # To hallway
        "look",     # See where we are
        "go south", # To vending machine
        "look",     # See vending machine
        
        # Step 5: Examine and use vending machine
        "examine vending machine",
        "look at vending machine",
        "use vending machine",
        
        # Step 6: Try to buy something (this might enter vending machine mode)
        "buy fast eddie",
        "insert coins",
        "put coins in machine",
        
        # Navigation back (if needed)
        "quit vending machine",
        "go back",
        "go north",
    ]
    
    successful_tests = 0
    failed_tests = 0
    
    for command in test_sequence:
        success = test_command(controller, command)
        if success:
            successful_tests += 1
        else:
            failed_tests += 1
            print(f"⚠️  Continuing after error with '{command}'...")
    
    # Final summary
    print(f"\n{'='*60}")
    print(f"🏁 VENDING MACHINE FLOW TEST COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful commands: {successful_tests}")
    print(f"❌ Failed commands: {failed_tests}")
    print(f"Total commands tested: {successful_tests + failed_tests}")
    
    # Final game state
    print(f"\nFinal Room: {controller.player.location.name}")
    inventory = []
    if hasattr(controller.player, 'inventory') and hasattr(controller.player.inventory, 'items'):
        inventory = [item.name for item in controller.player.inventory.items]
    print(f"Final Inventory: {inventory}")
    
    if failed_tests == 0:
        print("\n🎉 COMPLETE SUCCESS! Vending machine flow is working!")
    else:
        print(f"\n⚠️  {failed_tests} issues found that need fixing.")

if __name__ == "__main__":
    main()