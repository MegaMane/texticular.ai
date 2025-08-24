"""
JSON Schema validation utilities for Texticular game content.
Provides validation for game data files using JSON Schema.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import jsonschema
from jsonschema import validate, ValidationError


class GameContentValidator:
    """Validates Texticular game content against JSON schemas."""
    
    def __init__(self, schema_dir: Optional[str] = None):
        """Initialize validator with schema directory."""
        if schema_dir is None:
            # Default to project schemas directory
            project_root = Path(__file__).parent.parent.parent.parent
            schema_dir = project_root / "schemas"
        
        self.schema_dir = Path(schema_dir)
        self.schemas: Dict[str, Dict[str, Any]] = {}
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all JSON schemas from the schema directory."""
        if not self.schema_dir.exists():
            print(f"Warning: Schema directory {self.schema_dir} not found")
            return
            
        for schema_file in self.schema_dir.glob("*.json"):
            try:
                with open(schema_file, 'r') as f:
                    schema = json.load(f)
                    schema_name = schema_file.stem
                    self.schemas[schema_name] = schema
                    print(f"Loaded schema: {schema_name}")
            except Exception as e:
                print(f"Error loading schema {schema_file}: {e}")
    
    def validate_game_content(self, content: Dict[str, Any], 
                            schema_name: str = "game_content_schema") -> List[str]:
        """
        Validate game content against the specified schema.
        
        Args:
            content: The game content to validate
            schema_name: Name of the schema to use (without .json extension)
            
        Returns:
            List of validation error messages (empty if valid)
        """
        if schema_name not in self.schemas:
            return [f"Schema '{schema_name}' not found. Available schemas: {list(self.schemas.keys())}"]
        
        schema = self.schemas[schema_name]
        errors = []
        
        try:
            validate(instance=content, schema=schema)
        except ValidationError as e:
            errors.append(f"Validation error: {e.message}")
            if e.path:
                errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        except Exception as e:
            errors.append(f"Unexpected validation error: {e}")
        
        return errors
    
    def validate_file(self, file_path: str, 
                     schema_name: str = "game_content_schema") -> List[str]:
        """
        Validate a JSON file against the specified schema.
        
        Args:
            file_path: Path to the JSON file to validate
            schema_name: Name of the schema to use
            
        Returns:
            List of validation error messages (empty if valid)
        """
        try:
            with open(file_path, 'r') as f:
                content = json.load(f)
            return self.validate_game_content(content, schema_name)
        except FileNotFoundError:
            return [f"File not found: {file_path}"]
        except json.JSONDecodeError as e:
            return [f"Invalid JSON in {file_path}: {e}"]
        except Exception as e:
            return [f"Error reading {file_path}: {e}"]
    
    def get_available_schemas(self) -> List[str]:
        """Get list of available schema names."""
        return list(self.schemas.keys())


def validate_game_files(game_data_dir: str, validator: Optional[GameContentValidator] = None) -> Dict[str, List[str]]:
    """
    Validate all JSON files in the game data directory.
    
    Args:
        game_data_dir: Directory containing game JSON files
        validator: GameContentValidator instance (creates new one if None)
        
    Returns:
        Dictionary mapping file paths to validation error lists
    """
    if validator is None:
        validator = GameContentValidator()
    
    results = {}
    data_dir = Path(game_data_dir)
    
    if not data_dir.exists():
        return {str(data_dir): ["Directory not found"]}
    
    for json_file in data_dir.glob("*.json"):
        errors = validator.validate_file(str(json_file))
        results[str(json_file)] = errors
    
    return results


# CLI utility for validation
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python schema_validator.py <json_file> [schema_name]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    schema_name = sys.argv[2] if len(sys.argv) > 2 else "game_content_schema"
    
    validator = GameContentValidator()
    errors = validator.validate_file(file_path, schema_name)
    
    if errors:
        print(f"Validation errors in {file_path}:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"✅ {file_path} is valid according to {schema_name} schema")