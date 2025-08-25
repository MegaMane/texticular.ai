"""
ASCII-based UI system for Texticular
Provides clean, fixed-width terminal interface with color highlighting
"""

import os
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# ANSI color codes for terminal
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


@dataclass
class GameState:
    """Game state data for UI rendering"""
    room_name: str
    room_description: str
    visible_items: List[str]
    npcs: List[str]
    exits: List[Dict[str, str]]  # [{"direction": "west", "description": "...", "name": "Bathroom Door"}]
    inventory: List[str]
    turn: int
    score: int
    poop_level: int  # 0-100
    location: str
    last_response: str = ""
    dialogue_active: bool = False
    dialogue_content: Optional[Dict[str, Any]] = None


class ASCIIGameUI:
    """ASCII-based game interface"""
    
    def __init__(self, width: int = 120, height: int = 35):
        self.width = width
        self.height = height
        self.dialogue_ui = ASCIIDialogueUI(width, height)
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def render_poop_meter(self, level: int) -> str:
        """Create ASCII poop meter"""
        # 20 character meter
        filled = int((level / 100) * 20)
        empty = 20 - filled
        meter = '[' + ('*' * filled) + ('-' * empty) + ']'
        
        # Color coding
        if level < 30:
            return f"{Colors.GREEN}{meter}{Colors.RESET}"
        elif level < 70:
            return f"{Colors.YELLOW}{meter}{Colors.RESET}"
        else:
            return f"{Colors.RED}{meter}{Colors.RESET}"
            
    def format_exits(self, exits: List[Dict[str, str]]) -> List[str]:
        """Format exits with proper padding"""
        formatted = []
        for exit_info in exits:
            direction = exit_info['direction'].title()
            description = exit_info['description']
            name = exit_info['name']
            
            # Create the base text
            base_text = f"    To the {direction} {description}"
            
            # Calculate padding needed (minimum 3 dots)
            dots_needed = max(3, 80 - len(base_text) - len(name))
            padding = '.' * dots_needed
            
            formatted_line = f"{base_text}{padding}{{{name}}}"
            formatted.append(formatted_line)
            
        return formatted
        
    def wrap_text(self, text: str, width: int) -> List[str]:
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= width:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                
        if current_line:
            lines.append(current_line)
            
        return lines
        
    def render_game_screen(self, game_state: GameState):
        """Render the main game screen"""
        self.clear_screen()
        
        # If dialogue is active, render dialogue UI instead
        if game_state.dialogue_active and game_state.dialogue_content:
            self.dialogue_ui.render_dialogue_screen(game_state)
            return
            
        lines = []
        
        # Header line with inventory and stats
        inventory_text = f"Inventory: [{', '.join(game_state.inventory) if game_state.inventory else 'empty'}]"
        stats_text = f"Turn: {game_state.turn}"
        padding = self.width - len(inventory_text) - len(stats_text)
        header_line = inventory_text + (' ' * padding) + stats_text
        lines.append(header_line)
        
        # Second stats line
        score_text = f"Score: {game_state.score}"
        poop_text = f"HPooh: {self.render_poop_meter(game_state.poop_level)}"
        location_text = f"Location: {game_state.location}"
        
        # Position these on the right side
        stats_padding = self.width - len(score_text) - 15  # Account for poop meter
        lines.append((' ' * stats_padding) + score_text)
        lines.append((' ' * (stats_padding - 10)) + poop_text)
        lines.append((' ' * (stats_padding - 5)) + location_text)
        
        lines.append("")  # Empty line
        
        # Room name box
        room_name = game_state.room_name
        box_width = len(room_name) + 4
        room_box = [
            '|' + '-' * (box_width - 2) + '|',
            f"|  {Colors.BOLD}{Colors.YELLOW}{room_name}{Colors.RESET}  |",
            '|' + '-' * (box_width - 2) + '|'
        ]
        
        for box_line in room_box:
            lines.append(box_line)
            
        lines.append("")  # Empty line
        
        # Room description
        desc_lines = self.wrap_text(game_state.room_description, 100)
        for desc_line in desc_lines:
            lines.append(desc_line)
            
        lines.append("")  # Empty line
        
        # Visible items section
        if game_state.visible_items:
            for item in game_state.visible_items:
                item_lines = self.wrap_text(item, 100)
                for item_line in item_lines:
                    lines.append(item_line)
            lines.append("")  # Empty line
            
        # NPCs section
        if game_state.npcs:
            for npc in game_state.npcs:
                npc_lines = self.wrap_text(npc, 100)
                for npc_line in npc_lines:
                    lines.append(npc_line)
            lines.append("")  # Empty line
            
        # Exits section
        lines.append(f"{Colors.BOLD}Exits:{Colors.RESET}")
        exit_lines = self.format_exits(game_state.exits)
        for exit_line in exit_lines:
            lines.append(exit_line)
            
        lines.append("")  # Empty line
        lines.append("")  # Empty line
        
        # Last response (if any)
        if game_state.last_response:
            response_lines = self.wrap_text(game_state.last_response, 100)
            for response_line in response_lines:
                lines.append(f"{Colors.CYAN}{response_line}{Colors.RESET}")
            lines.append("")  # Empty line
            
        # Print all lines
        for line in lines:
            print(line)
            
        # Command input section
        command_border = '*' + '-' * (self.width - 30) + 'Enter Player Command' + '-' * 28 + '*'
        print(command_border)
        print(f"| >> {' ' * (self.width - 6)}|")
        print('*' + '-' * (self.width - 2) + '*')
        print(f"Basic Commands: {Colors.DIM}Look <room>, Go <direction>, Inv, Take <item>, Open <container or door>, Help, Save, Exit{Colors.RESET}")
        
    def get_input(self) -> str:
        """Get user input"""
        # Position cursor in the command box
        # Move cursor up to the input line
        sys.stdout.write('\033[3A')  # Move up 3 lines
        sys.stdout.write('\033[5C')  # Move right 5 characters (after "| >> ")
        sys.stdout.flush()
        
        try:
            user_input = input().strip()
            return user_input
        except (EOFError, KeyboardInterrupt):
            return "quit"


