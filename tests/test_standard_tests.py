import os
import unittest
import unittest.mock
from singer_tap_tester import StandardTests

# Actual Usage Example
class TestGithubStandard(StandardTests):

    tap_name = "tap-github"

    def config_environment(self):
        return ["TAP_GITHUB_TOKEN"]

    def get_config(self):
        return {
            "start_date": "2021-06-17",
            "access_token": os.getenv("TAP_GITHUB_TOKEN"),
            "repository": "singer-io/singer-tap-tester",
            }

    #############################
    ### Tap Expectations
    #############################

    def expected_metadata(self):
        """The expected streams and metadata about the streams"""

        return {
            "assignees": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "collaborators": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "comments": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "commit_comments": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "commits": {
                self.PRIMARY_KEYS: {"sha"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "events": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"created_at"}
            },
            "issue_labels": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "issue_milestones": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"due_on"}
            },
            "issue_events": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"created_at"}
            },
            "issues": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "pr_commits": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "project_cards": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "project_columns": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "projects": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "pull_requests": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "releases": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "review_comments": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "reviews": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.INCREMENTAL,
                self.REPLICATION_KEYS: {"updated_at"}
            },
            "stargazers": {
                self.PRIMARY_KEYS: {"user_id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "team_members": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "team_memberships": {
                self.PRIMARY_KEYS: {"url"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            },
            "teams": {
                self.PRIMARY_KEYS: {"id"},
                self.REPLICATION_METHOD: self.FULL_TABLE,
            }
        }

# Check to ensure that all implementation requirements are checked
class TestBaseTestRequirements(unittest.TestCase):
    def test_standard_tests_run_and_check(self):
        tap_name_impl = "tap-its-a-test"
        config_environment_impl = lambda _: ["MY_PASSWORD_OR_TOKEN"]
        StandardTests.subclass_requirements = ["config_environment", "tap_name"]

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
