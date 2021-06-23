from singer_tap_tester import StandardTests

# TODO: Mock out the tests so that this can continue to run even after they've been implemented
class TestStandardTests(StandardTests):
    def config_environment(self):
        return ["MY_PASSWORD_OR_TOKEN"]