class ASCIIDialogueUI:
    """ASCII-based dialogue interface"""
    
    def __init__(self, width: int = 120, height: int = 35):
        self.width = width
        self.height = height
        
    def render_dialogue_screen(self, game_state: GameState):
        """Render dialogue interface"""
        dialogue = game_state.dialogue_content
        if not dialogue:
            return
            
        lines = []
        
        # Header
        lines.append(f"{Colors.BOLD}{Colors.MAGENTA}═══════════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        lines.append(f"{Colors.BOLD}{Colors.MAGENTA}                                  CONVERSATION MODE                                {Colors.RESET}")
        lines.append(f"{Colors.BOLD}{Colors.MAGENTA}═══════════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        lines.append("")
        
        # NPC name and current dialogue text
        npc_name = dialogue.get('npc_name', 'Unknown')
        current_text = dialogue.get('current_text', '')
        
        lines.append(f"{Colors.BOLD}{Colors.YELLOW}{npc_name}:{Colors.RESET}")
        lines.append("")
        
        # Wrap dialogue text
        dialogue_lines = self.wrap_text(current_text, 100)
        for dialogue_line in dialogue_lines:
            lines.append(f"  {dialogue_line}")
            
        lines.append("")
        lines.append("")
        
        # Player response choices
        choices = dialogue.get('choices', [])
        if choices:
            lines.append(f"{Colors.BOLD}Your responses:{Colors.RESET}")
            lines.append("")
            for i, choice in enumerate(choices, 1):
                choice_text = choice.get('text', '')
                lines.append(f"  {Colors.GREEN}{i}.{Colors.RESET} {choice_text}")
                
            lines.append("")
            lines.append(f"{Colors.DIM}Enter the number of your choice, or 'quit' to end conversation.{Colors.RESET}")
        else:
            lines.append(f"{Colors.DIM}[Press ENTER to continue, or 'quit' to end conversation]{Colors.RESET}")
            
        # Print all lines
        for line in lines:
            print(line)
            
        # Fill remaining space
        remaining_lines = self.height - len(lines) - 3
        for _ in range(remaining_lines):
            print("")
            
        # Input prompt
        print(f"{Colors.BOLD}>> {Colors.RESET}", end="")
        
    def wrap_text(self, text: str, width: int) -> List[str]:
        """Simple text wrapping for dialogue"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= width:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                
        if current_line:
            lines.append(current_line)
            
        return lines