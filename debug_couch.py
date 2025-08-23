#!/usr/bin/env python3
"""Debug the couch sitting issue in detail."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map
from texticular.game_object import GameObject

def main():
    print("🔍 DEBUGGING COUCH SITTING CRASH")
    print("=" * 50)
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    # Get the couch object
    couch = GameObject.objects_by_key.get("room201-couch")
    if not couch:
        print("❌ Couch not found!")
        return
    
    print(f"Found couch: {couch.name}")
    print(f"Couch type: {type(couch)}")
    print(f"Couch descriptions: {couch.descriptions}")
    print(f"Current description: {couch.current_description}")
    print(f"Has 'Sitting' key: {'Sitting' in couch.descriptions}")
    
    # Test the exact line that's failing
    print("\n🧪 Testing direct description assignment...")
    try:
        print("Before: couch.current_description =", repr(couch.current_description))
        couch.current_description = "Sitting"
        print("After: couch.current_description =", repr(couch.current_description))
        print("✅ Direct assignment worked!")
    except Exception as e:
        print(f"❌ Direct assignment failed: {e}")
        return
    
    # Now test the action method call
    print("\n🧪 Testing action method call...")
    controller.user_input = "sit on couch"
    controller.response = []
    
    try:
        parse_success = controller.parse()
        print(f"Parse success: {parse_success}")
        print(f"Action: {controller.tokens.action}")
        print(f"Direct object key: {controller.tokens.direct_object_key}")
        
        if parse_success:
            controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
            controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
            
            print(f"Direct object: {controller.tokens.direct_object}")
            print(f"Direct object type: {type(controller.tokens.direct_object)}")
            
            # Call the specific action method
            target = controller.tokens.direct_object
            if hasattr(target, 'action') and target.action_method_name:
                print(f"Action method: {target.action_method_name}")
                result = target.action(controller=controller, target=target)
                print(f"Action result: {result}")
            else:
                print("No action method found")
                
        print(f"Final response: {controller.response}")
        
    except Exception as e:
        print(f"❌ Action method crashed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()