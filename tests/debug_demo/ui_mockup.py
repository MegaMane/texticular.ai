#!/usr/bin/env python3
"""
Rich UI Mockup for Texticular - Fixed Layout Design
Shows how the new interface will look and behave
"""

import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.columns import Columns
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

def create_game_layout():
    """Create the main game layout with fixed areas."""
    
    # Create main layout
    layout = Layout()
    
    # Split into header, body, footer
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=5)
    )
    
    # Split body into game area and HUD
    layout["body"].split_row(
        Layout(name="game", ratio=3),
        Layout(name="hud", size=25)
    )
    
    return layout

def create_header():
    """Create the game header with title."""
    title = Text("TEXTICULAR: Chapter 1 - You Gotta Go!", style="bold cyan")
    return Panel(Align.center(title), box=box.DOUBLE, style="cyan")

def create_game_area(room_name, description, exits):
    """Create the main game content area."""
    content = []
    
    # Location header
    location_text = Text(f"📍 {room_name}", style="bold yellow")
    content.append(location_text)
    content.append("")
    
    # Room description
    desc_lines = description.split(". ")
    for line in desc_lines:
        if line.strip():
            content.append(Text(line.strip() + ".", style="white"))
    
    content.append("")
    
    # Exits
    if exits:
        content.append(Text("🚪 Exits:", style="bold green"))
        for exit_info in exits:
            content.append(Text(f"  {exit_info}", style="green"))
    
    return Panel("\n".join([str(c) for c in content]), 
                title="Game World", 
                box=box.ROUNDED, 
                style="white")

