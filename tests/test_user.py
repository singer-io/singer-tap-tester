import unittest
from singer_tap_tester import user

class TestStreamSelection(unittest.TestCase):
    def test_select_stream_from_catalog_entry(self):
        # Arrange
        catalog_entry = {"tap_stream_id": "stream id name",
                         "stream": "name",
                         "key_properties": [],
                         "schema": {},
                         "replication_key": "id",
                         "replication_method": "FULL_TABLE",
                         "stream_alias": "alias name",
                         "metadata": [{"breadcrumb": [],
                                       "metadata": {"other_key": 1}},
                                       {"breadcrumb": ["properties", "field1"],
                                       "metadata": {"other_key": 1}},
                                       {"breadcrumb": ["properties", "field2"],
                                       "metadata": {"other_key": 1}}]
                         }
        # Act
        new_catalog_entry = user.select_stream(catalog_entry)
        # Assert
        self.assertEqual({"other_key": 1, "selected": True},
                         new_catalog_entry["metadata"][0]["metadata"])
        for mdata in new_catalog_entry["metadata"][1:]:
            self.assertEqual({"other_key": 1}, mdata["metadata"])
        self.assertIsNot(catalog_entry, new_catalog_entry)

    def test_select_all_streams_in_catalog(self):
        catalog = {
            "streams": [
                {"tap_stream_id": "stream id name",
                 "stream": "name",
                 "key_properties": [],
                 "schema": {},
                 "replication_key": "id",
                 "replication_method": "FULL_TABLE",
                 "stream_alias": "alias name",
                 "metadata": [{"breadcrumb": [],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field1"],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field2"],
                               "metadata": {"other_key": 1}}]},
                {"tap_stream_id": "stream id name2",
                 "stream": "name2",
                 "key_properties": [],
                 "schema": {},
                 "replication_key": "id",
                 "replication_method": "FULL_TABLE",
                 "stream_alias": "alias name2",
                 "metadata": [{"breadcrumb": [],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field1"],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field2"],
                               "metadata": {"other_key": 1}}]}]}

        new_catalog = user.select_all_streams(catalog)

        for stream in new_catalog["streams"]:
            self.assertEqual({"other_key": 1, "selected": True}, stream["metadata"][0]["metadata"])
            for mdata in stream["metadata"][1:]:
                self.assertEqual({"other_key": 1}, mdata["metadata"])
        self.assertIsNot(catalog, new_catalog)

class TestFieldSelection(unittest.TestCase):
    def test_select_field_from_metadata_entry(self):
        metadata_entry = {"breadcrumb": ["properties", "field1"],
                          "metadata": {"other_key": 1}}

        new_metadata_entry = user.select_field(metadata_entry)
        self.assertEqual({"other_key": 1, "selected": True}, new_metadata_entry["metadata"])
        self.assertIsNot(metadata_entry, new_metadata_entry)

    def test_select_all_fields_from_catalog_entry(self):
        catalog_entry = {
            "tap_stream_id": "stream id name",
            "stream": "name",
            "key_properties": [],
            "schema": {},
            "replication_key": "id",
            "replication_method": "FULL_TABLE",
            "stream_alias": "alias name",
            "metadata": [{"breadcrumb": [],
                          "metadata": {"other_key": 1}},
                         {"breadcrumb": ["properties", "field1"],
                          "metadata": {"other_key": 1}},
                         {"breadcrumb": ["properties", "field2"],
                          "metadata": {"other_key": 1}}]}

        new_catalog_entry = user.select_all_fields(catalog_entry)

        self.assertEqual({"other_key": 1}, new_catalog_entry["metadata"][0]["metadata"])
        for mdata in new_catalog_entry["metadata"][1:]:
            self.assertEqual({"other_key": 1, "selected": True}, mdata["metadata"])
        self.assertIsNot(catalog_entry, new_catalog_entry)

class SelectAllStreamsAndFields(unittest.TestCase):
    def test_select_all_streams_and_fields_in_catalog(self):
        catalog = {
            "streams": [
                {"tap_stream_id": "stream id name",
                 "stream": "name",
                 "key_properties": [],
                 "schema": {},
                 "replication_key": "id",
                 "replication_method": "FULL_TABLE",
                 "stream_alias": "alias name",
                 "metadata": [{"breadcrumb": [],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field1"],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field2"],
                               "metadata": {"other_key": 1}}]},
                {"tap_stream_id": "stream id name2",
                 "stream": "name2",
                 "key_properties": [],
                 "schema": {},
                 "replication_key": "id",
                 "replication_method": "FULL_TABLE",
                 "stream_alias": "alias name2",
                 "metadata": [{"breadcrumb": [],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field1"],
                               "metadata": {"other_key": 1}},
                              {"breadcrumb": ["properties", "field2"],
                               "metadata": {"other_key": 1}}]}]}

        new_catalog = user.select_all_streams_and_fields(catalog)
        for stream in new_catalog["streams"]:
            for mdata in stream["metadata"]:
                self.assertEqual({"other_key": 1, "selected": True}, mdata["metadata"])
        self.assertIsNot(catalog, new_catalog)
