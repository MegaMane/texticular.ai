from texticular.character import Player
from pytest import approx, raises
"""
Example of function based test suite with xunit setup and teardown
"""
# at command line pytest -v -s
# -v = verbose mode see results of each test run
# -s = see results of print statement on console


def setup_module(function):
    """runs once before any unit test or individual setup/teardown func"""
    print("Setup Module!")

def teardwon_module(function):
    """runs once before after all unit tests or individual setup/teardown func have run"""
    print("Teardown Module!")
def setup_function(function):
    """Runs once before each test"""
    if function == test_player:
        print("setting up test player")
    else:
        print("Setting up everything else")

def teardown_function(function):
    if function == test_player:
        print("tearing down test player")
    else:
        print("tearind down everything else")

def test_player():
    player = Player(
        key_value="test_player",
        name="Test Player", 
        descriptions={"Main": "A test player character"}
    )
    assert player is not None
    assert player.key_value == "test_player"
    assert player.name == "Test Player"
    assert player.hpoo == 80  # Default value
    assert player.money == 0.00  # Default value

def test_floating_point():
    assert (1.2 + 2.5) == approx(3.7)

def test_exception():
    with raises(ValueError):
        raisesValueException("a")

def raisesValueException(arg):
    if arg == "a":
        raise ValueError