"""
Terminal UI Manager using Rich library
Provides fixed input area and scrolling content display
"""

import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.padding import Padding
from typing import List, Optional


class TerminalUI:
    """
    Rich-based terminal UI with fixed input area and content display.
    Provides clean, immersive interface for text adventure games.
    """
    
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        
        # Set up layout structure
        self.layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="input", size=3),
        )
        
        # Current content and menu state
        self.current_content = []
        self.current_menu = None
        self.game_title = "TEXTICULAR - Chapter 1: You Gotta Go!"
        
        # Initialize display
        self.setup_header()
        self.clear_content()
        self.setup_input_area()
        
    def setup_header(self):
        """Set up the game header/title area."""
        title_text = Text(self.game_title, style="bold cyan")
        header_panel = Panel(
            Align.center(title_text),
            style="blue",
            height=3
        )
        self.layout["header"].update(header_panel)
        
    def setup_input_area(self):
        """Set up the fixed input area at bottom."""
        input_text = Text(">> ", style="bold green")
        input_panel = Panel(
            input_text,
            title="Command",
            style="green",
            height=3
        )
        self.layout["input"].update(input_panel)
        
    def clear_content(self):
        """Clear the main content area."""
        self.current_content = []
        self.current_menu = None
        self.update_display()
        
    def add_content(self, content: str, style: str = "white"):
        """Add content to the main display area."""
        if isinstance(content, list):
            for line in content:
                self.current_content.append(Text(line, style=style))
        else:
            # Split long content into lines
            lines = content.split('\n')
            for line in lines:
                self.current_content.append(Text(line, style=style))
                
    def set_menu(self, menu_content: str, title: str = "Menu"):
        """Set persistent menu content that stays visible."""
        self.current_menu = Panel(
            menu_content,
            title=title,
            style="yellow",
            expand=False
        )
        
    def clear_menu(self):
        """Clear the current menu."""
        self.current_menu = None
        
    def update_display(self):
        """Update the main content display."""
        # Create main content area
        content_text = Text()
        
        # Add regular content
        if self.current_content:
            # Keep only last 20 lines to prevent overflow
            recent_content = self.current_content[-20:]
            for text_obj in recent_content:
                content_text.append(text_obj)
                content_text.append("\n")
            
        # Add persistent menu if present
        if self.current_menu:
            content_text.append("\n")
            # Convert menu panel to text
            content_text.append(self.current_menu.renderable, style="yellow")
            
        # Create the main panel
        if not content_text.plain:
            content_text = Text("Welcome to Texticular!", style="bold cyan")
            
        main_panel = Panel(
            content_text,
            title="Game",
            style="white",
            expand=True
        )
        
        self.layout["main"].update(main_panel)
        
    def display(self):
        """Display the current UI state."""
        self.update_display()
        self.console.clear()
        self.console.print(self.layout)
        
    def get_input(self, prompt: str = ">> ") -> str:
        """Get input from user with Rich styling."""
        self.console.print(f"[bold green]{prompt}[/bold green]", end="")
        return input()
        
    def display_intro(self, intro_content: List[str]):
        """Display game introduction with proper formatting."""
        self.clear_content()
        
        # Add ASCII title
        self.add_content(intro_content[0], "bold cyan")  # ASCII art
        self.add_content("", "white")
        
        # Add story content
        for line in intro_content[1:]:
            if line.strip():
                self.add_content(line, "white")
            else:
                self.add_content("", "white")
                
        self.display()
        
    def display_room(self, room_content: List[str]):
        """Display room description and exits."""
        self.clear_content()
        
        # Add room content
        for line in room_content:
            if "---Exits---" in line:
                self.add_content(line, "bold yellow")
            elif line.strip().startswith("To the"):
                self.add_content(line, "cyan")
            else:
                self.add_content(line, "white")
                
        self.display()
        
    def display_vending_machine_menu(self, greeting: List[str], menu: str):
        """Display vending machine interface with persistent menu."""
        self.clear_content()
        
        # Add greeting
        for line in greeting:
            self.add_content(line, "bold magenta")
            
        # Set persistent menu
        self.set_menu(menu, "Vending Machine")
        self.display()
        
    def display_vending_response(self, response: List[str]):
        """Display vending machine response while keeping menu visible."""
        # Add response to content (menu stays persistent)
        self.add_content("", "white")  # Spacing
        for line in response:
            self.add_content(line, "green")
            
        self.display()
        
    def exit_vending_machine(self):
        """Clear vending machine menu."""
        self.clear_menu()
        
    def display_error(self, error_message: str):
        """Display error message."""
        self.add_content(f"ERROR: {error_message}", "bold red")
        self.display()
        
    def display_response(self, response: List[str]):
        """Display game response."""
        for line in response:
            if line.strip():
                self.add_content(line, "white")
                
        self.display()