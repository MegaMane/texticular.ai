"""
Gameplay Logger for Texticular
Logs all game actions, state changes, and player behavior for analysis
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import threading
import os


class GameplayLogger:
    """
    Logs gameplay sessions with detailed state tracking.
    Creates JSON logs that can be monitored in real-time.
    """
    
    def __init__(self, session_name: str = None):
        self.session_name = session_name or f"session_{int(time.time())}"
        self.log_dir = Path("gameplay_logs")
        self.log_dir.mkdir(exist_ok=True)
        
        # Main log file
        self.log_file = self.log_dir / f"{self.session_name}.json"
        self.live_file = self.log_dir / "current_session.json"
        
        # Session data
        self.session_data = {
            "session_id": self.session_name,
            "start_time": datetime.now().isoformat(),
            "events": [],
            "current_state": {},
            "statistics": {
                "commands_entered": 0,
                "rooms_visited": set(),
                "items_interacted": set(),
                "failed_commands": 0,
                "successful_commands": 0
            }
        }
        
        self.is_active = True
        
    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log a gameplay event with timestamp."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data
        }
        
        self.session_data["events"].append(event)
        self._update_statistics(event_type, data)
        self._save_logs()
        
    def log_command(self, command: str, parse_success: bool, response: str, game_state: Dict[str, Any]):
        """Log a player command with full context."""
        self.log_event("command", {
            "input": command,
            "parse_success": parse_success,
            "response": response,
            "game_state": game_state.copy() if game_state else {},
            "turn": game_state.get("turn", 0) if game_state else 0
        })
        
        # Update current state
        self.session_data["current_state"] = game_state.copy() if game_state else {}
        
    def log_room_change(self, from_room: str, to_room: str, method: str = "walk"):
        """Log room transitions."""
        self.log_event("room_change", {
            "from_room": from_room,
            "to_room": to_room,
            "method": method
        })
        
        self.session_data["statistics"]["rooms_visited"].add(to_room)
        
    def log_item_interaction(self, item_name: str, action: str, success: bool):
        """Log item interactions."""
        self.log_event("item_interaction", {
            "item": item_name,
            "action": action,
            "success": success
        })
        
        if success:
            self.session_data["statistics"]["items_interacted"].add(item_name)
    
    def log_game_state_change(self, state_name: str, old_value: Any, new_value: Any):
        """Log specific game state changes."""
        self.log_event("state_change", {
            "state": state_name,
            "old_value": old_value,
            "new_value": new_value
        })
    
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None):
        """Log game errors and crashes."""
        self.log_event("error", {
            "error_type": error_type,
            "message": error_message,
            "context": context or {}
        })
    
    def _update_statistics(self, event_type: str, data: Dict[str, Any]):
        """Update session statistics."""
        stats = self.session_data["statistics"]
        
        if event_type == "command":
            stats["commands_entered"] += 1
            if data.get("parse_success", False):
                stats["successful_commands"] += 1
            else:
                stats["failed_commands"] += 1
        
        # Convert sets to lists for JSON serialization
        stats["rooms_visited"] = list(stats["rooms_visited"])
        stats["items_interacted"] = list(stats["items_interacted"])
    
    def _save_logs(self):
        """Save logs to both main file and live monitoring file."""
        try:
            # Save to main session file
            with open(self.log_file, 'w') as f:
                json.dump(self.session_data, f, indent=2, default=str)
            
            # Save to live monitoring file (for real-time watching)
            with open(self.live_file, 'w') as f:
                json.dump(self.session_data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Warning: Could not save gameplay logs: {e}")
    
    def end_session(self):
        """End the logging session."""
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["duration"] = (
            datetime.now() - datetime.fromisoformat(self.session_data["start_time"])
        ).total_seconds()
        
        self._save_logs()
        self.is_active = False
        
        print(f"📊 Gameplay session saved to: {self.log_file}")
        print(f"📈 Session stats: {self.session_data['statistics']['commands_entered']} commands, "
              f"{len(self.session_data['statistics']['rooms_visited'])} rooms visited")
    
    def get_recent_events(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent events."""
        return self.session_data["events"][-count:]
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current game state."""
        return self.session_data["current_state"]


# Global logger instance
_gameplay_logger = None

def start_logging(session_name: str = None) -> GameplayLogger:
    """Start gameplay logging."""
    global _gameplay_logger
    _gameplay_logger = GameplayLogger(session_name)
    return _gameplay_logger

def get_logger() -> GameplayLogger:
    """Get the current gameplay logger."""
    global _gameplay_logger
    if _gameplay_logger is None:
        _gameplay_logger = start_logging()
    return _gameplay_logger

def stop_logging():
    """Stop gameplay logging."""
    global _gameplay_logger
    if _gameplay_logger:
        _gameplay_logger.end_session()
        _gameplay_logger = None