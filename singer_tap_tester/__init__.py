from . import user

from .sample_tests import StandardTests
from io import StringIO
import sys
import unittest


def capture_output(func, *args, **kwargs):
    temp_out = StringIO()
    temp_out.seek(0)

    sys.stdout = temp_out

    getbuffer = kwargs.pop('getbuffer', None)
    func(*args, **kwargs)

    sys.stdout = sys.__stdout__
    if getbuffer:
        return temp_out
    return temp_out.getvalue()

if __name__ == '__main__':
    unittest.main()
