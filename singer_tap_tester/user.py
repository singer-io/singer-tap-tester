"""
This module contains tools to perform actions that are usually performed by
a user. The most common being selection of fields and streams.

### A Note on Standards ###
All functions within this module should not modify the object passed in, but
copy it and return a new one in order to allow for flexibility in assertions
for test authors.
"""

from copy import deepcopy
from collections import defaultdict
import logging
import sys

# TODO: Make this easier to work with?
# FIXME: It's doubling logs now, likely due to singer-python's logger existing...
LOGGER = logging.getLogger("singer_tap_tester.user")
LOGGER.setLevel(logging.INFO)
formatter = logging.Formatter(fmt='%(levelname)s %(message)s', datefmt='')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

def select_stream(catalog_entry):
    "Appends `selected` metadata to the stream's catalog entry."

    tap_stream_id = catalog_entry['tap_stream_id']
    LOGGER.info(f'Selecting stream {tap_stream_id}')

    modified_entry = deepcopy(catalog_entry)

    for mdata in modified_entry['metadata']:
        if mdata['breadcrumb'] == []:
            mdata['metadata']['selected'] = True

    return modified_entry

def select_all_streams(catalog):
    """Loop over a catalog and select the streams"""

    modified_catalog = deepcopy(catalog)
    modified_catalog['streams'] = list(map(select_stream, modified_catalog['streams']))

    return modified_catalog

# TODO FIXME: This should respect `"inclusion": "unsupported"`
def select_field(metadata_entry):
    modified_metadata_entry = deepcopy(metadata_entry)
    modified_metadata_entry['metadata']['selected'] = True
    return modified_metadata_entry

def select_all_fields(catalog_entry):
    modified_catalog_entry = deepcopy(catalog_entry)

    modified_catalog_entry['metadata'] = [select_field(m) if m['breadcrumb'] != [] else m
                                          for m in modified_catalog_entry['metadata']]

    return modified_catalog_entry

def select_all_streams_and_fields(catalog):
    modified_catalog = select_all_streams(catalog)
    modified_catalog['streams'] = list(map(select_all_fields, modified_catalog['streams']))
    return modified_catalog
