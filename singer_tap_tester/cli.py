import io
import inspect
import json
import sys
import unittest.mock
import tempfile

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
    if not found_entry_points:
        raise Exception(f"Ambiguous entry_point - {len(found_entry_points)} entrypoints found in current (virtual) environment to run tap using command: '{run_command}'")
    discovered_main = entry_points[0].resolve()
    return discovered_main()

# TODO: How to structure this? I'd kind of like to just build a runner object that does all the things it needs. Might get out of control? Not sure...

def run_discovery(config):
    # Call it with mocks and temp files to simulate CLI
    patched_io = PatchStdOut()
    with patched_io, \
         tempfile.NamedTemporaryFile(mode='w') as config_file, \
         unittest.mock.patch('sys.argv', ['tap-tester', '--discover', '--config', config_file.name]):
        
        json.dump(config, config_file)
        config_file.flush()
        __call_entry_point()

        # Return result of mocked sys.stdout
        return patched_io.out.getvalue()
