#!/usr/bin/env python3
"""
Demo of NPC Dialogue System
Demonstrates complete janitor interaction flow without full game setup
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.texticular.character import NPC
from src.texticular.npc_manager import NPCManager
from src.texticular.ui.fixed_layout_ui import FixedLayoutUI
from src.texticular.game_object import GameObject


class DialogueDemo:
    """Demonstrate NPC dialogue system functionality."""
    
    def __init__(self):
        # Clear any existing objects to avoid conflicts
        GameObject.objects_by_key.clear()
        
        self.npc_manager = NPCManager()
        self.ui = FixedLayoutUI()
        self.setup_janitor()
    
    def setup_janitor(self):
        """Create and register the janitor NPC."""
        self.janitor = NPC(
            key_value="demo_janitor",
            name="Hank (Janitor)",
            descriptions={"Main": "A grizzled janitor in stained overalls, mopping the floor with methodical precision."},
            location_key="eastHallway",
            synonyms=["janitor", "custodian", "cleaner", "hank"],
            adjectives=["gruff", "weathered"],
            dialogue_file="janitor_dialogue.json"
        )
        
        self.npc_manager.register_npc(self.janitor)
        print("✅ Janitor NPC created and registered successfully")
        print(f"   Name: {self.janitor.name}")
        print(f"   Location: {self.janitor.location_key}")
        print(f"   Dialogue file: {self.janitor.dialogue_file}")
    
    def start_demo_conversation(self):
        """Start a conversation and let user navigate through it."""
        player_id = "demo_player"
        
        print("\n🎭 Starting conversation with janitor...")
        conversation = self.npc_manager.start_conversation(player_id, "demo_janitor")
        
        if not conversation:
            print("❌ Failed to start conversation")
            return
        
        print("✅ Conversation started successfully")
        
        # Interactive dialogue loop
        while True:
            current_node = conversation.current_node()
            
            # Display dialogue interface
            print("\n" + "="*80)
            self.ui.display_dialogue_interface(
                npc_name=self.janitor.name,
                dialogue_text=current_node.text,
                choices=[choice.text for choice in current_node.choices]
            )
            
            # Check if conversation has ended
            if not current_node.choices:
                print("\n💬 Conversation ended.")
                self.npc_manager.end_conversation(player_id)
                break
            
            # Get user input
            try:
                print(f"\nChoices (1-{len(current_node.choices)}) or 'quit' to end:")
                user_input = input("🎮 Your choice: ").strip().lower()
                
                if user_input in ['quit', 'q', 'exit']:
                    print("👋 Ending conversation...")
                    self.npc_manager.end_conversation(player_id)
                    break
                
                try:
                    choice_num = int(user_input)
                    if 1 <= choice_num <= len(current_node.choices):
                        choice_made = self.npc_manager.make_dialogue_choice(player_id, choice_num - 1)
                        if not choice_made:
                            print("❌ Invalid choice. Please try again.")
                    else:
                        print(f"❌ Please enter a number between 1 and {len(current_node.choices)}")
                except ValueError:
                    print("❌ Please enter a number or 'quit'")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Goodbye!")
                break
    
    def demonstrate_key_paths(self):
        """Demonstrate key dialogue paths programmatically."""
        print("\n🎯 Demonstrating Key Dialogue Paths")
        print("="*60)
        
        player_id = "demo_player_2"
        
        # Path 1: Direct money request leading to deal
        print("\n📍 Path 1: Direct Money Request → Deal Acceptance")
        conversation = self.npc_manager.start_conversation(player_id, "demo_janitor")
        
        if conversation:
            print(f"Start: {conversation.current_node().text[:60]}...")
            
            # Choice 2: "Do you have any money I could borrow?"
            self.npc_manager.make_dialogue_choice(player_id, 2)
            print(f"After money request: {conversation.current_node().text[:60]}...")
            
            # Choice 0: "What do you want in return?"
            self.npc_manager.make_dialogue_choice(player_id, 0)
            print(f"After asking about deal: {conversation.current_node().text[:60]}...")
            
            # Choice 2: "Deal! Where's this supply closet?"
            self.npc_manager.make_dialogue_choice(player_id, 2)
            print(f"After accepting deal: {conversation.current_node().text[:60]}...")
            
            # Final choice
            if conversation.current_node().choices:
                self.npc_manager.make_dialogue_choice(player_id, 0)
                final_text = conversation.current_node().text
                print(f"Deal complete: {final_text[:60]}...")
                
        self.npc_manager.end_conversation(player_id)
        
        # Path 2: Bathroom info request
        print("\n📍 Path 2: Bathroom Information Request")
        conversation = self.npc_manager.start_conversation(player_id, "demo_janitor")
        
        if conversation:
            # Choice 1: "I need to find a bathroom urgently!"
            self.npc_manager.make_dialogue_choice(player_id, 1)
            print(f"Urgent request: {conversation.current_node().text[:60]}...")
            
            # Choice 1: "Where's the nearest bathroom?"
            if len(conversation.current_node().choices) > 1:
                self.npc_manager.make_dialogue_choice(player_id, 1)
                print(f"Bathroom info: {conversation.current_node().text[:60]}...")
                
        self.npc_manager.end_conversation(player_id)
        
        print("\n✅ Key dialogue paths demonstrated successfully")
    
    def show_dialogue_statistics(self):
        """Show statistics about the loaded dialogue."""
        if "demo_janitor" in self.npc_manager.dialogue_graphs:
            dialogue = self.npc_manager.dialogue_graphs["demo_janitor"]
            nodes = dialogue.nodes()
            
            print(f"\n📊 Dialogue Statistics for {self.janitor.name}")
            print("="*50)
            print(f"Total nodes: {len(nodes)}")
            
            # Count nodes by type
            ending_nodes = len([n for n in nodes if not n.choices])
            branching_nodes = len([n for n in nodes if len(n.choices) > 2])
            
            print(f"Ending nodes: {ending_nodes}")
            print(f"Branching nodes (>2 choices): {branching_nodes}")
            
            # Show all available paths from START
            start_node = next((n for n in nodes if n.node_id == "START"), None)
            if start_node:
                print(f"Starting choices: {len(start_node.choices)}")
                for i, choice in enumerate(start_node.choices):
                    print(f"  {i+1}. {choice.text[:50]}...")
    
    def run_demo(self):
        """Run the complete demo."""
        print("🎮 NPC Dialogue System Demo")
        print("="*60)
        print("This demo showcases the complete NPC dialogue system")
        print("including conversation management, choice navigation,")
        print("and UI integration with the janitor character.")
        print("="*60)
        
        # Show dialogue statistics
        self.show_dialogue_statistics()
        
        # Demonstrate key paths
        self.demonstrate_key_paths()
        
        # Interactive demo
        print(f"\n🎯 Ready for interactive dialogue with {self.janitor.name}!")
        print("Use the number keys to make choices, or type 'quit' to exit.")
        
        try:
            self.start_demo_conversation()
        except KeyboardInterrupt:
            print("\n👋 Demo ended by user")
        
        print("\n🎉 Demo completed successfully!")
        print("The NPC dialogue system is fully functional and ready for integration.")


if __name__ == "__main__":
    demo = DialogueDemo()
    demo.run_demo()