#!/usr/bin/env python3
"""
Play Texticular with gameplay logging enabled
This version logs all your actions for real-time monitoring
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.game_controller import Controller
from texticular.game_loader import load_game_map
from texticular.gameplay_logger import start_logging, stop_logging

def main():
    """Play the game with logging enabled."""
    print("🎮 TEXTICULAR - Now with Real-time Logging!")
    print("=" * 50)
    print("Your gameplay is being logged for analysis.")
    print("Open another terminal and run: python watch_gameplay.py")
    print("to see real-time monitoring of your gameplay!")
    print("=" * 50)
    print()
    
    # Start logging
    logger = start_logging("texticular_session")
    print(f"📊 Logging started: {logger.session_name}")
    print()
    
    try:
        # Load game
        gamemap = load_game_map("GameConfigManifest.json")
        player = gamemap["characters"]["player"]
        controller = Controller(gamemap["rooms"], player)
        
        # Log game start
        logger.log_event("game_start", {
            "player_name": player.name,
            "starting_room": player.location.name,
            "starting_poop_level": controller.poop_level
        })
        
        # Start game (skip intro for faster testing)
        controller.response = []
        controller.commands["look"](controller)
        controller.render_game_screen()
        
        print("💡 Try commands like: 'look', 'sit on couch', 'i', 'go west', 'take note'")
        print("Type 'quit' to exit")
        print()
        
        # Game loop
        while True:
            try:
                # Get input
                controller.get_input()
                
                if controller.user_input.lower() in ['quit', 'exit', 'q']:
                    logger.log_event("game_quit", {"reason": "player_quit"})
                    print("👋 Thanks for playing!")
                    break
                
                # Track room changes
                old_room = controller.player.location.name
                
                # Process command
                controller.update()
                
                # Check for room change
                new_room = controller.player.location.name
                if old_room != new_room:
                    logger.log_room_change(old_room, new_room)
                
                # Render new screen
                controller.render_game_screen()
                
            except KeyboardInterrupt:
                logger.log_event("game_interrupt", {"reason": "keyboard_interrupt"})
                print("\n👋 Game interrupted!")
                break
            except Exception as e:
                logger.log_error("game_crash", str(e), {
                    "command": getattr(controller, 'user_input', ''),
                    "room": controller.player.location.name if controller.player.location else "Unknown"
                })
                print(f"\n❌ Error: {e}")
                print("Game continuing...")
                
    finally:
        # Stop logging
        stop_logging()
        print("📊 Gameplay session saved!")

if __name__ == "__main__":
    main()