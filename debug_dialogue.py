#!/usr/bin/env python3
"""
Debug genie dialogue loading
"""

import sys
import os
import json

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from texticular.dialogue.dialogue_graph import DialogueGraph, DialogueNode, DialogueChoice
from texticular.game_loader import get_data_path

def debug_genie_dialogue():
    print("🧪 DEBUGGING GENIE DIALOGUE SYSTEM")
    print("=" * 50)
    
    try:
        # Load dialogue from JSON file
        data_path = get_data_path()
        dialogue_file = os.path.join(data_path, "genie_dialogue.json")
        print(f"Loading from: {dialogue_file}")
        
        with open(dialogue_file, 'r') as f:
            dialogue_data = json.load(f)
        
        print(f"✅ JSON loaded successfully")
        print(f"Root node ID: {dialogue_data['rootNodeID']}")
        print(f"Total nodes in JSON: {len(dialogue_data['nodes'])}")
        
        # Try to parse the first node
        first_node = dialogue_data['nodes'][0]
        print(f"First node structure: {list(first_node.keys())}")
        print(f"First node ID: {first_node.get('nodeId', 'NOT FOUND')}")
        
        # Try to convert JSON to DialogueGraph
        print("\n🔄 Converting to DialogueGraph...")
        
        nodes = []
        for i, node_data in enumerate(dialogue_data['nodes']):
            print(f"Processing node {i}: {node_data.get('nodeId', 'NO_ID')}")
            
            choices = []
            for j, choice_data in enumerate(node_data.get('choices', [])):
                print(f"  Choice {j}: {choice_data.get('choice', 'NO_TEXT')[:30]}")
                choice = DialogueChoice(
                    text=choice_data['choice'],
                    leads_to_id=choice_data['leadsToId']
                )
                choices.append(choice)
            
            node = DialogueNode(
                node_id=node_data['nodeId'],
                text=node_data['text'],
                choices=choices
            )
            nodes.append(node)
        
        dialogue_graph = DialogueGraph(dialogue_data['rootNodeID'], nodes)
        print(f"✅ DialogueGraph created successfully!")
        print(f"Current node: {dialogue_graph.current_node().node_id}")
        print(f"Current text preview: {dialogue_graph.current_node().text[:60]}...")
        print(f"Number of choices: {len(dialogue_graph.current_node().choices)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_genie_dialogue()