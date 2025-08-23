#!/usr/bin/env python3
"""
Comprehensive Test Suite for NPC Dialogue System
Tests janitor NPC interaction, dialogue flow, and integration with vending machine
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.texticular import game_loader
from src.texticular.game_controller import Controller
from src.texticular.character import Player
from src.texticular.game_object import GameObject
from src.texticular.npc_manager import get_npc_manager
from src.texticular.game_enums import GameStates


class NPCDialogueTestSuite:
    """Comprehensive test suite for NPC dialogue system."""
    
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        self.setup_game()
    
    def setup_game(self):
        """Initialize game environment for testing."""
        print("🔧 Setting up test environment...")
        
        # Clear any existing game objects
        GameObject.objects_by_key.clear()
        
        # Load game data
        game_map = game_loader.load_game_map("GameConfigManifest.json")
        
        # Set up game controller  
        player = GameObject.objects_by_key.get("player")
        rooms = {key: obj for key, obj in GameObject.objects_by_key.items() 
                if hasattr(obj, 'exits')}
        
        self.controller = Controller(rooms, player)
        self.npc_manager = get_npc_manager()
        
        print(f"✅ Game environment ready. Loaded {len(rooms)} rooms and {len(self.npc_manager.npcs)} NPCs")
    
    def run_test(self, test_name, test_func):
        """Run a single test and record results."""
        print(f"\n🧪 Running test: {test_name}")
        try:
            result = test_func()
            if result:
                print(f"✅ PASS: {test_name}")
                self.test_results.append((test_name, "PASS", None))
            else:
                print(f"❌ FAIL: {test_name}")
                self.test_results.append((test_name, "FAIL", "Test returned False"))
                self.failed_tests.append(test_name)
        except Exception as e:
            print(f"💥 ERROR: {test_name} - {str(e)}")
            self.test_results.append((test_name, "ERROR", str(e)))
            self.failed_tests.append(test_name)
    
    def test_npc_loading(self):
        """Test that NPCs are properly loaded from JSON data."""
        # Check if janitor NPC exists
        janitor = self.npc_manager.get_npc("janitor")
        if not janitor:
            print("❌ Janitor NPC not found in NPC manager")
            return False
        
        # Check janitor properties
        if janitor.name != "Janitor":
            print(f"❌ Expected janitor name 'Janitor', got '{janitor.name}'")
            return False
        
        if janitor.location_key != "eastHallway":
            print(f"❌ Expected janitor location 'eastHallway', got '{janitor.location_key}'")
            return False
        
        # Check dialogue file
        if not hasattr(janitor, 'dialogue_file') or janitor.dialogue_file != "janitor_dialogue.json":
            print(f"❌ Janitor dialogue file not properly set")
            return False
        
        print("✅ Janitor NPC loaded with correct properties")
        return True
    
    def test_dialogue_file_loading(self):
        """Test that dialogue files are properly loaded."""
        janitor_key = "janitor"
        
        # Check if dialogue graph exists
        if janitor_key not in self.npc_manager.dialogue_graphs:
            print("❌ Janitor dialogue graph not loaded")
            return False
        
        dialogue = self.npc_manager.dialogue_graphs[janitor_key]
        
        # Check root node
        if dialogue._active_node_id != "START":
            print(f"❌ Expected root node 'START', got '{dialogue._active_node_id}'")
            return False
        
        # Check if nodes exist
        nodes = dialogue.nodes()
        if not nodes:
            print("❌ No dialogue nodes found")
            return False
        
        # Check for key dialogue nodes
        node_ids = [node.node_id for node in nodes]
        required_nodes = ["START", "DEAL_ACCEPTED", "MONEY_REQUEST", "EXIT"]
        
        for required_node in required_nodes:
            if required_node not in node_ids:
                print(f"❌ Required dialogue node '{required_node}' not found")
                return False
        
        print(f"✅ Dialogue loaded with {len(nodes)} nodes including all required nodes")
        return True
    
    def test_start_conversation(self):
        """Test starting a conversation with the janitor."""
        player_id = "player"
        janitor_key = "janitor"
        
        # Start conversation
        conversation = self.npc_manager.start_conversation(player_id, janitor_key)
        
        if not conversation:
            print("❌ Failed to start conversation with janitor")
            return False
        
        # Check if conversation is active
        active_conversation = self.npc_manager.get_active_conversation(player_id)
        if not active_conversation:
            print("❌ No active conversation found after starting")
            return False
        
        # Check current node
        current_node = active_conversation.current_node()
        if not current_node:
            print("❌ No current node in active conversation")
            return False
        
        if current_node.node_id != "START":
            print(f"❌ Expected current node 'START', got '{current_node.node_id}'")
            return False
        
        # Check dialogue text
        if "Fast Eddie" not in current_node.text:
            print("❌ Expected starting dialogue to mention Fast Eddie")
            return False
        
        # Check choices
        if len(current_node.choices) < 3:
            print(f"❌ Expected at least 3 choices, got {len(current_node.choices)}")
            return False
        
        print("✅ Successfully started conversation with correct initial state")
        return True
    
    def test_dialogue_choice_navigation(self):
        """Test making choices and navigating dialogue tree."""
        player_id = "player"
        janitor_key = "janitor"
        
        # Start conversation
        conversation = self.npc_manager.start_conversation(player_id, janitor_key)
        if not conversation:
            return False
        
        # Test making a choice (choice index 2 - "Do you have any money I could borrow?")
        choice_made = self.npc_manager.make_dialogue_choice(player_id, 2)
        if not choice_made:
            print("❌ Failed to make dialogue choice")
            return False
        
        # Check new current node
        current_node = conversation.current_node()
        if current_node.node_id != "MONEY_DIRECT":
            print(f"❌ Expected node 'MONEY_DIRECT', got '{current_node.node_id}'")
            return False
        
        # Check dialogue text changed appropriately
        if "spare change" not in current_node.text.lower():
            print("❌ Expected dialogue about spare change")
            return False
        
        print("✅ Successfully navigated dialogue tree with choices")
        return True
    
    def test_deal_acceptance_path(self):
        """Test the complete deal acceptance dialogue path."""
        player_id = "player"
        janitor_key = "janitor"
        
        # Start conversation
        conversation = self.npc_manager.start_conversation(player_id, janitor_key)
        
        # Navigate to deal acceptance
        # Choice 2: "Do you have any money I could borrow?"
        self.npc_manager.make_dialogue_choice(player_id, 2)
        
        # Choice 0: "What do you want in return?"
        self.npc_manager.make_dialogue_choice(player_id, 0)
        
        # Check we're at DEAL_DETAILS
        current_node = conversation.current_node()
        if current_node.node_id != "DEAL_DETAILS":
            print(f"❌ Expected 'DEAL_DETAILS', got '{current_node.node_id}'")
            return False
        
        # Choice 2: "Deal! Where's this supply closet?"
        self.npc_manager.make_dialogue_choice(player_id, 2)
        
        # Check we reach ACCEPT_DEAL
        current_node = conversation.current_node()
        if current_node.node_id != "ACCEPT_DEAL":
            print(f"❌ Expected 'ACCEPT_DEAL', got '{current_node.node_id}'")
            return False
        
        # Final choice to complete the deal
        self.npc_manager.make_dialogue_choice(player_id, 0)
        
        # Check we reach DEAL_ACCEPTED
        current_node = conversation.current_node()
        if current_node.node_id != "DEAL_ACCEPTED":
            print(f"❌ Expected 'DEAL_ACCEPTED', got '{current_node.node_id}'")
            return False
        
        # Check if conversation ends (no choices)
        if current_node.choices:
            print("❌ Expected conversation to end (no choices) after deal accepted")
            return False
        
        print("✅ Successfully completed deal acceptance dialogue path")
        return True
    
    def test_talk_command_integration(self):
        """Test the 'talk' command integration with dialogue system."""
        # Move player to east hallway where janitor is located
        self.controller.player.go_to("eastHallway")
        
        # Test talk command
        self.controller.response = []
        self.controller.player_input = "talk to janitor"
        
        # Parse the command
        self.controller.tokens = self.controller.parser.parse_sentence(self.controller.player_input)
        
        # Check if janitor is recognized as target
        if not self.controller.tokens.direct_object:
            print("❌ Parser did not recognize janitor as target")
            return False
        
        # Execute talk command
        from texticular.actions import verb_actions as va
        result = va.talk(self.controller)
        
        if not result:
            print("❌ Talk command returned False")
            return False
        
        # Check if game state changed to dialogue
        if self.controller.gamestate != GameStates.DIALOGUESCENE:
            print(f"❌ Expected game state DIALOGUESCENE, got {self.controller.gamestate}")
            return False
        
        # Check if active NPC is set
        if not self.controller.active_npc:
            print("❌ No active NPC set after talk command")
            return False
        
        if self.controller.active_npc.key_value != "janitor":
            print(f"❌ Expected active NPC 'janitor', got '{self.controller.active_npc.key_value}'")
            return False
        
        print("✅ Talk command successfully integrated with dialogue system")
        return True
    
    def test_dialogue_ui_integration(self):
        """Test dialogue UI display integration."""
        # Start conversation
        player_id = self.controller.player.key_value
        conversation = self.npc_manager.start_conversation(player_id, "janitor")
        
        if not conversation:
            return False
        
        current_node = conversation.current_node()
        
        # Test if UI can display dialogue (should not crash)
        try:
            self.controller.ui.display_dialogue_interface(
                npc_name="Janitor",
                dialogue_text=current_node.text,
                choices=[choice.text for choice in current_node.choices]
            )
            print("✅ Dialogue UI integration successful")
            return True
        except Exception as e:
            print(f"❌ Dialogue UI integration failed: {e}")
            return False
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        player_id = "player"
        
        # Test talking to non-existent NPC
        conversation = self.npc_manager.start_conversation(player_id, "nonexistent")
        if conversation is not None:
            print("❌ Should not be able to start conversation with non-existent NPC")
            return False
        
        # Test invalid choice in dialogue
        conversation = self.npc_manager.start_conversation(player_id, "janitor")
        if conversation:
            # Try to make an invalid choice (index 99)
            choice_made = self.npc_manager.make_dialogue_choice(player_id, 99)
            if choice_made:
                print("❌ Should not be able to make invalid choice")
                return False
        
        # Test ending non-existent conversation
        self.npc_manager.end_conversation("nonexistent_player")  # Should not crash
        
        print("✅ Edge cases handled properly")
        return True
    
    def run_complete_interaction_simulation(self):
        """Simulate a complete player interaction from start to finish."""
        print("\n🎭 Running Complete Interaction Simulation")
        print("="*60)
        
        # Reset player to starting position
        self.controller.player.go_to("room201")
        self.controller.gamestate = GameStates.EXPLORATION
        
        # Step 1: Player goes to couch to find coins
        print("Step 1: Player searches couch for coins...")
        self.controller.player.go_to("room203")
        
        # Step 2: Player examines couch 
        self.controller.player_input = "examine couch"
        self.controller.tokens = self.controller.parser.parse_sentence(self.controller.player_input)
        
        # Step 3: Player sits on couch to find coins
        self.controller.player_input = "sit on couch"  
        self.controller.tokens = self.controller.parser.parse_sentence(self.controller.player_input)
        
        from texticular.actions import story_item_actions as sia
        try:
            sia.sit_on_couch(self.controller, self.controller.tokens.direct_object)
            print("✅ Player successfully found coins in couch")
        except Exception as e:
            print(f"❌ Failed to find coins in couch: {e}")
            return False
        
        # Step 4: Player goes to find janitor
        print("Step 2: Player goes to East Hallway to find janitor...")
        self.controller.player.go_to("eastHallway")
        
        # Step 5: Player talks to janitor
        print("Step 3: Player talks to janitor...")
        self.controller.player_input = "talk to janitor"
        self.controller.tokens = self.controller.parser.parse_sentence(self.controller.player_input)
        
        from texticular.actions import verb_actions as va
        result = va.talk(self.controller)
        if not result:
            print("❌ Failed to start conversation with janitor")
            return False
        
        # Step 6: Navigate dialogue to make deal
        print("Step 4: Player negotiates deal with janitor...")
        player_id = self.controller.player.key_value
        
        # Make money request
        self.npc_manager.make_dialogue_choice(player_id, 2)  # "Do you have any money..."
        self.npc_manager.make_dialogue_choice(player_id, 0)  # "What do you want in return?"
        self.npc_manager.make_dialogue_choice(player_id, 2)  # "Deal! Where's this supply closet?"
        self.npc_manager.make_dialogue_choice(player_id, 0)  # "Consider it done!"
        
        # Step 7: Check if conversation ended properly
        active_conversation = self.npc_manager.get_active_conversation(player_id)
        if active_conversation:
            print("❌ Conversation should have ended after deal acceptance")
            return False
        
        print("✅ Complete interaction simulation successful!")
        return True
    
    def run_all_tests(self):
        """Run the complete test suite."""
        print("🚀 Starting NPC Dialogue System Test Suite")
        print("="*60)
        
        # Core functionality tests
        self.run_test("NPC Loading", self.test_npc_loading)
        self.run_test("Dialogue File Loading", self.test_dialogue_file_loading)
        self.run_test("Start Conversation", self.test_start_conversation)
        self.run_test("Dialogue Choice Navigation", self.test_dialogue_choice_navigation)
        self.run_test("Deal Acceptance Path", self.test_deal_acceptance_path)
        
        # Integration tests
        self.run_test("Talk Command Integration", self.test_talk_command_integration)
        self.run_test("Dialogue UI Integration", self.test_dialogue_ui_integration)
        
        # Edge cases and error handling
        self.run_test("Edge Cases", self.test_edge_cases)
        
        # Complete simulation
        self.run_test("Complete Interaction Simulation", self.run_complete_interaction_simulation)
        
        # Print results summary
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print a summary of all test results."""
        print("\n" + "="*60)
        print("📊 TEST RESULTS SUMMARY")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r[1] == "PASS"])
        failed_tests = len([r for r in self.test_results if r[1] in ["FAIL", "ERROR"]])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.failed_tests:
            print("\n❌ FAILED TESTS:")
            for test_name in self.failed_tests:
                result = next(r for r in self.test_results if r[0] == test_name)
                print(f"  • {test_name}: {result[2] or 'Test failed'}")
        
        print("\n📋 DETAILED RESULTS:")
        for test_name, status, error in self.test_results:
            status_icon = "✅" if status == "PASS" else "❌"
            print(f"  {status_icon} {test_name}: {status}")
            if error and status != "PASS":
                print(f"    └─ {error}")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! NPC Dialogue system is working correctly.")
        else:
            print(f"\n⚠️  {failed_tests} test(s) failed. Please review the issues above.")


if __name__ == "__main__":
    # Run the test suite
    test_suite = NPCDialogueTestSuite()
    test_suite.run_all_tests()