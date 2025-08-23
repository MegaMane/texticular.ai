"""
NPC Manager for Texticular
Handles NPC creation, dialogue management, and interaction states
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from texticular.character import NPC
from texticular.dialogue.dialogue_graph import DialogueGraph, DialogueNode, DialogueChoice
from texticular.game_object import GameObject


class NPCManager:
    """Manages all NPCs and their dialogue states in the game."""
    
    def __init__(self):
        self.npcs: Dict[str, NPC] = {}
        self.dialogue_graphs: Dict[str, DialogueGraph] = {}
        self.active_conversations: Dict[str, DialogueGraph] = {}  # player_id -> active dialogue
        
    def load_npcs_from_json(self, npc_data_file: str, dialogue_dir: str = "data/dialogues"):
        """Load NPCs and their dialogues from JSON configuration."""
        try:
            # Load NPC definitions
            with open(npc_data_file, 'r') as f:
                npc_config = json.load(f)
            
            # Create NPCs
            for npc_data in npc_config.get("npcs", []):
                npc = self._create_npc_from_data(npc_data)
                self.npcs[npc.key_value] = npc
                
                # Load dialogue if specified
                if "dialogue_file" in npc_data:
                    dialogue_path = Path(dialogue_dir) / npc_data["dialogue_file"]
                    if dialogue_path.exists():
                        dialogue = self._load_dialogue_from_json(str(dialogue_path))
                        self.dialogue_graphs[npc.key_value] = dialogue
                        
        except Exception as e:
            print(f"Warning: Could not load NPCs from {npc_data_file}: {e}")
    
    def _create_npc_from_data(self, npc_data: Dict[str, Any]) -> NPC:
        """Create an NPC instance from JSON data."""
        return NPC(
            key_value=npc_data["keyValue"],
            name=npc_data["name"],
            descriptions=npc_data["descriptions"],
            sex=npc_data.get("sex", "?"),
            hp=npc_data.get("hp", 100),
            location_key=npc_data["locationKey"],
            flags=npc_data.get("flags", [])
        )
    
    def _load_dialogue_from_json(self, dialogue_file: str) -> DialogueGraph:
        """Load a dialogue graph from JSON file."""
        with open(dialogue_file, 'r') as f:
            dialogue_data = json.load(f)
        
        # Convert JSON to DialogueGraph
        nodes = []
        for node_data in dialogue_data["nodes"]:
            choices = []
            for choice_data in node_data.get("choices", []):
                choice = DialogueChoice(
                    text=choice_data["choice"],
                    leads_to_id=choice_data["leadsToId"]
                )
                choices.append(choice)
            
            node = DialogueNode(
                node_id=node_data["nodeId"],
                text=node_data["text"],
                choices=choices
            )
            nodes.append(node)
        
        return DialogueGraph(
            root_node_id=dialogue_data["rootNodeID"],
            nodes=nodes,
            title=dialogue_data.get("title", "Conversation")
        )
    
    def get_npc(self, npc_key: str) -> Optional[NPC]:
        """Get an NPC by key."""
        return self.npcs.get(npc_key)
    
    def get_npcs_in_room(self, room_key: str) -> List[NPC]:
        """Get all NPCs currently in a specific room."""
        return [npc for npc in self.npcs.values() if npc.location_key == room_key]
    
    def start_conversation(self, player_id: str, npc_key: str) -> Optional[DialogueGraph]:
        """Start a conversation with an NPC."""
        if npc_key in self.dialogue_graphs:
            # Create a fresh dialogue instance for this conversation
            original = self.dialogue_graphs[npc_key]
            conversation = DialogueGraph(
                root_node_id=original._active_node_id,
                nodes=original.nodes(),
                title=original.title
            )
            self.active_conversations[player_id] = conversation
            return conversation
        return None
    
    def get_active_conversation(self, player_id: str) -> Optional[DialogueGraph]:
        """Get the player's active conversation, if any."""
        return self.active_conversations.get(player_id)
    
    def end_conversation(self, player_id: str):
        """End the player's active conversation."""
        if player_id in self.active_conversations:
            del self.active_conversations[player_id]
    
    def make_dialogue_choice(self, player_id: str, choice_index: int) -> bool:
        """Make a choice in the active dialogue. Returns True if choice was valid."""
        conversation = self.active_conversations.get(player_id)
        if conversation:
            try:
                conversation.make_choice(choice_index)
                
                # Check if conversation has ended
                current_node = conversation.current_node()
                if not current_node.choices or current_node.node_id == "EXIT":
                    self.end_conversation(player_id)
                    
                return True
            except (IndexError, KeyError):
                return False
        return False
    
    def register_npc(self, npc: NPC):
        """Register an existing NPC instance and load its dialogue if available."""
        self.npcs[npc.key_value] = npc
        
        # Load dialogue file if specified
        if hasattr(npc, 'dialogue_file') and npc.dialogue_file:
            from texticular.game_loader import get_data_path
            dialogue_path = Path(get_data_path()) / npc.dialogue_file
            if dialogue_path.exists():
                dialogue = self._load_dialogue_from_json(str(dialogue_path))
                self.dialogue_graphs[npc.key_value] = dialogue
            else:
                print(f"Warning: Dialogue file not found: {dialogue_path}")
    
    def create_janitor_npc(self) -> NPC:
        """Create the janitor NPC with money-lending dialogue."""
        janitor = NPC(
            key_value="janitor-east-hallway",
            name="Janitor",
            descriptions={
                "Main": "A gruff-looking janitor in blue coveralls. He's leaning on his mop and looks like he might be willing to help... for the right price."
            },
            sex="M",
            hp=100,
            location_key="eastHallway2f",
            flags=[]
        )
        
        # Create janitor dialogue
        janitor_dialogue = DialogueGraph(
            root_node_id="GREETING",
            nodes=[
                DialogueNode(
                    node_id="GREETING",
                    text="Janitor: *looks up from mopping* Well hey there, stranger. You look like you're in a real hurry. What's got you all worked up?",
                    choices=[
                        DialogueChoice("I need to borrow some money", "MONEY_REQUEST"),
                        DialogueChoice("I'm looking for a bathroom", "BATHROOM_HELP"),
                        DialogueChoice("Just looking around", "CASUAL"),
                        DialogueChoice("Never mind", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="MONEY_REQUEST",
                    text="Janitor: *chuckles* Money, huh? Well, I ain't made of cash, but I might be able to help ya out. How much you need?",
                    choices=[
                        DialogueChoice("Just enough for the vending machine", "VENDING_MONEY"),
                        DialogueChoice("A couple dollars", "SMALL_LOAN"),
                        DialogueChoice("Never mind", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="VENDING_MONEY",
                    text="Janitor: Ah, the vending machine! *grins* I got some change right here. Tell ya what - I'll give you two bucks, but you gotta do me a little favor first. See that supply closet over there? I lost my keys somewhere in this mess. Find 'em for me, and the money's yours.",
                    choices=[
                        DialogueChoice("Deal! Where should I look?", "ACCEPT_QUEST"),
                        DialogueChoice("That's too much work", "REFUSE_QUEST"),
                        DialogueChoice("Can't you just lend me 50 cents?", "SMALL_REQUEST")
                    ]
                ),
                DialogueNode(
                    node_id="SMALL_REQUEST",
                    text="Janitor: *laughs heartily* Fifty cents? Hell, you seem honest enough. Here ya go, kid. *tosses you two quarters* Don't spend it all in one place!",
                    choices=[
                        DialogueChoice("Thanks! You're a lifesaver!", "GRATEFUL_EXIT"),
                        DialogueChoice("This is exactly what I needed!", "GRATEFUL_EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="GRATEFUL_EXIT",
                    text="Janitor: *waves* No problem! Good luck with whatever's got you in such a rush!",
                    choices=[]
                ),
                DialogueNode(
                    node_id="ACCEPT_QUEST",
                    text="Janitor: Great! I think I dropped them somewhere in the west hallway, maybe near one of the rooms. They're on a big keyring with a little janitor figure on it. You can't miss 'em!",
                    choices=[
                        DialogueChoice("I'll find them", "QUEST_ACCEPTED"),
                        DialogueChoice("Actually, this sounds hard", "REFUSE_QUEST")
                    ]
                ),
                DialogueNode(
                    node_id="QUEST_ACCEPTED", 
                    text="Janitor: Excellent! Come back when you find those keys and I'll give you that two dollars. Maybe even throw in a little extra for the trouble.",
                    choices=[]
                ),
                DialogueNode(
                    node_id="REFUSE_QUEST",
                    text="Janitor: *shrugs* Well, can't say I didn't try to help. Maybe ask someone else, or check around for loose change. Good luck!",
                    choices=[]
                ),
                DialogueNode(
                    node_id="SMALL_LOAN",
                    text="Janitor: A couple bucks? *scratches head* Well, I suppose I could spare a little. But I don't just hand out money to strangers, you know. What's it for?",
                    choices=[
                        DialogueChoice("Emergency bathroom situation", "BATHROOM_EMERGENCY"),
                        DialogueChoice("Vending machine snacks", "VENDING_MONEY"),
                        DialogueChoice("Just forget it", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="BATHROOM_EMERGENCY",
                    text="Janitor: *eyes widen with understanding* Oh boy, one of THOSE emergencies! *quickly digs in pocket* Here's fifty cents - there's a vending machine down south that sells Fast Eddie's. Might help with your... situation. Or make it worse. Hard to tell with that stuff!",
                    choices=[
                        DialogueChoice("Thank you so much!", "GRATEFUL_EXIT"),
                        DialogueChoice("You're a real pal!", "GRATEFUL_EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="BATHROOM_HELP",
                    text="Janitor: Bathroom? *looks around conspiratorially* Well, there's the one in your room, but I heard there's a... situation with a dog. The lobby bathroom needs a token. Your best bet might be that vending machine - Fast Eddie's will clean you right out!",
                    choices=[
                        DialogueChoice("Can I borrow money for the vending machine?", "VENDING_MONEY"),
                        DialogueChoice("A dog in the bathroom?!", "DOG_INFO"),
                        DialogueChoice("Thanks for the info", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="DOG_INFO",
                    text="Janitor: *whispers* Big Great Dane. Mean as hell. Management knows about it but... *shrugs* ...they're working on it. I'd stay away if I were you. Maybe try the Fast Eddie's route instead.",
                    choices=[
                        DialogueChoice("Can you lend me money for that?", "SMALL_REQUEST"),
                        DialogueChoice("This place is crazy", "CASUAL"),
                        DialogueChoice("Thanks for the warning", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="CASUAL",
                    text="Janitor: *grins* Yeah, this place is something else alright. Been working here for fifteen years and I still see something new every day. Most of it ain't good, but it keeps things interesting!",
                    choices=[
                        DialogueChoice("Fifteen years? Wow", "LONG_TIMER"),
                        DialogueChoice("Any advice for surviving here?", "SURVIVAL_TIPS"),
                        DialogueChoice("I'll let you get back to work", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="LONG_TIMER",
                    text="Janitor: *chuckles* Yep, seen it all. Angry dogs, mysterious stains, guests who think they're in the Ritz... You name it. But hey, job's a job, and the stories are worth something!",
                    choices=[
                        DialogueChoice("Got any good stories?", "STORIES"),
                        DialogueChoice("Sounds like you've earned your pay", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="SURVIVAL_TIPS",
                    text="Janitor: *leans in* Here's a tip: always carry exact change, avoid the elevator after 10 PM, and if you hear weird noises from Room 203... well, just turn up the TV. Trust me on that last one.",
                    choices=[
                        DialogueChoice("Room 203?", "ROOM_203"),
                        DialogueChoice("Thanks for the advice!", "EXIT")
                    ]
                ),
                DialogueNode(
                    node_id="ROOM_203",
                    text="Janitor: *winks* Let's just say some folks are... enthusiastic... about their hotel stays. Walls are thin around here. Real thin.",
                    choices=[
                        DialogueChoice("I'll keep that in mind", "EXIT"),
                        DialogueChoice("This place gets weirder and weirder", "CASUAL")
                    ]
                ),
                DialogueNode(
                    node_id="EXIT",
                    text="Janitor: *waves* Take care now! And remember - if you need anything, just holler. I'll be around here somewhere.",
                    choices=[]
                )
            ],
            title="Conversation with Janitor"
        )
        
        self.npcs[janitor.key_value] = janitor
        self.dialogue_graphs[janitor.key_value] = janitor_dialogue
        
        return janitor


# Global NPC manager instance
_npc_manager = None

def get_npc_manager() -> NPCManager:
    """Get the global NPC manager instance."""
    global _npc_manager
    if _npc_manager is None:
        _npc_manager = NPCManager()
    return _npc_manager