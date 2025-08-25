#!/usr/bin/env python3
"""
Test genie dialogue
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_loader import load_game_map
from texticular.game_controller import Controller

def test_genie():
    print("🧞‍♂️ TESTING GENIE DIALOGUE")
    print("=" * 40)
    
    # Load game 
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap, player)
    
    cmd = "Talk genie"
    print(f"🔧 Testing: '{cmd}'")
    controller.user_input = cmd
    controller.response = []
    
    try:
        parse_success = controller.parse()
        
        if parse_success:
            # Object resolution
            controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
            controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
            
            print(f"   ✅ Parsed: {controller.tokens.action}")
            if controller.tokens.direct_object:
                print(f"   📦 Direct object: {controller.tokens.direct_object.name}")
            if controller.tokens.indirect_object:
                print(f"   📦 Indirect object: {controller.tokens.indirect_object.name}")
            
            # Try to handle the command
            handled = controller.handle_input()
            
            # Show response
            if controller.response:
                response_text = " ".join(controller.response)
                print(f"   📝 Response: {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
                
                # Check if dialogue started
                if hasattr(controller, 'dialogue_graph') and controller.dialogue_graph:
                    print(f"   🎭 Dialogue started successfully!")
                    print(f"   🎭 Current node: {controller.dialogue_graph.current_node().node_id}")
                else:
                    print(f"   ⚠️  Dialogue not started")
                    
            else:
                print(f"   ⚠️  No response generated")
                
        else:
            print(f"   ❌ Parse failed: {controller.tokens.response}")
            
    except Exception as e:
        print(f"   💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_genie()