"""
Ipyrest tests running on a local server implementing sample API endpoints.

To be executed with pytest:

    pytest -s -v test_local.py
"""

from os.path import exists, join

import pytest
import timeout_decorator

from api_server import app, find_free_port, run_flask_app
from ipyrest import Api, recorder


port = find_free_port()
kwargs = dict(host='0.0.0.0', port=port, debug=False)
run_flask_app(app, kwargs)
server = f'http://localhost:{port}'
SERVER_NOT_FOUND = False


def test_empty():
    "Create empty box, do not send any request."

    Api()
    assert True


def test_gpx():
    "Make simple GPX request."

    Api(f'{server}/get_gpx', click_send=True)


def test_vcr():
    "Make simple request, record in a VCR cassete."

    cassette_path = 'cassette3.yaml'
    Api(f'{server}/get_header', cassette_path=cassette_path,
        click_send=True)  # get_json
    assert exists(join(recorder.cassette_library_dir, cassette_path))


def test_api_local():
    "Create empty box, do nothing else."

    Api(f'{server}/get_json')
    assert True


def test_timeout():
    "Timeout."

    Api(f'{server}/get_slow/sleep/1.0', click_send=True)
    assert True


def test_do_timeout():
    "Do timeout."

    # Tried with pytest.raises(Exception), but no luck:
    # https://stackoverflow.com/questions/23337471/how-to-properly-assert-that-an-exception-gets-raised-in-pytest#29855337

    api = Api(f'{server}/get_slow/sleep/2.0', timeout=1)
    try:
        api.click_send()
    except timeout_decorator.TimeoutError:
        assert True
