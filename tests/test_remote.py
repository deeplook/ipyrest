"""
Ipyrest tests running on remote APIs or sites.

To be executed with pytest:

    pytest -s -v test_remote.py
"""

import os

import pytest


def test_osm_tile():
    "Get PNG tile from tile.osm.org."

    from ipyrest import Api
    url = 'http://tile.osm.org/0/0/0.png'
    api = Api(url, click_send=True)

    assert api.url_txt.value == url
    assert api.resp.status_code == 200


def test_jupyter():
    "Get body of jupyter.org."

    from ipyrest import Api
    url = 'https://jupyter.org'
    api = Api(url, click_send=True)

    assert api.url_txt.value == url
    assert api.resp.status_code == 200


def test_google_header():
    "Get response header of google.com."

    import json
    from ipyrest import Api
    url = 'http://google.com'
    api = Api(url, click_send=True)

    assert api.url_txt.value == url

    h = json.loads(api.resp_pane.get_child_named('Headers').value)
    assert h["Content-Type"] == "text/html; charset=ISO-8859-1"

    
HAVE_HEREMAPS_CREDS = os.getenv('HEREMAPS_APP_ID', None) and os.getenv('HEREMAPS_APP_CODE', None) 

@pytest.mark.skipif(not HAVE_HEREMAPS_CREDS, reason='Could not find HEREMAPS credentials.')
def test_here_maptile_image():
    "Get maptile image from HERE.com."

    from ipyrest import Api
    url = 'https://1.{maptype}.maps.api.here.com/' \
          'maptile/2.1/{tiletype}/newest/{scheme}/{zoom}/{xtile}/{ytile}/{size}/{format}'
    args = dict(
        maptype='base',
        tiletype='maptile',
        scheme='normal.day',
        zoom='11',
        xtile='525',
        ytile='761',
        size='256',
        format='png8',
    )
    params = dict(
        app_id=os.getenv('HEREMAPS_APP_ID'),
        app_code=os.getenv('HEREMAPS_APP_CODE'),
        ppi='320',
    )

    # This needs to build the final URL, first, from the args and params
    # before sending the request! We simulate this here:
    url = url.format(**args)
    query = '&'.join(f'{k}={v}' for (k, v) in params.items())
    url = f'{url}?{query}'
    api = Api(url, click_send=True)

    # This should do it all by itself:
    # api = Api(url, args=args, params=params, click_send=True)

    img = api.resp_pane.get_child_named(
        'Content').get_child_named('Image').value
    assert img.startswith(b'\x89PNG\r\n')
