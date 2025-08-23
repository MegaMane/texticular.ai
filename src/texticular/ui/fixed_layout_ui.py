"""
Fixed Layout Rich Terminal UI for Texticular
Provides a screen-based interface that clears and redraws each turn
"""

import os
from typing import List, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, BarColumn, TextColumn
from rich import box


class FixedLayoutUI:
    """
    Fixed layout terminal UI that clears and redraws each turn.
    Provides distinct areas for game content, HUD, and command input.
    """
    
    def __init__(self):
        self.console = Console()
        self.turn_count = 0
        self.score = 0
        self.poop_level = 45  # Starting urgency level
        self.last_command = ""
        self.last_response = ""
        self.inventory_preview = []
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def create_layout(self) -> Layout:
        """Create the main game layout with fixed areas."""
        layout = Layout()
        
        # Split into header, body, footer
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=6)
        )
        
        # Split body into game area and HUD
        layout["body"].split_row(
            Layout(name="game", ratio=3),
            Layout(name="hud", size=28)
        )
        
        return layout
    
    def create_header(self) -> Panel:
        """Create the game header with title."""
        title = Text("TEXTICULAR: Chapter 1 - You Gotta Go!", style="bold cyan")
        return Panel(Align.center(title), box=box.DOUBLE, style="cyan")
    
    def create_game_area(self, room_name: str, description: str, exits: List[str]) -> Panel:
        """Create the main game content area."""
        content = []
        
        # Location header with icon
        location_text = Text(f"📍 {room_name}", style="bold yellow")
        content.append(location_text)
        content.append("")
        
        # Room description - format nicely
        desc_lines = description.split(". ")
        for line in desc_lines:
            if line.strip():
                # Wrap long lines
                words = line.strip().split()
                current_line = []
                for word in words:
                    if len(" ".join(current_line + [word])) <= 50:
                        current_line.append(word)
                    else:
                        if current_line:
                            content.append(Text(" ".join(current_line) + ("." if line.endswith(".") else ""), style="white"))
                            current_line = [word]
                        else:
                            current_line.append(word)
                
                if current_line:
                    content.append(Text(" ".join(current_line) + ("." if line.endswith(".") else ""), style="white"))
        
        content.append("")
        
        # Exits section
        if exits:
            content.append(Text("🚪 Exits:", style="bold green"))
            for exit_info in exits:
                content.append(Text(f"  {exit_info}", style="green"))
        
        return Panel("\n".join([str(c) for c in content]), 
                    title="Game World", 
                    box=box.ROUNDED, 
                    style="white")
    
    def create_hud(self, turn: int, score: int, location: str, poop_level: int, inventory: List[str]) -> Panel:
        """Create the HUD/status area."""
        hud_content = []
        
        # Game stats
        hud_content.append(Text("📊 GAME STATUS", style="bold magenta"))
        hud_content.append("")
        hud_content.append(Text(f"Turn: {turn}", style="cyan"))
        hud_content.append(Text(f"Score: {score}", style="cyan"))
        hud_content.append(Text(f"Location: {location}", style="cyan"))
        hud_content.append("")
        
        # Poop meter (the critical stat!)
        hud_content.append(Text("💩 URGENCY METER", style="bold red"))
        bar_length = 18
        filled = int((poop_level / 100) * bar_length)
        empty = bar_length - filled
        poop_bar = "█" * filled + "░" * empty
        
        # Color based on urgency
        if poop_level > 90:
            poop_color = "red"
            status = "🚨 CRITICAL!"
        elif poop_level > 75:
            poop_color = "yellow" 
            status = "⚠️ Urgent!"
        elif poop_level > 50:
            poop_color = "yellow"
            status = "😰 Worried"
        else:
            poop_color = "green"
            status = "😌 Ok"
            
        hud_content.append(Text(f"[{poop_bar}]", style=poop_color))
        hud_content.append(Text(f"{poop_level}% - {status}", style=poop_color))
        hud_content.append("")
        
        # Inventory preview
        hud_content.append(Text("🎒 INVENTORY", style="bold blue"))
        if inventory:
            for item in inventory[:4]:  # Show max 4 items
                hud_content.append(Text(f"• {item}", style="blue"))
            if len(inventory) > 4:
                hud_content.append(Text(f"• ... and {len(inventory)-4} more", style="dim blue"))
        else:
            hud_content.append(Text("• Empty", style="dim blue"))
        hud_content.append("")
        
        # Quick help
        hud_content.append(Text("💡 QUICK HELP", style="bold green"))
        hud_content.append(Text("look - examine area", style="dim"))
        hud_content.append(Text("go <dir> - move", style="dim"))
        hud_content.append(Text("i - inventory", style="dim"))
        hud_content.append(Text("sit/use/take", style="dim"))
        
        return Panel("\n".join([str(c) for c in hud_content]), 
                    title="Status", 
                    box=box.ROUNDED, 
                    style="magenta")
    
    def create_footer(self, last_command: str, response: str) -> Panel:
        """Create the command/response footer."""
        footer_content = []
        
        # Show last command if exists
        if last_command:
            footer_content.append(Text(f">> {last_command}", style="bold white"))
        
        # Show response, wrapped to fit
        if response:
            # Limit response length and wrap
            max_length = 150
            if len(response) > max_length:
                response = response[:max_length] + "..."
            
            # Word wrap response
            words = response.split()
            lines = []
            current_line = []
            
            for word in words:
                if len(" ".join(current_line + [word])) <= 75:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(" ".join(current_line))
            
            for line in lines[:2]:  # Show max 2 lines
                footer_content.append(Text(line, style="yellow"))
        
        # Always show command prompt
        footer_content.append("")
        footer_content.append(Text("Enter command:", style="bold green"))
        
        return Panel("\n".join([str(c) for c in footer_content]), 
                    title="Command", 
                    box=box.ROUNDED, 
                    style="green")
    
    def render_screen(self, game_state: Dict[str, Any]):
        """
        Main method to render the complete game screen.
        
        Args:
            game_state: Dictionary containing:
                - room_name: Current room name
                - description: Room description
                - exits: List of exit descriptions
                - turn: Current turn number
                - score: Current score
                - poop_level: Urgency level (0-100)
                - inventory: List of inventory item names
                - last_command: Last command entered
                - response: Response to last command
        """
        # Clear screen for clean redraw
        self.clear_screen()
        
        # Extract game state
        room_name = game_state.get("room_name", "Unknown")
        description = game_state.get("description", "")
        exits = game_state.get("exits", [])
        turn = game_state.get("turn", 1)
        score = game_state.get("score", 0)
        poop_level = game_state.get("poop_level", 50)
        inventory = game_state.get("inventory", [])
        last_command = game_state.get("last_command", "")
        response = game_state.get("response", "")
        
        # Create and populate layout
        layout = self.create_layout()
        layout["header"].update(self.create_header())
        layout["game"].update(self.create_game_area(room_name, description, exits))
        layout["hud"].update(self.create_hud(turn, score, room_name, poop_level, inventory))
        layout["footer"].update(self.create_footer(last_command, response))
        
        # Render to console
        self.console.print(layout)
    
    def get_input(self) -> str:
        """Get input from user. This appears below the rendered screen."""
        try:
            return input("🎮 ")
        except (EOFError, KeyboardInterrupt):
            return "quit"
    
    def display_intro(self, intro_content: List[str]):
        """Display the game introduction with the new layout."""
        self.clear_screen()
        
        # Create simple layout for intro
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="content", ratio=1),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(self.create_header())
        
        # Intro content
        intro_text = "\n\n".join(intro_content)
        intro_panel = Panel(intro_text, title="Welcome to Texticular!", box=box.ROUNDED, style="cyan")
        layout["content"].update(intro_panel)
        
        # Footer
        footer_panel = Panel(Align.center(Text("Press ENTER to begin...", style="bold green")), 
                           box=box.ROUNDED, style="green")
        layout["footer"].update(footer_panel)
        
        self.console.print(layout)
        
        # Wait for user
        try:
            input()
        except (EOFError, KeyboardInterrupt):
            pass
    
    def display_vending_machine_menu(self, greeting: List[str], menu: str):
        """Display vending machine interface with the fixed layout."""
        self.clear_screen()
        
        # Create vending machine layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=4)
        )
        
        # Header with vending machine title
        title = Text("🤖 FAST EDDIE'S VENDING MACHINE", style="bold cyan")
        subtitle = Text("When in doubt, flush it out!", style="dim cyan")
        header_panel = Panel(f"{title}\n{subtitle}", box=box.DOUBLE, style="cyan")
        layout["header"].update(header_panel)
        
        # Body with greeting and menu
        content = []
        
        # Add greeting
        for line in greeting:
            content.append(Text(line, style="magenta"))
        content.append("")
        
        # Add menu
        content.append(Text("🛒 MENU:", style="bold green"))
        for line in menu.split('\n'):
            if line.strip():
                content.append(Text(line, style="green"))
        
        body_panel = Panel("\n".join([str(c) for c in content]), 
                          title="Vending Machine Interface", 
                          box=box.ROUNDED, 
                          style="white")
        layout["body"].update(body_panel)
        
        # Footer with input prompt
        footer_content = Text("Enter your selection (1, 2, 'money', 'menu', 'leave'):", style="bold yellow")
        footer_panel = Panel(footer_content, title="Input", box=box.ROUNDED, style="yellow")
        layout["footer"].update(footer_panel)
        
        self.console.print(layout)
    
    def display_vending_response(self, response: List[str]):
        """Display vending machine response in fixed layout."""
        # For simplicity, just print the response and wait
        # In a full implementation, this could show a temporary overlay
        self.clear_screen()
        
        response_text = "\n".join([str(r) for r in response])
        response_panel = Panel(response_text, 
                              title="🤖 Vending Machine Response", 
                              box=box.ROUNDED, 
                              style="magenta")
        
        self.console.print(response_panel)
        
        # Brief pause to show response
        try:
            input("\nPress ENTER to continue...")
        except (EOFError, KeyboardInterrupt):
            pass
    
    def exit_vending_machine(self):
        """Exit vending machine mode - no special action needed for fixed layout."""
        pass
    
    def display_dialogue_interface(self, npc_name: str, dialogue_text: str, choices: List[str]):
        """Display NPC dialogue interface with the fixed layout."""
        self.clear_screen()
        
        # Create dialogue layout
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=6)
        )
        
        # Header with NPC info
        title = Text(f"💬 CONVERSATION WITH {npc_name.upper()}", style="bold cyan")
        header_panel = Panel(title, box=box.DOUBLE, style="cyan")
        layout["header"].update(header_panel)
        
        # Body with dialogue text
        dialogue_content = []
        
        # Format dialogue text with proper wrapping
        words = dialogue_text.split()
        lines = []
        current_line = []
        max_width = 60
        
        for word in words:
            if len(" ".join(current_line + [word])) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        
        if current_line:
            lines.append(" ".join(current_line))
        
        for line in lines:
            dialogue_content.append(Text(line, style="white"))
        
        body_panel = Panel("\n".join([str(c) for c in dialogue_content]), 
                          title=f"{npc_name} says...", 
                          box=box.ROUNDED, 
                          style="white")
        layout["body"].update(body_panel)
        
        # Footer with choices
        footer_content = []
        if choices:
            footer_content.append(Text("Choose your response:", style="bold yellow"))
            footer_content.append("")
            for i, choice in enumerate(choices):
                choice_text = f"{i + 1}. {choice}"
                if len(choice_text) > 70:
                    choice_text = choice_text[:67] + "..."
                footer_content.append(Text(choice_text, style="green"))
        else:
            footer_content.append(Text("Press ENTER to continue...", style="dim yellow"))
        
        footer_panel = Panel("\n".join([str(c) for c in footer_content]), 
                           title="Response Options", 
                           box=box.ROUNDED, 
                           style="yellow")
        layout["footer"].update(footer_panel)
        
        self.console.print(layout)
    
    def display_dialogue_response(self, response_text: str):
        """Display a dialogue response or result."""
        self.clear_screen()
        
        response_panel = Panel(response_text, 
                              title="💬 Conversation Result", 
                              box=box.ROUNDED, 
                              style="green")
        
        self.console.print(response_panel)
        
        # Brief pause
        try:
            input("\nPress ENTER to continue...")
        except (EOFError, KeyboardInterrupt):
            pass