"""
Text formatting utilities for improved UI display.
Handles intelligent text wrapping, spacing, and content organization.
"""

import re
from typing import List, Union, Dict, Any
from rich.text import Text


class TextFormatter:
    """Handles intelligent text formatting for UI display."""
    
    def __init__(self, width: int = 70):
        self.width = width
        
    def format_game_content(self, room_name: str, description: str, exits: List[str], 
                          last_response: str = "") -> List[Text]:
        """Format complete game content with proper spacing and organization."""
        content = []
        
        # Location header with icon and proper spacing
        location_text = Text(f"📍 {room_name}", style="bold yellow")
        content.append(location_text)
        content.append(Text())  # Empty line after header
        
        # Format room description with intelligent wrapping
        if description:
            formatted_desc = self.format_description_text(description)
            content.extend(formatted_desc)
            content.append(Text())  # Empty line after description
        
        # Add last response (like vending machine menu, container contents, etc.)
        if last_response:
            formatted_response = self.format_response_text(last_response)
            content.extend(formatted_response)
            content.append(Text())  # Empty line after response
        
        # Exits section with proper formatting
        if exits:
            content.append(Text("🚪 Exits:", style="bold green"))
            for exit_info in exits:
                formatted_exit = self.format_exit_text(exit_info)
                content.append(formatted_exit)
        
        return content
    
    def format_description_text(self, description: str) -> List[Text]:
        """Format room description with intelligent paragraph breaks."""
        content = []
        
        # Clean up the description and split into logical sections
        sections = self.split_into_sections(description)
        
        for i, section in enumerate(sections):
            if section.strip():
                # Wrap text intelligently
                wrapped_lines = self.intelligent_wrap(section.strip(), self.width)
                for line in wrapped_lines:
                    content.append(Text(line, style="white"))
                
                # Add spacing between sections (but not after the last one)
                if i < len(sections) - 1:
                    content.append(Text())
        
        return content
    
    def format_response_text(self, response: str) -> List[Text]:
        """Format game responses like vending machine menus, container contents, etc."""
        content = []
        
        # Handle different types of responses
        if self.is_vending_machine_response(response):
            content.extend(self.format_vending_machine_response(response))
        elif self.is_container_contents_response(response):
            content.extend(self.format_container_contents_response(response))
        elif self.is_dialogue_response(response):
            content.extend(self.format_dialogue_response(response))
        else:
            # Standard response formatting
            content.extend(self.format_standard_response(response))
        
        return content
    
    def format_vending_machine_response(self, response: str) -> List[Text]:
        """Format vending machine menu with proper styling."""
        content = []
        lines = response.split('\n')
        
        current_section = []
        for line in lines:
            line = line.strip()
            if not line:
                if current_section:
                    # Process the current section
                    section_text = '\n'.join(current_section)
                    if '***' in section_text:
                        # Header section
                        content.append(Text(section_text, style="bold cyan"))
                    elif 'MENU' in section_text or '====' in section_text:
                        # Menu header section  
                        content.append(Text(section_text, style="bold green"))
                    elif any(c.isdigit() and ('$' in section_text or 'left)' in section_text) for c in section_text):
                        # Menu items
                        content.append(Text(section_text, style="green"))
                    elif 'Commands:' in section_text:
                        # Instructions
                        content.append(Text(section_text, style="yellow"))
                    else:
                        content.append(Text(section_text, style="white"))
                    
                    current_section = []
                    content.append(Text())  # Spacing between sections
            else:
                current_section.append(line)
        
        # Process any remaining section
        if current_section:
            section_text = '\n'.join(current_section)
            content.append(Text(section_text, style="white"))
        
        return content
    
    def format_container_contents_response(self, response: str) -> List[Text]:
        """Format container contents with proper styling."""
        content = []
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                content.append(Text())
            elif '---' in line or '===' in line:
                content.append(Text(line, style="dim cyan"))
            elif ':' in line and ('inside' in line.lower() or 'see' in line.lower()):
                content.append(Text(line, style="bold cyan"))
            else:
                content.append(Text(line, style="green"))
        
        return content
    
    def format_dialogue_response(self, response: str) -> List[Text]:
        """Format NPC dialogue responses."""
        content = []
        # For dialogue, we want to preserve the existing dialogue UI
        # This is handled separately by the dialogue system
        content.append(Text(response, style="magenta"))
        return content
    
    def format_standard_response(self, response: str) -> List[Text]:
        """Format standard game responses."""
        content = []
        
        # Handle multi-line responses
        if '\n' in response:
            lines = response.split('\n')
            for line in lines:
                if line.strip():
                    wrapped = self.intelligent_wrap(line.strip(), self.width)
                    for wrapped_line in wrapped:
                        content.append(Text(wrapped_line, style="cyan"))
                else:
                    content.append(Text())
        else:
            wrapped = self.intelligent_wrap(response, self.width)
            for wrapped_line in wrapped:
                content.append(Text(wrapped_line, style="cyan"))
        
        return content
    
    def format_exit_text(self, exit_info: str) -> Text:
        """Format individual exit information."""
        # Clean up and format exit descriptions
        if ':' in exit_info:
            direction, description = exit_info.split(':', 1)
            direction = direction.strip()
            description = description.strip()
            
            # Wrap description if too long
            if len(description) > 50:
                wrapped_desc = self.intelligent_wrap(description, 50)[0] + "..."
            else:
                wrapped_desc = description
                
            return Text(f"  {direction}: {wrapped_desc}", style="green")
        else:
            return Text(f"  {exit_info}", style="green")
    
    def split_into_sections(self, text: str) -> List[str]:
        """Split text into logical sections for better formatting."""
        # Clean up the input text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split on common section boundaries
        # Look for patterns that indicate new sections
        section_patterns = [
            r'\. To the ',  # Room description to exits
            r'\. The ',     # Between different description elements
            r'\. A ',       # New object descriptions
            r'\. There ',   # Location-based descriptions
            r'\. Against ', # Furniture descriptions
            r'\. Next to ', # Spatial relationships
        ]
        
        sections = [text]
        for pattern in section_patterns:
            new_sections = []
            for section in sections:
                parts = re.split(f'({pattern})', section)
                current_part = ""
                for i, part in enumerate(parts):
                    if re.match(pattern, part):
                        if current_part.strip():
                            new_sections.append(current_part.strip() + '.')
                        current_part = part
                    else:
                        current_part += part
                
                if current_part.strip():
                    new_sections.append(current_part.strip())
            
            sections = new_sections
        
        # Filter out very short sections and combine them
        filtered_sections = []
        for section in sections:
            if len(section.strip()) < 20 and filtered_sections:
                # Combine short sections with previous
                filtered_sections[-1] += " " + section
            else:
                filtered_sections.append(section)
        
        return filtered_sections
    
    def intelligent_wrap(self, text: str, width: int) -> List[str]:
        """Wrap text intelligently, preserving word boundaries and readability."""
        if not text or len(text) <= width:
            return [text]
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            # Check if adding this word would exceed the width
            if current_length + word_length + len(current_line) > width:
                if current_line:  # If we have words in current line
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_length = word_length
                else:  # Single word is too long
                    if word_length > width:
                        # Split long words
                        lines.append(word[:width])
                        current_line = [word[width:]] if len(word) > width else []
                        current_length = len(word[width:]) if len(word) > width else 0
                    else:
                        current_line = [word]
                        current_length = word_length
            else:
                current_line.append(word)
                current_length += word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def is_vending_machine_response(self, response: str) -> bool:
        """Check if response is from vending machine."""
        vending_indicators = [
            'FAST EDDIE', 'VENDING MACHINE', 'MENU', 
            'Insert coins', 'Buy item', '$0.50', '$2.50'
        ]
        return any(indicator in response for indicator in vending_indicators)
    
    def is_container_contents_response(self, response: str) -> bool:
        """Check if response is container contents."""
        container_indicators = [
            'look inside', 'You look inside', '---', 'see...'
        ]
        return any(indicator in response for indicator in container_indicators)
    
    def is_dialogue_response(self, response: str) -> bool:
        """Check if response is dialogue."""
        # Dialogue responses are handled by the dialogue system UI
        return False  # For now, let dialogue system handle its own formatting


def format_for_web(content: List[Text]) -> str:
    """Convert formatted content to HTML for web display."""
    html_parts = []
    
    for text_obj in content:
        if isinstance(text_obj, Text):
            if not text_obj.plain:  # Empty line
                html_parts.append("<br>")
            else:
                # Convert Rich styles to CSS classes
                style_class = ""
                if hasattr(text_obj, 'style') and text_obj.style:
                    style_class = f' class="text-{text_obj.style}"'
                html_parts.append(f"<p{style_class}>{text_obj.plain}</p>")
        else:
            html_parts.append(f"<p>{str(text_obj)}</p>")
    
    return '\n'.join(html_parts)


def format_for_plain_text(content: List[Text]) -> str:
    """Convert formatted content to plain text."""
    lines = []
    
    for text_obj in content:
        if isinstance(text_obj, Text):
            lines.append(text_obj.plain if text_obj.plain else "")
        else:
            lines.append(str(text_obj))
    
    return '\n'.join(lines)