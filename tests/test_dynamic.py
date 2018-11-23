"""
Ipyrest tests running examples stored in stand-alone code snippets.

These tests are all based on small use-cases implemented in individual
Python modules. They are expected to run stand-alone and create one
Api instance named e.g. ``api`` (but it can be any arbitrary name)
which will be inspected in the test functions contained here.

To be executed with pytest:

    pytest -s -v test_dynamic.py
"""

import os
from types import ModuleType
from typing import Optional

import pytest

from ipyrest import Api


def get_ipyrest_widget(module: ModuleType) -> Optional[Api]:
    "Return one Api widget inside a given module, if present, or None."

    for (name, obj) in module.__dict__.items():
        if obj.__class__ == Api:
            return obj
    return None


def test_usecase_jupyter_header():
    "Run dynamic test for external module."

    import usecase_jupyter_header as usecase
    w = get_ipyrest_widget(usecase)

    import json

    assert w.url_txt.value == w.url

    h = json.loads(w.resp_pane.get_child_named('Headers').value)
    assert h["Content-Type"] == "text/html; charset=utf-8"


HAVE_HEREMAPS_CREDS = os.getenv('HEREMAPS_APP_ID', None) and os.getenv('HEREMAPS_APP_CODE', None) 

@pytest.mark.skipif(not HAVE_HEREMAPS_CREDS, reason='Could not find HEREMAPS credentials.')
def test_usecase_here_geocoder():
    "Run dynamic test for external module."

    import usecase_here_geocoder as usecase
    w = get_ipyrest_widget(usecase)

    exp = {'Latitude': 52.53086, 'Longitude': 13.38474}
    res = w.resp.json()[
        'Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
    assert res == exp
