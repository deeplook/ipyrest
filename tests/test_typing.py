"""
Ipyrest tests running typechecks on its own modules.

To be executed with pytest:

    pytest -s -v test_typing.py
"""

import pytest
from mypy import api
from typing import List, Tuple, Iterator


TypeComplaint = Iterator[Tuple[str, int, str, str]]


def type_scan(paths: List[str], flags: List[str] = []) -> TypeComplaint:
    """
    Scan a file with given path using MyPy with given Boolean flags to report typing issues.

    Yields (fn, lineno, type, line) tuples.
    """
    cmd = ['--' + f for f in flags] + paths
    stdout, stderr, status = api.run(cmd)
    lines = stdout.strip().split('\n')
    for line in lines:
        fn, lineno, typ, line = map(lambda s: s.strip(), line.split(':', 3))
        print(fn, lineno, typ, line)
        yield fn, int(lineno), typ, line


@pytest.mark.skip(reason="Need to consolidate more.")
def test_static_typing():
    """Test if mypy has no typing complaints about this package."""

    from ipyrest import ipyrest, extendedtab, responseviews
    files = [m.__file__ for m in (ipyrest, extendedtab, responseviews)]
    scan = type_scan(files, flags=['ignore-missing-imports'])
    assert len(list(scan)) == 0
