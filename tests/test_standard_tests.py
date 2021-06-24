import os
import unittest
import unittest.mock
from singer_tap_tester import StandardTests

# Actual Usage Example
class TestGithubStandard(StandardTests):
    def tap_name(self):
        return "tap-github"

    def config_environment(self):
        return ["TAP_GITHUB_TOKEN"]

# Check to ensure that all implementation requirements are checked
class TestBaseTestRequirements(unittest.TestCase):
    def test_standard_tests_run_and_check(self):
        tap_name_impl = lambda _: "tap-its-a-test"
        config_environment_impl = lambda _: ["MY_PASSWORD_OR_TOKEN"]

        def make_test_class(impls):
            return type('TestStandardTests',
                        (StandardTests,),
                        impls)

        TestStandardTestsMissingConfig = make_test_class({
            "tap_name": tap_name_impl,
            })
        TestStandardTestsMissingName = make_test_class({
            "config_environment": config_environment_impl,
            })
        TestStandardTestsMissingAll = make_test_class({})

        # Assert all required implementations are checked
        with self.assertRaises(NotImplementedError) as missing_config:
            unittest.TextTestRunner().run(unittest.makeSuite(TestStandardTestsMissingConfig))
        with self.assertRaises(NotImplementedError) as missing_name:
            unittest.TextTestRunner().run(unittest.makeSuite(TestStandardTestsMissingName))
        with self.assertRaises(NotImplementedError) as missing_all:
            unittest.TextTestRunner().run(unittest.makeSuite(TestStandardTestsMissingAll))

        self.assertIn("['config_environment']", str(missing_config.exception))
        self.assertIn("['tap_name']", str(missing_name.exception))
        self.assertIn("['config_environment', 'tap_name']", str(missing_all.exception))

        with unittest.mock.patch('singer_tap_tester.base.standard_test_functions', {lambda scen: print("Ran mocked test!")}):
            TestStandardTestsFullImpl = make_test_class({
                "config_environment": config_environment_impl,
                "tap_name": tap_name_impl,
            })

            # Assert environment variable existence is checked
            missing_env_var_message = "Missing environment variables required to run the tap for this test: ['MY_PASSWORD_OR_TOKEN']"
            with self.assertRaises(Exception) as missing_env_var:
                unittest.TextTestRunner().run(unittest.makeSuite(TestStandardTestsFullImpl))
            self.assertEqual(missing_env_var_message, str(missing_env_var.exception))

            # Assert Happy Path Passes
            with open('/dev/null', 'w') as devnull:
                os.environ["MY_PASSWORD_OR_TOKEN"] = "itisset!"
                unittest.TextTestRunner(stream=devnull).run(unittest.makeSuite(TestStandardTestsFullImpl))
