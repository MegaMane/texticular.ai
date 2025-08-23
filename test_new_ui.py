#!/usr/bin/env python3
"""
Test the new fixed-layout UI with the actual game
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map

def main():
    """Test the new UI with a few game commands."""
    print("🎮 Testing New Fixed Layout UI")
    print("Starting game with new interface...")
    print("Commands to try: 'look', 'sit on couch', 'i', 'go west', 'go east'")
    print("Type 'quit' to exit")
    print()
    
    # Load game
    gamemap = load_game_map("GameConfigManifest.json")
    player = gamemap["characters"]["player"]
    controller = Controller(gamemap["rooms"], player)
    
    # Start game (skip intro for testing)
    controller.response = []
    controller.commands["look"](controller)
    controller.render_game_screen()
    
    # Simple game loop for testing
    while True:
        try:
            # Get input
            user_input = controller.ui.get_input()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for testing!")
                break
            
            # Process command
            controller.user_input = user_input
            controller.response = []
            
            # Parse and execute
            parse_success = controller.parse()
            if parse_success:
                controller.tokens.direct_object = controller.get_game_object(controller.tokens.direct_object_key)
                controller.tokens.indirect_object = controller.get_game_object(controller.tokens.indirect_object_key)
                controller.handle_input()
            else:
                controller.response = [controller.tokens.response]
            
            # Update game state
            controller.clocker()
            
            # Render new screen
            controller.render_game_screen()
            
        except KeyboardInterrupt:
            print("\n👋 Game interrupted!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Continuing...")

if __name__ == "__main__":
    main()