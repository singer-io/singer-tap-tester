import unittest

# TODO: This is the bread and butter of this. Base_Test suite should be a module that defines these pieces with a usable API that someone could extend.
# - Things like ensuring at startup that the child class has implemented everything.
# - It should be very friendly.

class EnableTest(unittest.TestCase):
    __test__ = True

class BaseTest(unittest.TestCase):

    __test__ = False
    def test_run(self):
        print(f'Hi from {self.__class__}')
        self.assertEqual(1, 1)

class DiscoveryTest(BaseTest):
    def test_run(self):
        print(f'Discovery test is different than Base {self.__class__}')


class AutomaticFieldsTest(BaseTest):
    pass


class StartDateTest(BaseTest):
    pass


class PaginationTest(BaseTest):
    pass


class BookmarksTest(BaseTest):
    pass


class AllFieldsTest(BaseTest):
    pass
