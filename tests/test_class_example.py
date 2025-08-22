from texticular.game_object import GameObject

class TestGameObject:
    """Example of a test class with Xunit Style setup and teardown"""
    @classmethod
    def setup_class(cls):
        print("Setup TestClass!")

    @classmethod
    def teardown_class(cls):
        print("Teardown TestClass!")

    def setup_method(self, function):
        """Runs once before each test"""
        if function == self.test_canCreateGameObject:
            print("setting up test_canCreateGameObject")
        else:
            print("Setting up everything else")

    def teardown_method(self, function):
        if function == self.test_canCreateGameObject:
            print("tearing down test_canCreateGameObject")
        else:
            print("tearind down everything else")

    def test_canCreateGameObject(self):
        assert GameObject()
