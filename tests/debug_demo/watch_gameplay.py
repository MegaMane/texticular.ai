#!/usr/bin/env python3
"""
Real-time Gameplay Monitor for Texticular
Watches gameplay logs and provides live analysis
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.table import Table
from rich import box


class GameplayMonitor:
    """Monitors gameplay logs in real-time."""
    
    def __init__(self):
        self.console = Console()
        self.log_file = Path("gameplay_logs/current_session.json")
        self.last_event_count = 0
        self.session_data = None
        
    def load_session_data(self):
        """Load the current session data."""
        if not self.log_file.exists():
            return None
            
        try:
            with open(self.log_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def create_layout(self):
        """Create the monitor layout."""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1)
        )
        
        layout["body"].split_row(
            Layout(name="events", ratio=2),
            Layout(name="stats", ratio=1)
        )
        
        return layout
    
    def create_header(self):
        """Create the header panel."""
        title = Text("🔍 TEXTICULAR GAMEPLAY MONITOR", style="bold cyan")
        if self.session_data:
            subtitle = Text(f"Session: {self.session_data.get('session_id', 'Unknown')}", style="dim")
            return Panel(f"{title}\n{subtitle}", box=box.DOUBLE, style="cyan")
        return Panel(title, box=box.DOUBLE, style="cyan")
    
    def create_events_panel(self, recent_events):
        """Create the recent events panel."""
        if not recent_events:
            return Panel("No events yet...", title="Recent Events", style="yellow")
        
        content = []
        for event in recent_events[-10:]:  # Show last 10 events
            timestamp = event.get("timestamp", "")
            event_type = event.get("event_type", "unknown")
            data = event.get("data", {})
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = timestamp[-8:]  # Last 8 chars
            
            # Format event based on type
            if event_type == "command":
                cmd = data.get("input", "")
                success = "✅" if data.get("parse_success", False) else "❌"
                response = data.get("response", "")[:50] + "..." if len(data.get("response", "")) > 50 else data.get("response", "")
                content.append(Text(f"{time_str} {success} >> {cmd}", style="white"))
                if response:
                    content.append(Text(f"    {response}", style="dim"))
                    
            elif event_type == "room_change":
                from_room = data.get("from_room", "")
                to_room = data.get("to_room", "")
                content.append(Text(f"{time_str} 🚪 {from_room} → {to_room}", style="green"))
                
            elif event_type == "item_interaction":
                item = data.get("item", "")
                action = data.get("action", "")
                success = "✅" if data.get("success", False) else "❌"
                content.append(Text(f"{time_str} {success} 🎒 {action} {item}", style="blue"))
                
            elif event_type == "error":
                error_msg = data.get("message", "")
                content.append(Text(f"{time_str} 💥 ERROR: {error_msg}", style="red"))
                
            else:
                content.append(Text(f"{time_str} 📝 {event_type}: {str(data)[:50]}", style="dim"))
        
        return Panel("\n".join([str(c) for c in content]), 
                    title="Recent Events", 
                    box=box.ROUNDED, 
                    style="white")
    
    def create_stats_panel(self, stats, current_state):
        """Create the statistics panel."""
        content = []
        
        # Session stats
        content.append(Text("📊 SESSION STATS", style="bold magenta"))
        content.append("")
        
        if stats:
            content.append(Text(f"Commands: {stats.get('commands_entered', 0)}", style="cyan"))
            content.append(Text(f"Successful: {stats.get('successful_commands', 0)}", style="green"))
            content.append(Text(f"Failed: {stats.get('failed_commands', 0)}", style="red"))
            content.append(Text(f"Rooms visited: {len(stats.get('rooms_visited', []))}", style="cyan"))
            content.append(Text(f"Items used: {len(stats.get('items_interacted', []))}", style="cyan"))
        
        content.append("")
        
        # Current game state
        content.append(Text("🎮 CURRENT STATE", style="bold yellow"))
        content.append("")
        
        if current_state:
            content.append(Text(f"Room: {current_state.get('room_name', 'Unknown')}", style="yellow"))
            content.append(Text(f"Turn: {current_state.get('turn', 0)}", style="yellow"))
            content.append(Text(f"Score: {current_state.get('score', 0)}", style="yellow"))
            content.append(Text(f"Poop Level: {current_state.get('poop_level', 0)}%", style="red"))
            
            inventory = current_state.get('inventory', [])
            if inventory:
                content.append(Text("Inventory:", style="blue"))
                for item in inventory[:5]:  # Show max 5 items
                    content.append(Text(f"  • {item}", style="dim blue"))
        
        content.append("")
        content.append(Text("💡 OBSERVATIONS", style="bold green"))
        content.append("")
        
        # AI Analysis
        if stats and stats.get('commands_entered', 0) > 0:
            success_rate = (stats.get('successful_commands', 0) / stats.get('commands_entered', 1)) * 100
            content.append(Text(f"Success rate: {success_rate:.1f}%", 
                              style="green" if success_rate > 80 else "yellow" if success_rate > 60 else "red"))
            
            if stats.get('failed_commands', 0) > 3:
                content.append(Text("🤔 Player struggling with commands", style="orange"))
            
            if len(stats.get('rooms_visited', [])) > 3:
                content.append(Text("🗺️  Good exploration pattern", style="green"))
        
        return Panel("\n".join([str(c) for c in content]), 
                    title="Statistics & Analysis", 
                    box=box.ROUNDED, 
                    style="magenta")
    
    def generate_renderable(self):
        """Generate the complete UI for live display."""
        # Load current session data
        self.session_data = self.load_session_data()
        
        if not self.session_data:
            return Panel("Waiting for gameplay session to start...\nRun the game with logging enabled!", 
                        title="No Active Session", 
                        style="dim")
        
        # Create layout
        layout = self.create_layout()
        
        # Get data
        events = self.session_data.get("events", [])
        stats = self.session_data.get("statistics", {})
        current_state = self.session_data.get("current_state", {})
        
        # Populate layout
        layout["header"].update(self.create_header())
        layout["events"].update(self.create_events_panel(events))
        layout["stats"].update(self.create_stats_panel(stats, current_state))
        
        return layout
    
    def run(self):
        """Run the real-time monitor."""
        self.console.print("🔍 Starting Texticular Gameplay Monitor...")
        self.console.print("This will update in real-time as you play the game!")
        self.console.print("Press Ctrl+C to exit")
        self.console.print()
        
        try:
            with Live(self.generate_renderable(), refresh_per_second=2, console=self.console) as live:
                while True:
                    live.update(self.generate_renderable())
                    time.sleep(0.5)  # Update twice per second
                    
        except KeyboardInterrupt:
            self.console.print("\n👋 Monitor stopped!")


if __name__ == "__main__":
    monitor = GameplayMonitor()
    monitor.run()