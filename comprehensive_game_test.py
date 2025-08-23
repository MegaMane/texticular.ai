#!/usr/bin/env python3
"""
Comprehensive test of all basic game functionality
Tests everything from basic interactions to vending machine flow
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map

def test_basic_functionality():
    """Test all the basic game interactions that should work."""
    print("🧪 COMPREHENSIVE GAME FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    # Test categories
    test_results = {
        "basic_commands": 0,
        "object_interactions": 0,
        "inventory_system": 0,
        "room_navigation": 0,
        "vending_machine": 0,
        "parser_features": 0
    }
    
    total_tests = 0
    passed_tests = 0
    
    def run_test(command, category, should_succeed=True):
        nonlocal total_tests, passed_tests
        total_tests += 1
        
        controller.user_input = command
        controller.response = []
        
        try:
            parse_success = controller.parse()
            if parse_success:
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                controller.handle_input()
            else:
                controller.response = [controller.tokens.response]
            
            # Check if test passed
            if should_succeed:
                success = parse_success and not any("error" in str(r).lower() for r in controller.response)
            else:
                success = not parse_success  # Should fail
                
            if success:
                passed_tests += 1
                test_results[category] += 1
                print(f"✅ '{command}' - PASS")
            else:
                print(f"❌ '{command}' - FAIL: {controller.response}")
                
            return success
            
        except Exception as e:
            print(f"💥 '{command}' - CRASH: {e}")
            return False
    
    # BASIC COMMANDS
    print("\n📋 Testing Basic Commands...")
    run_test("look", "basic_commands")
    run_test("examine room", "basic_commands", False)  # Should fail gracefully
    run_test("inventory", "basic_commands")
    run_test("i", "basic_commands")
    
    # PARSER FEATURES  
    print("\n🔤 Testing Parser Features...")
    run_test("examine couch", "parser_features")
    run_test("search couch", "parser_features") 
    run_test("look at nightstand", "parser_features")  # Tests concatenation fix
    run_test("sit on couch", "parser_features")
    
    # OBJECT INTERACTIONS
    print("\n🎯 Testing Object Interactions...")
    run_test("open couch", "object_interactions")
    run_test("take coins", "object_interactions")
    run_test("open drawer", "object_interactions")  
    run_test("close drawer", "object_interactions")
    run_test("take ear plugs", "object_interactions")
    
    # INVENTORY SYSTEM
    print("\n🎒 Testing Inventory System...")
    run_test("inventory", "inventory_system")
    run_test("drop coins", "inventory_system")
    run_test("take coins", "inventory_system")
    
    # ROOM NAVIGATION
    print("\n🚪 Testing Room Navigation...")
    run_test("go east", "room_navigation")    # To hallway
    run_test("look", "room_navigation")       # See hallway
    run_test("go south", "room_navigation")   # To vending machine
    run_test("look", "room_navigation")       # See vending area
    run_test("go north", "room_navigation")   # Back to hallway
    run_test("go west", "room_navigation")    # Back to room 201
    run_test("go east", "room_navigation")    # To hallway again
    run_test("go south", "room_navigation")   # To vending machine again
    
    # VENDING MACHINE FLOW
    print("\n🤖 Testing Vending Machine...")
    run_test("examine vending machine", "vending_machine")
    run_test("use vending machine", "vending_machine")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🏁 COMPREHENSIVE TEST RESULTS")
    print(f"{'='*60}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print(f"\n📊 Category Breakdown:")
    for category, count in test_results.items():
        print(f"  {category.replace('_', ' ').title()}: {count} tests passed")
    
    # Final inventory check
    inventory = []
    if hasattr(controller.player, 'inventory') and hasattr(controller.player.inventory, 'items'):
        inventory = [item.name for item in controller.player.inventory.items]
    print(f"\nFinal Inventory: {inventory}")
    print(f"Final Location: {controller.player.location.name}")
    
    if passed_tests == total_tests:
        print(f"\n🎉 PERFECT SCORE! All {total_tests} tests passed!")
        print("The game is ready for NPC dialogue implementation!")
    elif passed_tests >= total_tests * 0.9:
        print(f"\n🎊 EXCELLENT! {passed_tests}/{total_tests} tests passed ({(passed_tests/total_tests)*100:.1f}%)")
        print("Just a few minor issues to clean up.")
    else:
        print(f"\n⚠️  NEEDS WORK: Only {passed_tests}/{total_tests} tests passed ({(passed_tests/total_tests)*100:.1f}%)")
        print("Several core issues need fixing before proceeding.")

if __name__ == "__main__":
    test_basic_functionality()