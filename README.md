Ipyrest
=======

[![Binder](https://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/deeplook/ipyrest/master) 
[![Nbviewer](https://img.shields.io/badge/render-nbviewer-orange.svg)](http://nbviewer.jupyter.org/github/deeplook/ipyrest/tree/master/)
[![Travis-CI](http://img.shields.io/travis/deeplook/ipyrest.svg)](https://travis-ci.org/deeplook/ipyrest)
[![image](https://img.shields.io/pypi/implementation/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![image](https://img.shields.io/pypi/pyversions/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![image](https://img.shields.io/pypi/v/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![image](https://img.shields.io/pypi/dm/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![image](https://img.shields.io/pypi/l/ipyrest.svg)](https://pypi.org/project/ipyrest/)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/deeplook)

Ipyrest is an emerging Jupyter notebook widget for exploring RESTful APIs. It has two main goals: provide a more convenient interface in the spirit of Postman, and allow for plug-in components, starting with output renderers for various MIME types, e.g. GeoJSON, see below.

About
-----

At its core ipyrest is a wrapper for the excellent requests package based on the equally excellent ipywidgets package. The idea is to provide more interactive exploration capabilities when working with RESTful APIs. It does so by letting you build requests for an API call and understand more quickly the responses you receive. To that end you can use existing views for requests and responses or build your own. It is inspired by Postman, but without the bloat, and goes beyond it to make sure you can extend it the way you want. In essence, it's for data scientists rather than web developers. 


Example
-------

``` {.sourceCode .python}
from ipyrest import Api

# Fix content-type as it is not set for gists.
def reset_content_type(resp):
    resp.headers['Content-Type'] = 'application/vnd.geo+json'

url = 'https://gist.githubusercontent.com/' \
      'deeplook/71e9ded257cfc2d8e5e9/raw/f0cfbab5f266fcb8056e8aea046f1f222346b76b/2013.geojson'
Api(url, post_process_resp=reset_content_type)
```

![banner](https://github.com/deeplook/ipyrest/raw/master/images/banner.png "")

Features
--------

Ipyrest deals with the following concepts, implemented to varying degrees: HTTP Server, Service, Request, Response, Data, MIME-Types, Compression, Logging, Caching, Time-Outs, Errors, Views, Plugins, Testing, and UI.

At the moment the following plugins are available for rendering output from HTTP responses in common formats: Plain Text, CSV, HTML, Bitmaps, SVG, JSON, GeoJSON, GPX, Protobuf, (and some experimental 3D stuff).

The main dependencies are: Python >= 3.6, jupyter, ipywidgets, timeout_decorator, requests, and vcr. Plugin dependencies are: ipyleaflet, ipyvolume, geojson, qgrid, protobuf. Testing dependencies are flask, mypy, and pytest.

Installation
------------

Released versions of ipyrest can be installed from PyPI with:

``` {.sourceCode .bash}
pip install ipyrest
```

Development versions of ipyrest can be installed either directly from GitHub or after downloading/cloning and unpacking like this in its top-level directory:

``` {.sourceCode .bash}
pip install git+https://github.com/deeplook/ipyrest

pip install -e .
```

Testing
-------

Run `pip install -r requirements_test.txt` and `PYTHONPATH=. pytest -s -v tests` in the root directory. Some tests will automatically start a local flask webserver in `tests/api_server.py` which implements a set of sample API endpoints for local testing. And some of these tests need keys/tokens defined as environment variables for the respective APIs being tested. If not present these tests will be skipped.

Documentation
-------------

The `docs` folder is only a stub for now. At the moment it is recommended to look at [`examples/meetup.ipynb`](examples/meetup.ipynb), mostly a tutorial-like collection of examples given as a presentation at a meetup. Some of these need appropriate API keys.

How to Contribute
-----------------

1.  Check for open issues or open a fresh issue to start a discussion
    around a feature idea or a bug or example for some API (ideally without
    authentication), e.g. from the extensive collection of
    [Public APIs](https://github.com/toddmotto/public-apis).
2.  Fork [the repository](https://github.com/deeplook/ipyrest) on
    GitHub to start making your changes to the **master** branch (or
    branch off of it).
3.  Write a test which shows that the bug was fixed or that the feature
    works as expected.
4.  Send a pull request and bug the maintainer until it gets merged and
    published. :) Make sure to add yourself to
    [AUTHORS](https://github.com/deeplook/ipyrest/blob/master/AUTHORS.rst).