def create_hud(turn, score, location, poop_level=75):
    """Create the HUD/status area."""
    hud_content = []
    
    # Game stats
    hud_content.append(Text("📊 GAME STATUS", style="bold magenta"))
    hud_content.append("")
    hud_content.append(Text(f"Turn: {turn}", style="cyan"))
    hud_content.append(Text(f"Score: {score}", style="cyan"))
    hud_content.append(Text(f"Location: {location}", style="cyan"))
    hud_content.append("")
    
    # Poop meter (the most important stat!)
    hud_content.append(Text("💩 URGENCY METER", style="bold red"))
    poop_bar = "█" * (poop_level // 5) + "░" * (20 - poop_level // 5)
    poop_color = "red" if poop_level > 80 else "yellow" if poop_level > 50 else "green"
    hud_content.append(Text(f"[{poop_bar}] {poop_level}%", style=poop_color))
    
    if poop_level > 90:
        hud_content.append(Text("🚨 CRITICAL!", style="bold red blink"))
    elif poop_level > 70:
        hud_content.append(Text("⚠️ Urgent!", style="bold yellow"))
    
    hud_content.append("")
    
    # Inventory preview
    hud_content.append(Text("🎒 INVENTORY", style="bold blue"))
    hud_content.append(Text("• Backpack", style="blue"))
    hud_content.append(Text("• Note", style="blue"))
    hud_content.append("")
    
    # Controls help
    hud_content.append(Text("💡 QUICK HELP", style="bold green"))
    hud_content.append(Text("look - examine area", style="dim"))
    hud_content.append(Text("go <dir> - move", style="dim"))
    hud_content.append(Text("i - inventory", style="dim"))
    hud_content.append(Text("sit/use/take", style="dim"))
    
    return Panel("\n".join([str(c) for c in hud_content]), 
                title="Status", 
                box=box.ROUNDED, 
                style="magenta")

def create_footer(last_command, response):
    """Create the command/response footer."""
    # Last command and response
    footer_content = []
    
    if last_command:
        footer_content.append(Text(f">> {last_command}", style="bold white"))
    
    if response:
        # Limit response to fit in footer area
        response_text = response[:200] + "..." if len(response) > 200 else response
        footer_content.append(Text(response_text, style="yellow"))
    
    # Command prompt
    footer_content.append("")
    footer_content.append(Text("Enter command:", style="bold green"))
    
    return Panel("\n".join([str(c) for c in footer_content]), 
                title="Command", 
                box=box.ROUNDED, 
                style="green")

def mockup_demo():
    """Run the UI mockup demo."""
    console = Console()
    
    # Sample game states to cycle through
    game_states = [
        {
            "turn": 1,
            "score": 0,
            "room": "Room 201",
            "description": "You wake up disoriented with a pounding headache in a shabby looking hotel room surrounded by a bunch of empty cans. You've got a taste in your mouth like a dirty old rat crawled in and died in there. There is an obnoxious orange couch in the corner next to a small window smudged with sticky purple hand prints.",
            "exits": ["WEST - Bathroom (locked by dog)", "EAST - Hallway"],
            "last_command": "",
            "response": "Welcome to Texticular! Type 'look' to examine your surroundings.",
            "poop_level": 45
        },
        {
            "turn": 2,
            "score": 0,
            "room": "Room 201",
            "description": "You wake up disoriented with a pounding headache in a shabby looking hotel room surrounded by a bunch of empty cans. You've got a taste in your mouth like a dirty old rat crawled in and died in there. There is an obnoxious orange couch in the corner next to a small window smudged with sticky purple hand prints.",
            "exits": ["WEST - Bathroom (locked by dog)", "EAST - Hallway"],
            "last_command": "look at couch",
            "response": "There is an obnoxious orange couch in the corner. The cushions look lumpy and stained.",
            "poop_level": 52
        },
        {
            "turn": 3,
            "score": 5,
            "room": "Room 201",
            "description": "You wake up disoriented with a pounding headache in a shabby looking hotel room surrounded by a bunch of empty cans. You've got a taste in your mouth like a dirty old rat crawled in and died in there. You are sitting on the obnoxious orange couch. The cushions are lumpy and smell faintly of Fast Eddie's.",
            "exits": ["WEST - Bathroom (locked by dog)", "EAST - Hallway"],
            "last_command": "sit on couch",
            "response": "You sit on the couch. You are sitting on the obnoxious orange couch. The cushions are lumpy and smell faintly of Fast Eddie's.",
            "poop_level": 67
        },
        {
            "turn": 8,
            "score": 15,
            "room": "West Hallway",
            "description": "You eagerly enter the hallway leaving your room behind you to the West. The glow of the yellow fluorescent lights are complimented by the well-worn red carpet. The diamond pattern urges you forward.",
            "exits": ["NORTH - Room 203", "EAST - East Hallway", "SOUTH - Vending Machine", "WEST - Room 201"],
            "last_command": "go east",
            "response": "You walk east into the hallway. The fluorescent lights hum overhead.",
            "poop_level": 89
        },
        {
            "turn": 12,
            "score": 25,
            "room": "Vending Machine Alcove",
            "description": "The vending alcove is in stark contrast to the rest of your well-worn surroundings. The vending machine is shiny and new and stocked to the brim with Fast Eddie's colon cleanse, as well as some other interesting items.",
            "exits": ["NORTH - West Hallway"],
            "last_command": "use vending machine",
            "response": "🚨 CRITICAL POOP LEVEL! You need to find a bathroom NOW!",
            "poop_level": 95
        }
    ]
    
    print("🎮 TEXTICULAR UI MOCKUP - Press Ctrl+C to exit")
    print("This shows how the new fixed-layout interface will work...")
    time.sleep(2)
    
    try:
        for i, state in enumerate(game_states):
            # Clear screen
            os.system('clear' if os.name == 'posix' else 'cls')
            
            # Create layout
            layout = create_game_layout()
            
            # Populate layout
            layout["header"].update(create_header())
            layout["game"].update(create_game_area(
                state["room"], 
                state["description"], 
                state["exits"]
            ))
            layout["hud"].update(create_hud(
                state["turn"], 
                state["score"], 
                state["room"], 
                state["poop_level"]
            ))
            layout["footer"].update(create_footer(
                state["last_command"], 
                state["response"]
            ))
            
            # Render
            console.print(layout)
            
            # Show state info
            print(f"\n🎯 Mockup State {i+1}/5 - Showing: Turn {state['turn']}, Poop Level {state['poop_level']}%")
            time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n👋 Mockup demo ended!")

if __name__ == "__main__":
    mockup_demo()