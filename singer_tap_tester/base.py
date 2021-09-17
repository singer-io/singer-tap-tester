import unittest
import os

from .standard_tests import test_sync_canary, test_catalog_standards

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
    subclass_requirements = ["config_environment", "tap_name", "get_config"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_subclass_requirements()
        self.check_config_environment()

    def check_subclass_requirements(self):
        missing_implementations = [req for req in self.subclass_requirements
                                   if not hasattr(self, req)]
        if missing_implementations:
            raise NotImplementedError(f"{self.__class__.__name__}: TestCases derived from singer_tap_tester.BaseTapTest must implement these functions or properties (see `{self.__class__.__name__}.subclass_requirements` for the full list): {missing_implementations}")

    def check_config_environment(self):
        missing_envs = [x for x in self.config_environment()
                        if os.getenv(x) is None]
        if missing_envs:
            raise Exception(f"Missing environment variables required to run the tap for this test: {missing_envs}")

    # The following constants and methods will dynamically set the standard expectations

    PRIMARY_KEYS = "table-key-properties"
    REPLICATION_METHOD = "forced-replication-method"
    REPLICATION_KEYS = "valid-replication-keys"
    INCREMENTAL = "INCREMENTAL"
    FULL_TABLE = "FULL_TABLE"

    def expected_metadata(self):
        """A dummy dictionary meant to be overridden in a Test<Tap>Standard class"""
        return {}

    def expected_streams(self):
        """A set of expected stream names"""
        return set(self.expected_metadata().keys())

    def expected_primary_keys(self):
        """
        return a dictionary with key of stream name
        and value as a set of primary key fields
        """
        return {table: properties.get(self.PRIMARY_KEYS, set())
                for table, properties
                in self.expected_metadata().items()}

    def expected_replication_keys(self):
        """
        return a dictionary with key of table name
        and value as a set of replication key fields
        """
        return {table: properties.get(self.REPLICATION_KEYS, set())
                for table, properties
                in self.expected_metadata().items()}

    def expected_automatic_fields(self):
        auto_fields = {}
        for k, v in self.expected_metadata().items():
            auto_fields[k] = v.get(self.PRIMARY_KEYS, set()) | v.get(self.REPLICATION_KEYS, set())
        return auto_fields

    def expected_replication_method(self):
        """Return a dictionary with key of table name nd value of replication method"""
        return {table: properties.get(self.REPLICATION_METHOD)
                for table, properties
                in self.expected_metadata().items()}

standard_test_functions = {
    test_sync_canary,
    test_catalog_standards,
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
