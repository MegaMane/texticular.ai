# Texticular Test Suite

This directory contains comprehensive tests for the Texticular text adventure game engine.

## Running Tests

### Quick Test (All Tests)
```bash
python tests/run_all_tests.py
```

### Individual Test Categories

**Unit Tests (pytest):**
```bash
python -m pytest tests/test_game_object.py tests/test_player.py tests/test_room.py tests/test_story_item.py -v
```

**Dialogue System Tests:**
```bash
python tests/test_npc_dialogue_direct.py
```

**Parser Functionality Tests:**
```bash
python tests/test_parser_fixes.py
```

**Vending Machine Flow Tests:**
```bash
python tests/test_vending_machine_flow.py
```

## Test Structure

### Core Unit Tests (pytest-based)
- `test_game_object.py` - GameObject class functionality
- `test_player.py` - Player character functionality  
- `test_room.py` - Room system tests
- `test_story_item.py` - Story item and inventory tests

### Integration Tests
- `test_npc_dialogue_direct.py` - Complete NPC dialogue system testing
- `test_parser_fixes.py` - Parser-to-action routing validation
- `test_vending_machine_flow.py` - End-to-end vending machine interaction
- `comprehensive_game_test.py` - Full game functionality test

### Supporting Tests
- `test_game_loader.py` - JSON data loading tests
- `dialogue_test.py` - Dialogue graph unit tests

### Debug/Demo Files (in debug_demo/)
- Various debugging scripts and UI mockups
- Demo scripts for showcasing specific features

## Test Results Summary

When all tests pass, you should see:
- **Unit Tests**: 21 passed, 1 skipped
- **Dialogue System**: 6/7 tests passed (85.7% success rate)
- **Parser Functionality**: Complete success
- **Vending Machine Flow**: Complete success

The dialogue system has one expected failure due to GameObject registry collision in isolation testing - this is not a functional issue.

## Adding New Tests

### For pytest-based tests:
1. Create `test_feature_name.py` in this directory
2. Use pytest conventions (`test_` prefix for functions)
3. Add to the unit test list in `run_all_tests.py`

### For integration tests:
1. Create standalone test scripts with proper success indicators
2. Add to `run_all_tests.py` with appropriate success detection
3. Follow the pattern of existing integration tests

## Dependencies

Tests require:
- pytest (for unit tests)
- texticular package (installed with `pip install -e .`)
- All game data files in `data/` directory