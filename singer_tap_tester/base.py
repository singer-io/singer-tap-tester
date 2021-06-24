import unittest
import os

class EnableSubTests(type):
    """
    Defines a metaclass that marks any class defined outside of
    this module as a runnable test case.

    This is to prevent runners like `pytest` from picking up
    BaseTapTest and StandardTests multiple times, since they are
    marked with `__test__ = False` while still enabling
    subclasses of these types to be:

    1. Standard `TestCase`s
    2. Discovered by runners
    3. Executed with the checks provided in BaseTapTest and/or the
       standard tests defined in StandardTests
    """
    def __init__(cls, clsname, bases, clsdict):
       if clsdict.get('__module__') != __name__:
           cls.__test__ = True

class BaseTapTest(unittest.TestCase, metaclass=EnableSubTests):
    # Prevents this from being discovered as a test itself
    __test__ = False

    # Required for a fully formed tap-test to be implemented
    required_subclass_functions = ["config_environment", "tap_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_subclass_requirements()
        self.check_config_environment()

    def check_subclass_requirements(self):
        missing_implementations = [req for req in self.required_subclass_functions
                                   if not hasattr(self, req)]
        if missing_implementations:
            raise NotImplementedError(f"{self.__class__.__name__}: TestCases derived from singer_tap_tester.BaseTapTest must implement these functions (see `{self.__class__.__name__}.required_subclass_functions` for the full list): {missing_implementations}")

    def check_config_environment(self):
        missing_envs = [x for x in self.config_environment()
                        if os.getenv(x) is None]
        if missing_envs:
            raise Exception(f"Missing environment variables required to run the tap for this test: {missing_envs}")

def test_sync_canary(scenario):
    # Do the test and assertions here
    print("Did canary test!")
    pass

def test_discovery(scenario):
    print("Did discovery test!")
    pass

standard_test_functions = {
    test_sync_canary,
    test_discovery,
    }

class StandardTests(BaseTapTest):
    """
    Class that contains the standard set of tests that exercise a
    tap in a generic fashion. Tests are populated dynamically below
    for flexibility in testing and usage.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def runTest(self):
        for test_fun in standard_test_functions:
            with self.subTest(test_fun.__name__):
                test_fun(self)
