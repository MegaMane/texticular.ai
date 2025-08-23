#!/usr/bin/env python3
"""
Direct Test of NPC Dialogue System Components
Tests the core dialogue functionality without full game initialization
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.texticular.character import NPC
from src.texticular.npc_manager import NPCManager
from src.texticular.dialogue.dialogue_graph import DialogueGraph, DialogueNode, DialogueChoice


class DirectNPCTest:
    """Direct test of NPC dialogue components without full game setup."""
    
    def __init__(self):
        self.test_results = []
        self.failed_tests = []
        
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
    
    def test_npc_creation(self):
        """Test creating an NPC instance."""
        npc = NPC(
            key_value="test_janitor",
            name="Test Janitor", 
            descriptions={"Main": "A test janitor"},
            location_key="test_room",
            synonyms=["janitor", "cleaner"],
            adjectives=["gruff"],
            dialogue_file="test_dialogue.json"
        )
        
        if not npc:
            return False
            
        if npc.name != "Test Janitor":
            print(f"❌ Expected name 'Test Janitor', got '{npc.name}'")
            return False
            
        if npc.dialogue_file != "test_dialogue.json":
            print(f"❌ Expected dialogue_file 'test_dialogue.json', got '{npc.dialogue_file}'")
            return False
            
        print("✅ NPC created successfully with all properties")
        return True
    
    def test_dialogue_graph_creation(self):
        """Test creating a dialogue graph from scratch."""
        # Create dialogue choices
        choice1 = DialogueChoice("Hello there!", "GREETING_RESPONSE")
        choice2 = DialogueChoice("I need help", "HELP_REQUEST")
        
        # Create dialogue nodes
        start_node = DialogueNode("START", "Welcome! How can I help you?", [choice1, choice2])
        greeting_node = DialogueNode("GREETING_RESPONSE", "Hello to you too!", [])
        help_node = DialogueNode("HELP_REQUEST", "What kind of help do you need?", [])
        
        # Create dialogue graph
        dialogue = DialogueGraph("START", [start_node, greeting_node, help_node], "Test Dialogue")
        
        if not dialogue:
            print("❌ Failed to create dialogue graph")
            return False
            
        current_node = dialogue.current_node()
        if current_node.node_id != "START":
            print(f"❌ Expected current node 'START', got '{current_node.node_id}'")
            return False
            
        if len(current_node.choices) != 2:
            print(f"❌ Expected 2 choices, got {len(current_node.choices)}")
            return False
            
        print("✅ Dialogue graph created successfully with proper structure")
        return True
    
    def test_dialogue_navigation(self):
        """Test navigating through dialogue choices."""
        # Create simple dialogue
        choice1 = DialogueChoice("Option 1", "NODE1")
        start_node = DialogueNode("START", "Choose an option", [choice1])
        node1 = DialogueNode("NODE1", "You chose option 1!", [])
        
        dialogue = DialogueGraph("START", [start_node, node1])
        
        # Make a choice
        dialogue.make_choice(0)  # Choose first option
        
        current_node = dialogue.current_node()
        if current_node.node_id != "NODE1":
            print(f"❌ Expected current node 'NODE1', got '{current_node.node_id}'")
            return False
            
        if current_node.text != "You chose option 1!":
            print(f"❌ Unexpected node text: '{current_node.text}'")
            return False
            
        print("✅ Dialogue navigation working correctly")
        return True
    
    def test_janitor_dialogue_loading(self):
        """Test loading the actual janitor dialogue file."""
        from src.texticular.game_loader import get_data_path
        
        dialogue_path = Path(get_data_path()) / "janitor_dialogue.json"
        if not dialogue_path.exists():
            print(f"❌ Dialogue file not found: {dialogue_path}")
            return False
            
        # Create NPC manager and test loading
        npc_manager = NPCManager()
        
        try:
            dialogue = npc_manager._load_dialogue_from_json(str(dialogue_path))
            if not dialogue:
                print("❌ Failed to load dialogue from JSON")
                return False
                
            current_node = dialogue.current_node()
            if current_node.node_id != "START":
                print(f"❌ Expected root node 'START', got '{current_node.node_id}'")
                return False
                
            # Check for key elements in starting dialogue
            if "Fast Eddie" not in current_node.text:
                print("❌ Starting dialogue doesn't mention Fast Eddie")
                return False
                
            if len(current_node.choices) < 3:
                print(f"❌ Expected at least 3 starting choices, got {len(current_node.choices)}")
                return False
                
            print("✅ Janitor dialogue loaded successfully from JSON")
            return True
            
        except Exception as e:
            print(f"❌ Error loading dialogue: {e}")
            return False
    
    def test_npc_manager_registration(self):
        """Test NPC manager registration functionality."""
        npc_manager = NPCManager()
        
        # Create test NPC with dialogue file
        npc = NPC(
            key_value="test_janitor",
            name="Test Janitor",
            descriptions={"Main": "A test janitor"},
            location_key="test_room",
            dialogue_file="janitor_dialogue.json"
        )
        
        # Register the NPC
        npc_manager.register_npc(npc)
        
        # Check if NPC was registered
        retrieved_npc = npc_manager.get_npc("test_janitor")
        if not retrieved_npc:
            print("❌ NPC was not registered correctly")
            return False
            
        if retrieved_npc.name != "Test Janitor":
            print(f"❌ Retrieved NPC has wrong name: '{retrieved_npc.name}'")
            return False
            
        # Check if dialogue was loaded
        if "test_janitor" not in npc_manager.dialogue_graphs:
            print("❌ Dialogue was not loaded for registered NPC")
            return False
            
        print("✅ NPC registration and dialogue loading successful")
        return True
    
    def test_conversation_management(self):
        """Test starting and managing conversations."""
        npc_manager = NPCManager()
        
        # Create and register NPC
        npc = NPC(
            key_value="conversation_janitor",
            name="Conversation Janitor", 
            descriptions={"Main": "A janitor for conversation testing"},
            location_key="test_room",
            dialogue_file="janitor_dialogue.json"
        )
        npc_manager.register_npc(npc)
        
        # Start conversation
        player_id = "test_player"
        conversation = npc_manager.start_conversation(player_id, "conversation_janitor")
        
        if not conversation:
            print("❌ Failed to start conversation")
            return False
            
        # Check if conversation is tracked
        active_conversation = npc_manager.get_active_conversation(player_id)
        if not active_conversation:
            print("❌ Active conversation not tracked")
            return False
            
        # Make a dialogue choice
        choice_made = npc_manager.make_dialogue_choice(player_id, 0)
        if not choice_made:
            print("❌ Failed to make dialogue choice")
            return False
            
        # Check if conversation state changed
        new_node = active_conversation.current_node()
        if new_node.node_id == "START":
            print("❌ Dialogue state didn't change after choice")
            return False
            
        print("✅ Conversation management working correctly")
        return True
    
    def test_dialogue_ui_integration(self):
        """Test that dialogue data can be formatted for UI display."""
        from src.texticular.ui.fixed_layout_ui import FixedLayoutUI
        
        # Create simple dialogue for testing
        choice1 = DialogueChoice("Test choice 1", "NODE1")
        choice2 = DialogueChoice("Test choice 2", "NODE2")
        start_node = DialogueNode("START", "This is a test dialogue for UI display.", [choice1, choice2])
        
        ui = FixedLayoutUI()
        
        try:
            # This should not crash
            ui.display_dialogue_interface(
                npc_name="Test NPC",
                dialogue_text=start_node.text,
                choices=[choice.text for choice in start_node.choices]
            )
            print("✅ UI integration successful (no crashes)")
            return True
            
        except Exception as e:
            print(f"❌ UI integration failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all direct NPC tests."""
        print("🚀 Starting Direct NPC Dialogue System Tests")
        print("="*60)
        
        self.run_test("NPC Creation", self.test_npc_creation)
        self.run_test("Dialogue Graph Creation", self.test_dialogue_graph_creation)
        self.run_test("Dialogue Navigation", self.test_dialogue_navigation)
        self.run_test("Janitor Dialogue Loading", self.test_janitor_dialogue_loading)
        self.run_test("NPC Manager Registration", self.test_npc_manager_registration)
        self.run_test("Conversation Management", self.test_conversation_management)
        self.run_test("Dialogue UI Integration", self.test_dialogue_ui_integration)
        
        self.print_test_summary()
    
    def print_test_summary(self):
        """Print test summary."""
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
            print("\n🎉 ALL TESTS PASSED! NPC Dialogue system components are working correctly.")
        else:
            print(f"\n⚠️  {failed_tests} test(s) failed. Please review the issues above.")


if __name__ == "__main__":
    test_suite = DirectNPCTest()
    test_suite.run_all_tests()