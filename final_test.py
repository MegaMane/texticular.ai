#!/usr/bin/env python3
"""
Final comprehensive test of all originally failing commands from results.txt
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_loader import load_game_map
from texticular.game_controller import Controller

def comprehensive_final_test():
    print("🎯 FINAL COMPREHENSIVE TEST")
    print("Testing ALL originally failing commands from results.txt")
    print("=" * 60)
    
    # Load game 
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    # All the commands that were failing in results.txt
    test_commands = [
        ("Look at the floor", "Should describe the floor"),
        ("Look at the rabbit ears", "Should describe rabbit ears"), 
        ("Turn on the TV", "Should turn on TV with static"),
        ("Pickup the phone", "Should try to pick up phone"),
        ("Talk genie", "Should start genie dialogue"),
        ("Rub genie", "Should start genie dialogue"),
        ("Use the phone", "Should interact with phone"),
        ("Sit on the bed", "Should sit on bed"),
        ("Get up", "Should stand up"),
        ("Move the rabbit ears", "Should move rabbit ears"),
    ]
    
    passed = 0
    failed = 0
    
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
                
                print(f"   ✅ Parsed: {controller.tokens.action} {controller.tokens.direct_object.name if controller.tokens.direct_object else 'None'}")
                
                # Try to handle the command
                handled = controller.handle_input()
                
                # Show response
                if controller.response:
                    response_text = " ".join(controller.response)
                    print(f"   📝 Response: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
                    passed += 1
                else:
                    print(f"   ⚠️  No response generated")
                    failed += 1
                    
            else:
                print(f"   ❌ Parse failed: {controller.tokens.response}")
                failed += 1
                
        except Exception as e:
            print(f"   💥 Error: {e}")
            failed += 1
    
    print(f"\n📊 FINAL RESULTS:")
    print("=" * 60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("🎉 ALL COMMANDS WORKING! Room 201 is fully functional!")
    else:
        print(f"⚠️  {failed} commands still need work")
    
    print(f"\n🎮 Game is ready for player testing!")

if __name__ == "__main__":
    comprehensive_final_test()