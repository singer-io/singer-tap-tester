import re
from singer_tap_tester import cli, user

def test_catalog_standards(scenario):
    """
    The purpose of this test is to run the tap's discovery mode and
    verify a valid catalog is produced
    """
    catalog = cli.run_discovery(scenario.tap_name, scenario.get_config())

    def get_catalog_entry(stream):
        catalog_entry = [entry for entry in catalog['streams']
                         if entry["stream"] == stream][0]
        return catalog_entry

    def get_stream_level_properties(stream):
        catalog_entry = get_catalog_entry(stream)
        metadata = catalog_entry["metadata"]
        stream_properties = [item for item in metadata if item.get("breadcrumb") == []]

        return stream_properties


    # verify only expected streams were discovered
    expected_streams = scenario.expected_streams()

    discovered_streams = {entry['stream'] for entry in catalog['streams']}

    scenario.assertSetEqual(expected_streams, discovered_streams)


    # verify tap_stream_id follows the naming convention that
    # streams should only have lowercase alphas and underscores
    for stream in expected_streams:
        with scenario.subTest(stream=stream):
            catalog_entry = get_catalog_entry(stream)
            scenario.assertTrue(re.fullmatch(r"[a-z_0-9]+",  catalog_entry['tap_stream_id']),
                            msg="This stream doesn't follow standard naming.")


    # verify there is only 1 top level breadcrumb in metadata
    for stream in expected_streams:
        with scenario.subTest(stream=stream):
            stream_properties = get_stream_level_properties(stream)
            scenario.assertEqual(1, len(stream_properties))


    # verify expected primary key(s) are specified in metadata
    for stream in expected_streams:
        with scenario.subTest(stream=stream):
            expected_primary_keys = scenario.expected_primary_keys()[stream]

            stream_properties = get_stream_level_properties(stream)
            actual_primary_keys = set(
                stream_properties[0].get(
                    "metadata", {scenario.PRIMARY_KEYS: []}).get(scenario.PRIMARY_KEYS, [])
            )

            scenario.assertSetEqual(expected_primary_keys, actual_primary_keys)


    # test replication methods in metadata
    for stream in expected_streams:
        with scenario.subTest(stream=stream):

            expected_replication_method = scenario.expected_replication_method()[stream]
            expected_replication_keys = scenario.expected_replication_keys()[stream]

            stream_properties = get_stream_level_properties(stream)
            actual_replication_method = stream_properties[0].get(
                "metadata", {scenario.REPLICATION_METHOD: None}).get(scenario.REPLICATION_METHOD)
            actual_replication_keys = set(
                stream_properties[0].get(
                    "metadata", {scenario.REPLICATION_KEYS: []}).get(scenario.REPLICATION_KEYS, [])
            )

            # verify the forced replication method matches our expectations
            scenario.assertEqual(expected_replication_method, actual_replication_method)

            # verify expected replication key(s) are specified in metadata
            scenario.assertSetEqual(expected_replication_keys, actual_replication_keys)

            # verify that if there is a replication key we are doing INCREMENTAL
            if actual_replication_keys:
                scenario.assertEqual(
                    scenario.INCREMENTAL, actual_replication_method,
                    msg=f"Invalid replication.  Method: {actual_replication_method}  Replication Keys: {actual_replication_keys}."
                )
            else:  # verify if there is no replication key we are doing FULL TABLE
                scenario.assertEqual(
                    scenario.FULL_TABLE, actual_replication_method,
                    msg=f"Invalid replication.  Method: {actual_replication_method}  Replication Keys: {actual_replication_keys}."
                )

    # verify that primary keys and replication keys
    # are given the inclusion of automatic in metadata
    for stream in expected_streams:
        with scenario.subTest(stream=stream):
            expected_automatic_fields = scenario.expected_automatic_fields()[stream]

            metadata = get_catalog_entry(stream)["metadata"]
            actual_automatic_fields = set(
                item.get("breadcrumb", ["properties", None])[1] for item in metadata
                if item.get("metadata").get("inclusion") == "automatic"
            )

            scenario.assertSetEqual(expected_automatic_fields, actual_automatic_fields)

    # verify that all other fields have inclusion of available
    # This assumes there are no unsupported fields for SaaS sources
    for stream in expected_streams:
        with scenario.subTest(stream=stream):
            metadata = get_catalog_entry(stream)["metadata"]

            actual_fields = set(
                item.get("breadcrumb", ["properties", None])[1] for item in metadata
                if item.get("breadcrumb") != []
            )
            actual_automatic_fields = set(
                item.get("breadcrumb", ["properties", None])[1] for item in metadata
                if item.get("metadata").get("inclusion") == "automatic"
           )
            actual_available_fields = set(
                item.get("breadcrumb", ["properties", None])[1] for item in metadata
                if item.get("metadata").get("inclusion") == "available"
            )

            scenario.assertSetEqual(actual_fields - actual_automatic_fields, actual_available_fields)
