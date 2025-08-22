import pytest

from texticular.game_loader import GameLoader
from unittest.mock import  MagicMock
from pytest import raises

@pytest.fixture()
def loader():
    loader = GameLoader()
    return loader

@pytest.fixture()
def mock_open(monkeypatch):
    mock_file = MagicMock()
    mock_file.readline = MagicMock(return_value="test line")
    mock_open = MagicMock(return_value=mock_file)
    monkeypatch.setattr("builtins.open", mock_open)
    return mock_open


#@pytest.mark.skip
def test_returnsCorrectString(loader,mock_open,monkeypatch):
    mock_exists = MagicMock(return_value=True)
    monkeypatch.setattr("os.path.exists", mock_exists)
    result = loader.readFromFile("somefile.txt")
    mock_open.assert_called_once_with("somefile.txt","r")
    assert result == "test line"

def test_thowsExceptionWithBafFile(loader,mock_open,monkeypatch):
    mock_exists = MagicMock(return_value=False)
    monkeypatch.setattr("os.path.exists", mock_exists)
    with raises(FileNotFoundError):
        result = loader.readFromFile("somfile.txt")
