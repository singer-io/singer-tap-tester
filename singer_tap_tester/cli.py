import io
import inspect
import logging
import os
import json
import sys
import unittest.mock
import tempfile
from contextlib import contextmanager, ExitStack

LOGGER = logging.getLogger("singer_tap_tester.cli")

class PatchStdOut():
    """
    Context Manager that will take stdout and patch it such that any tap
    output is captured by the StringIO object associated with this context
    manager's instance, while still letting PDB prompt output through to
    the terminal.

    Any time an attempt occurs to write text to stdout, the stack frames will
    be inspected. If `pdb.py` shows up, this is taken as a debugger session
    and will pass through, otherwise, the output is assumed to be tap output
    and will pass on to the StringIO object stored on this object.
    """
    __old_std_out_write = sys.stdout.write

    def __init__(self):
        self.out = io.StringIO()

    def stdout_dispatcher(self, text):
        pdb_frames = [f.filename for f in inspect.stack() if f.filename.endswith('pdb.py')]
        if pdb_frames:
            self.__old_std_out_write(text)
        else:
            self.out.write(text)

    def __enter__(self):
        sys.stdout.write = self.stdout_dispatcher

    def __exit__(self, _tp, _v, _tb):
        sys.stdout.write = self.__old_std_out_write

def __call_entry_point(run_command):
    # Find Main Entry Point through package resources
    entry_maps = [a.get_entry_map() for a in __import__('pkg_resources').working_set if 'tap-' in a.project_name]
    found_entry_points = [fun
                          for entry_map in entry_maps
                          for fun in entry_map.get('console_scripts',{}).values()
                          if fun.name == run_command]
    if not found_entry_points:
        raise Exception(f"No entrypoints found in current (virtual) environment to run tap using command: '{run_command}'")
    if len(found_entry_points) > 1:
        raise Exception(f"Ambiguous entry_point - {len(found_entry_points)} entrypoints found in current (virtual) environment to run tap using command: '{run_command}'")
    discovered_main = found_entry_points[0].resolve()
    return discovered_main()


def __run_tap(tap_entry_point,config=None,catalog=None,state=None,discover=False):
    patched_io = PatchStdOut()
    context_managers = [patched_io]
    argvs = [tap_entry_point]
    if discover:
        argvs.append('--discover')

    if config:
        file_name = '/tmp/tap_config.json'
        with open('/tmp/tap_config.json', 'w') as f:
            json.dump(config, f)
        argvs.extend(['--config', file_name])

    if catalog:
        file_name = '/tmp/tap_catalog.json'
        with open(file_name, 'w') as f:
            json.dump(catalog, f)
        argvs.extend(['--catalog', file_name])

    if state:
        file_name = '/tmp/tap_state.json'
        with open(file_name, 'w') as f:
            json.dump(state, f)
        argvs.extend(['--state', file_name])

    LOGGER.info(f"CLI command to reproduce: {' '.join(argvs)}")
    context_managers.append(unittest.mock.patch('sys.argv', argvs))

    with ExitStack() as stack:
        # Dynamically enter all contexts and reguster with stack to __exit__
        # properly
        for cm in context_managers:
            stack.enter_context(cm)

        __call_entry_point(tap_entry_point)
        return patched_io.out.getvalue()

def run_discovery(tap_entry_point, config):
    # Call it with mocks and temp files to simulate CLI
    LOGGER.info("Running discovery...")
    catalog = __run_tap(tap_entry_point, config=config, discover=True)

    # Run check mode so we can validate the creds. Should not sync any records
    LOGGER.info("Running sync without catalog to validate config.")
    __run_tap(tap_entry_point, config=config)

    return json.loads(catalog)

def run_sync(tap_entry_point, config, catalog, state):

    LOGGER.info("Running sync...")
    raw_singer_messages = __run_tap(tap_entry_point, config=config, catalog=catalog, state=state)

    return list(map(json.loads, raw_singer_messages.strip().split(os.linesep)))
