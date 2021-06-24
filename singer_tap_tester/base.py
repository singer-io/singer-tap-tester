import unittest
import os

class EnableSubTests(type):
    """
    Defines a metaclass that marks any class defined outside of
    this module as a runnable test case.

    This is to prevent runners like `pytest` from picking up
    BaseTest and StandardTests multiple times, since they are
    marked with `__test__ = False` while still enabling
    subclasses of these types to be:

    1. Standard `TestCase`s
    2. Discovered by runners
    3. Executed with the checks provided in BaseTest and/or the
       standard tests defined in StandardTests
    """
    def __init__(cls, clsname, bases, clsdict):
       if clsdict['__module__'] != __name__:
           cls.__test__ = True

class BaseTest(unittest.TestCase, metaclass=EnableSubTests):
    # This is the test that will enforce any implementation requirements
    # Setup and/or standard test entry point or something similar where it can check if thjings like "tap-name" or "scenario-name" or "config" are all defined
    __test__ = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_config_environment()

    def config_environment(self):
        raise NotImplementedError("TestCases derived from singer_tap_tester.BaseTest must implement `config_environment`.")

    def check_config_environment(self):
        missing_envs = [x for x in self.config_environment()
                        if os.getenv(x) is None]
        if missing_envs:
            raise Exception(f"Missing environment variables: {missing_envs}")

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

class StandardTests(BaseTest):
    """
    Class that contains the standard set of tests that exercise a
    tap in a generic fashion. Tests are populated dynamically below
    for flexibility in testing and usage.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def config_environment(self):
        raise NotImplementedError(f"Usage of singer_tap_tester.{self.__class__.__name__} must implement `config_environment`.")

for f in standard_test_functions:
    setattr(StandardTests, f.__name__, f)
