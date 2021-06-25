from singer_tap_tester import cli, user

def test_sync_canary(scenario):
    """
    The purpose of this test is to run the tap with all streams
    selected to naively exercise all code and any changes to those
    streams.

    This is certainly not comprehensive, and assumes that all
    streams have data, but is generally enough to provide some
    value.
    """
    catalog = cli.run_discovery(scenario.tap_name, scenario.get_config())
    new_catalog = user.select_all_streams_and_fields(catalog)
    tap_output = cli.run_sync(scenario.tap_name, scenario.get_config(), new_catalog, {})
    # TODO: Do assertions on messages and types
    # TODO: Run through target's validating handler
    # TODO: Generate a final summary report so that this test can be used to gauge the potential usefulness of the specific data set available to the test author/runner
