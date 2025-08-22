from texticular.game_controller import Controller
import pytest
import unittest.mock

@pytest.fixture()
def setup():
    print("\nSetup")
    yield
    print("\ntearing down setup func")

@pytest.fixture(autouse=True)
def autosetup():
    print("\nRunning this mother fucker across the board!")
    yield
    print("\nTearing this mother fucker down!")

@pytest.fixture()
def boilerplate():
    return  Controller()

#option 1 pass in setup as a param to test 1 so that it gets called before test1
def test1(setup):
    print("Executing test1")
    assert True

#option 2 use this decorator to mark setup as a function to call before test2
@pytest.mark.usefixtures("setup")
def test2():
    print("Excuting test2")
    assert True

def test_controller(boilerplate):
    assert boilerplate
