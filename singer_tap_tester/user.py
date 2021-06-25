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


LOG = logging.getLogger('alu_tester.user')

# TODO: What's the proper set of API functions here? This feels too verbose, but then again, the previous one felt too terse
# - Perhaps just having "select field" and "select stream" available, and allow folks to group them together as they see fit.
# - No need to provide an abstraction for a "map", comprehension, or "for"
# TODO: Can we do type hints somehow? Is that useful? Does that restrict valid Python versions too much?

# TODO: API style. Should it be immutable or mutable? I feel like for user interaction we want mutable, but who knows what the expectation is.

def select_stream(catalog_entry):
    "Appends `selected` metadata to the stream's catalog entry."

    tap_stream_id = catalog_entry['tap_stream_id']
    LOG.info(f'Selecting stream {tap_stream_id}')
    modified_entry = deepcopy(catalog_entry)

    for breadcrumb, md in modified_entry['metadata']:
        if breadcrumb == []:
            modified_entry['metadata']['selected'] = True

    return modified_entry

def select_all_streams(catalog):
    """Loop over a catalog and select the streams"""

    modified_catalog = deepcopy(catalog)
    modified_catalog['streams'] = list(map(select_stream, modified_catalog['streams']))

    return modified_catalog

def select_field(metadata_entry):
    modified_metadata_entry = deepcopy(metadata_entry)
    modified_metadata_entry['metadata']['selected'] = 'true'
    return modified_metadata_entry

def select_all_fields(catalog):
    modified_catalog = deepcopy(catalog)
    for catalog_entry in modified_catalog['streams']:
        for metadata_entry in catalog_entry['metadata']:
            if metadata_entry['breadcrumb'] is not []:
                metadata_entry['metadata']['selected'] = 'true'
    return modified_catalog

def select_all_streams_and_fields(catalog):
    modified_catalog = select_all_streams(catalog)
    return select_all_fields(modified_catalog)
