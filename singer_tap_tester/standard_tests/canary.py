from singer_tap_tester import cli, user

def test_sync_canary(scenario):
    # Create Connection
    # Run Discovery
    catalog = cli.run_discovery(scenario.tap_name, scenario.get_config())
    # Select all streams and fields
    new_catalog = user.select_all_streams_and_fields(catalog)
    # Run sync
    tap_output = cli.run_sync(scenario.tap_name, scenario.get_config(), new_catalog, {})
    # Look at records and states and other things to ensure that everything is up to snuff
    pass
