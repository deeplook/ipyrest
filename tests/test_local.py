"""
Ipyrest tests running on a local server implementing sample API endpoints.

To be executed with pytest:

    pytest -s -v test_local.py
"""

from os.path import exists, join

import pytest
import requests


server = 'http://localhost:5000'
try:
    requests.get(f'{server}/')
    SERVER_NOT_FOUND = False
except requests.exceptions.ConnectionError:
    SERVER_NOT_FOUND = True


def test_empty():
    "Create empty box, do not send any request."

    from ipyrest import Api
    Api()
    assert True


@pytest.mark.skipif(SERVER_NOT_FOUND, reason="API server not found.")
def test_gpx():
    "Make simple GPX request."

    from ipyrest import Api
    server = 'http://localhost:5000'
    Api(f'{server}/get_gpx', click_send=True)


# @pytest.mark.skip(reason="Not ready yet.")
@pytest.mark.skipif(SERVER_NOT_FOUND, reason="API server not found.")
def test_vcr():
    "Make simple request, record in a VCR cassete."

    from ipyrest import Api, recorder
    server = 'http://localhost:5000'
    cassette_path = 'cassette3.yaml'
    Api(f'{server}/get_header', cassette_path=cassette_path,
        click_send=True)  # get_json
    assert exists(join(recorder.cassette_library_dir, cassette_path))


@pytest.mark.skipif(SERVER_NOT_FOUND, reason="API server not found.")
def test_api_local():
    "Create empty box, do nothing else."

    from ipyrest import Api
    server = 'http://localhost:5000'
    Api(f'{server}/get_json')
    assert True


@pytest.mark.skipif(SERVER_NOT_FOUND, reason="API server not found.")
def test_timeout():
    "Timeout."

    from ipyrest import Api
    server = 'http://localhost:5000'
    Api(f'{server}/get_slow/sleep/1.0', click_send=True)
    assert True


@pytest.mark.skipif(SERVER_NOT_FOUND, reason="API server not found.")
def test_do_timeout():
    "Do timeout."

    # Tried with pytest.raises(Exception), but no luck:
    # https://stackoverflow.com/questions/23337471/how-to-properly-assert-that-an-exception-gets-raised-in-pytest#29855337

    import timeout_decorator
    from ipyrest import Api
    server = 'http://localhost:5000'
    api = Api(f'{server}/get_slow/sleep/2.0', timeout=1)
    try:
        api.click_send()
    except timeout_decorator.TimeoutError:
        assert True
