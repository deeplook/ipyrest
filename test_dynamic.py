"""
IPyPostman tests running examples stored in stand-alone code snippets.

These tests are all based on small use-cases implemented in individual
Python modules. They are expected to run stand-alone and create one
Api instance named e.g. ``api`` (but it can be any arbitrary name)
which will be inspected in the test functions contained here.

To be executed with PyTest:

    pytest -s -v test_dynamic.py
"""


from types import ModuleType
from typing import Optional

from ipyrest import Api


def get_postman_widget(module: ModuleType) -> Optional[Api]:
    "Return one Api widget inside a given module, if present, or None."

    for (name, obj) in module.__dict__.items():
        if obj.__class__ == Api:
            return obj
    return None


def test_usecase_jupyter_header():
    "Run dynamic test for external module."

    import usecase_jupyter_header as usecase
    pmw = get_postman_widget(usecase)
    
    import json

    assert pmw.url_txt.value == pmw.url

    h = json.loads(pmw.resp_pane.get_child_named('Headers').value)
    assert h["Content-Type"] == "text/html; charset=utf-8"

    
def test_usecase_here_geocoder():
    "Run dynamic test for external module."

    import usecase_here_geocoder as usecase
    pmw = get_postman_widget(usecase)
    
    exp = {'Latitude': 52.5308599, 'Longitude': 13.38474}
    res = pmw.resp.json()['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
    assert res == exp
